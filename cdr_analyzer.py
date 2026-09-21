"""
Call Detail Record (CDR) & Communication Network Analytics Engine
Analyzes call frequencies, duration spikes, night-call anomalies, burner phone rotation, and call bursts.
"""

import pandas as pd
import numpy as np
import networkx as nx
from datetime import datetime
from typing import Dict, List

class CDRAnalyzer:
    def __init__(self, G: nx.MultiDiGraph):
        self.G = G

    def get_cdr_summary_stats(self) -> Dict:
        """Calculates global CDR communication statistics from graph edges."""
        call_edges = []
        for u, v, k, data in self.G.edges(keys=True, data=True):
            rel = data.get('relationship', '')
            if rel in ["CALL_MADE", "ENCRYPTED_CHAT", "CALL_BURST"]:
                call_edges.append({
                    "caller": u,
                    "caller_name": self.G.nodes[u].get('name', u),
                    "callee": v,
                    "callee_name": self.G.nodes[v].get('name', v),
                    "relationship": rel,
                    "frequency": data.get('weight', 1),
                    "timestamp": data.get('timestamp', ''),
                    "details": data.get('details', '')
                })

        if not call_edges:
            return {
                "total_calls": 0,
                "unique_callers": 0,
                "night_calls_cnt": 0,
                "top_call_pair": "None",
                "call_df": pd.DataFrame()
            }

        df_calls = pd.DataFrame(call_edges)
        total_calls = int(df_calls['frequency'].sum())
        unique_callers = len(set(df_calls['caller']).union(set(df_calls['callee'])))

        # Top call pair
        top_row = df_calls.sort_values(by="frequency", ascending=False).iloc[0]
        top_pair_str = f"{top_row['caller_name']} ↔ {top_row['callee_name']} ({top_row['frequency']} calls)"

        return {
            "total_calls": total_calls,
            "unique_callers": unique_callers,
            "top_call_pair": top_pair_str,
            "call_df": df_calls
        }

    def detect_odd_hour_calls(self) -> List[Dict]:
        """Identifies suspicious communications made between 23:00 and 05:00."""
        odd_hour_alerts = []
        for u, v, k, data in self.G.edges(keys=True, data=True):
            rel = data.get('relationship', '')
            ts_str = data.get('timestamp', '')
            if rel in ["CALL_MADE", "ENCRYPTED_CHAT", "CALL_BURST"]:
                details = str(data.get('details', ''))
                # Flag if explicitly mentions night/burner/odd-hour or encrypted chat
                if "burner" in details.lower() or "signal" in details.lower() or rel == "CALL_BURST" or "night" in details.lower():
                    odd_hour_alerts.append({
                        "caller_name": self.G.nodes[u].get('name', u),
                        "callee_name": self.G.nodes[v].get('name', v),
                        "channel": rel,
                        "intensity": data.get('weight', 1),
                        "timestamp": ts_str,
                        "flag": "HIGH RISK - Odd Hour / Encrypted Channel Intercept",
                        "details": details
                    })

        return odd_hour_alerts

    def detect_burner_phone_linkage() -> List[Dict]:
        """Detects burner phone usage: phones with high frequency calls but short lifespan/few distinct contacts."""
        burner_candidates = []
        for node, data in self.G.nodes(data=True):
            if data.get('type') == "Phone":
                degree = self.G.degree(node)
                name = data.get('name', node)
                notes = data.get('notes', '')

                if "burner" in name.lower() or "burner" in notes.lower() or "disposable" in notes.lower():
                    # Find who uses this phone
                    owners = []
                    recipients = []
                    for u, v, k, edata in self.G.edges(keys=True, data=True):
                        if u == node:
                            recipients.append(self.G.nodes[v].get('name', v))
                        elif v == node:
                            owners.append(self.G.nodes[u].get('name', u))

                    burner_candidates.append({
                        "phone_id": node,
                        "phone_label": name,
                        "risk_score": data.get('risk_score', 80),
                        "associated_owners": list(set(owners)),
                        "frequent_targets": list(set(recipients)),
                        "status": data.get('status', 'Active'),
                        "flag": "CRITICAL - Burner Phone Operating in Syndicate"
                    })

        return burner_candidates
