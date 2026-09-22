"""
Multi-Source Data Ingestion Engine
Handles structured and unstructured datasets: FIRs, CDR CSVs, Financial logs, Surveillance files, and SOCMINT feeds.
"""

import pandas as pd
import io
from nlp_extractor import NLPEntityExtractor

class MultiSourceDataLoader:
    """
    Parses diverse multi-source files into standardized nodes and edges dataframes.
    """

    @staticmethod
    def load_fir_narrative(fir_text: str):
        """Processes unstructured FIR narrative text via NLP entity extractor."""
        extractor = NLPEntityExtractor()
        df_nodes, df_edges = extractor.extract_entities_and_relationships(fir_text)
        return df_nodes, df_edges

    @staticmethod
    def load_cdr_csv(file_obj) -> pd.DataFrame:
        """Loads and normalizes Call Detail Record (CDR) CSV files."""
        df_cdr = pd.read_csv(file_obj)

        # Standardize column headers
        col_map = {
            "calling_number": "caller",
            "from": "caller",
            "source_phone": "caller",
            "called_number": "callee",
            "to": "callee",
            "target_phone": "callee",
            "date_time": "timestamp",
            "call_date": "timestamp",
            "duration_sec": "duration"
        }
        df_cdr = df_cdr.rename(columns={k: v for k, v in col_map.items() if k in df_cdr.columns})

        nodes = []
        edges = []
        unique_phones = set(df_cdr['caller']).union(set(df_cdr['callee']))

        for ph in unique_phones:
            nodes.append({
                "id": str(ph),
                "name": str(ph),
                "type": "Phone",
                "risk_score": 65,
                "status": "CDR Tracked",
                "notes": "Ingested from CDR file."
            })

        for _, row in df_cdr.iterrows():
            caller = str(row['caller'])
            callee = str(row['callee'])
            ts = str(row.get('timestamp', '2026-03-01'))
            dur = float(row.get('duration', 60))

            edges.append({
                "source": caller,
                "target": callee,
                "relationship": "CALL_BURST" if dur < 10 else "CALL_MADE",
                "weight": 1,
                "timestamp": ts,
                "amount": 0,
                "details": f"Duration: {dur}s"
            })

        return pd.DataFrame(nodes), pd.DataFrame(edges)

    @staticmethod
    def load_financial_csv(file_obj) -> pd.DataFrame:
        """Loads and normalizes Financial Transaction CSV files."""
        df_fin = pd.read_csv(file_obj)

        col_map = {
            "source": "source",
            "sender": "source",
            "from_account": "source",
            "target": "target",
            "receiver": "target",
            "to_account": "target",
            "tx_amount": "amount",
            "value": "amount"
        }
        df_fin = df_fin.rename(columns={k: v for k, v in col_map.items() if k in df_fin.columns})

        nodes = []
        edges = []
        unique_accs = set(df_fin['source']).union(set(df_fin['target']))

        for acc in unique_accs:
            acc_type = "Crypto Wallet" if str(acc).startswith("0x") else "Bank Account"
            nodes.append({
                "id": str(acc),
                "name": str(acc),
                "type": acc_type,
                "risk_score": 75,
                "status": "Financial Audit",
                "notes": f"Ingested from Financial Log."
            })

        for _, row in df_fin.iterrows():
            src = str(row['source'])
            dst = str(row['target'])
            amt = float(row.get('amount', 0))
            ts = str(row.get('timestamp', '2026-03-01'))

            rel = "CRYPTO_TRANSFER" if src.startswith("0x") or dst.startswith("0x") else "MONEY_TRANSFERRED"
            edges.append({
                "source": src,
                "target": dst,
                "relationship": rel,
                "weight": max(1, int(amt / 10000)),
                "timestamp": ts,
                "amount": amt,
                "details": f"Wire transfer of ${amt:,.2f}"
            })

        return pd.DataFrame(nodes), pd.DataFrame(edges)
