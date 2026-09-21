"""
AI-Powered Unstructured Text NLP Entity & Link Extractor Engine
Parses FIRs, Police Reports, Surveillance Transcripts, Intelligence Briefs, and Social Media Posts
"""

import re
import pandas as pd
import random
from typing import Dict, List, Tuple

class NLPEntityExtractor:
    """
    Extracts entities (People, Phones, Bank Accounts, Crypto Wallets, Vehicles, Locations, FIRs, Handles)
    and infer relationships from raw unstructured narrative text.
    """

    # RegEx Patterns for Entity Detection
    PATTERNS = {
        "FIR_INCIDENT": r'\b(FIR-\d{4}-\d{3,5}|FIR\s*#?\s*\d{4,6}|Report\s*#?\s*\d{4,6})\b',
        "PHONE": r'\b(\+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4})\b',
        "BANK_ACC": r'\b(ACC_\d{3,6}|Account\s*#?\s*\d{5,12}|IBAN[A-Z0-9]{12,30})\b',
        "CRYPTO_WALLET": r'\b(0x[a-fA-F0-9]{20,40}|bc1[a-zA-Z0-9]{25,40})\b',
        "VEHICLE": r'\b([A-Z]{2,3}-\d{3,4}|[A-Z]{3}-\d{3,4}|SUV|Sedan|Van|Truck)\b',
        "SOCIAL_HANDLE": r'(@[A-Za-z0-9_]{3,20})\b',
        "SHELL_COMPANY": r'\b([A-Z][a-zA-Z0-9& ]+(?:Holdings|Corp|Ltd|FZE|Inc|Group|Enterprises|Logistics|Trading))\b',
        "LOCATION": r'\b(Warehouse\s*#?\d+|Suite\s*#?\d+|Hotel\s+[A-Z][a-z]+|Cell\ tower\s*#?\d+|Airport|Docklands|Downtown|Tower\s*#?\d+)\b'
    }

    SUSPECT_KEYWORDS = [
        "suspect", "accused", "kingpin", "leader", "associate", "mule", "operator",
        "handler", "courier", "boss", "alias", "target", "person of interest"
    ]

    def __init__(self):
        pass

    def extract_entities_and_relationships(self, raw_text: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Parses raw text, discovers entities, assigns IDs, and links entities that co-occur in the same paragraph/sentence.
        """
        nodes = []
        edges = []
        node_map = {}  # key -> entity metadata

        # Split into sentences / paragraphs for context co-occurrence
        sentences = [s.strip() for s in re.split(r'[\.\n;]', raw_text) if s.strip()]

        entity_counter = 1

        # 1. Extract Named Entities using RegEx and heuristic Rules
        for sentence in sentences:
            found_in_sentence = []

            # Check FIR Incidents
            firs = re.findall(self.PATTERNS["FIR_INCIDENT"], sentence, re.IGNORECASE)
            for fir in firs:
                e_id = f"INC_{hash(fir) % 10000:04d}"
                if e_id not in node_map:
                    node_map[e_id] = {
                        "id": e_id, "name": fir, "type": "Incident",
                        "risk_score": 85, "status": "Under Investigation", "notes": f"Extracted from report text: '{fir}'"
                    }
                found_in_sentence.append(e_id)

            # Check Phones
            phones = re.findall(self.PATTERNS["PHONE"], sentence)
            for ph in phones:
                if len(ph.replace(" ", "").replace("-", "")) >= 7:
                    e_id = f"PHN_{hash(ph) % 10000:04d}"
                    if e_id not in node_map:
                        node_map[e_id] = {
                            "id": e_id, "name": ph, "type": "Phone",
                            "risk_score": 70, "status": "Interception Target", "notes": "Extracted phone number."
                        }
                    found_in_sentence.append(e_id)

            # Check Bank Accounts
            accs = re.findall(self.PATTERNS["BANK_ACC"], sentence, re.IGNORECASE)
            for acc in accs:
                e_id = f"ACC_{hash(acc) % 10000:04d}"
                if e_id not in node_map:
                    node_map[e_id] = {
                        "id": e_id, "name": acc, "type": "Bank Account",
                        "risk_score": 75, "status": "Flagged Account", "notes": "Extracted bank account."
                    }
                found_in_sentence.append(e_id)

            # Check Crypto Wallets
            wallets = re.findall(self.PATTERNS["CRYPTO_WALLET"], sentence)
            for wlt in wallets:
                e_id = f"WLT_{hash(wlt) % 10000:04d}"
                if e_id not in node_map:
                    node_map[e_id] = {
                        "id": e_id, "name": wlt[:10] + "..." + wlt[-4:], "type": "Crypto Wallet",
                        "risk_score": 88, "status": "Tainted Wallet", "notes": f"Full address: {wlt}"
                    }
                found_in_sentence.append(e_id)

            # Check Shell Companies
            companies = re.findall(self.PATTERNS["SHELL_COMPANY"], sentence)
            for comp in companies:
                e_id = f"SHL_{hash(comp) % 10000:04d}"
                if e_id not in node_map:
                    node_map[e_id] = {
                        "id": e_id, "name": comp, "type": "Shell Company",
                        "risk_score": 80, "status": "Audit Required", "notes": "Extracted corporate entity."
                    }
                found_in_sentence.append(e_id)

            # Check Social Media Handles
            handles = re.findall(self.PATTERNS["SOCIAL_HANDLE"], sentence)
            for h in handles:
                e_id = f"SOC_{hash(h) % 10000:04d}"
                if e_id not in node_map:
                    node_map[e_id] = {
                        "id": e_id, "name": h, "type": "Social Media Handle",
                        "risk_score": 65, "status": "SOCMINT Target", "notes": f"Social media handle {h}"
                    }
                found_in_sentence.append(e_id)

            # Check Locations
            locations = re.findall(self.PATTERNS["LOCATION"], sentence, re.IGNORECASE)
            for loc in locations:
                e_id = f"LOC_{hash(loc) % 10000:04d}"
                if e_id not in node_map:
                    node_map[e_id] = {
                        "id": e_id, "name": loc, "type": "Location",
                        "risk_score": 60, "status": "Surveillance Spot", "notes": "Extracted location landmark."
                    }
                found_in_sentence.append(e_id)

            # Extract Suspect Names using Capitalized Name patterns (e.g., Victor Vance, Elena Rostova)
            names = re.findall(r'\b([A-Z][a-z]+\s+[A-Z][a-z]+)\b', sentence)
            for name in names:
                # Exclude common false positives
                if name not in ["Grand Palace", "Cell Tower", "Docklands Warehouse", "Apex Holdings", "BlueWave Logistics", "SilkRoad Trading"]:
                    # Check context keywords for suspect risk bump
                    is_suspect_context = any(kw in sentence.lower() for kw in self.SUSPECT_KEYWORDS)
                    risk = random.randint(75, 95) if is_suspect_context else random.randint(50, 75)
                    
                    e_id = f"PER_{hash(name) % 10000:04d}"
                    if e_id not in node_map:
                        node_map[e_id] = {
                            "id": e_id, "name": name, "type": "Suspect",
                            "risk_score": risk, "status": "Extracted Suspect",
                            "notes": f"Identified in sentence context: '{sentence[:60]}...'"
                        }
                    found_in_sentence.append(e_id)

            # Build Edges for entities co-occurring in the same sentence
            unique_found = list(set(found_in_sentence))
            for i in range(len(unique_found)):
                for j in range(i + 1, len(unique_found)):
                    src = unique_found[i]
                    dst = unique_found[j]

                    # Infer relationship type based on entity types
                    src_type = node_map[src]['type']
                    dst_type = node_map[dst]['type']

                    rel = "ASSOCIATED_WITH"
                    amt = 0
                    
                    # Detect amounts in sentence
                    amt_match = re.search(r'\$\s*([0-9,]+(?:\.[0-9]{2})?)', sentence)
                    if amt_match:
                        try:
                            amt = float(amt_match.group(1).replace(',', ''))
                        except ValueError:
                            amt = 0.0

                    if "Phone" in [src_type, dst_type] and "Phone" in [src_type, dst_type]:
                        rel = "CALL_MADE"
                    elif "Bank Account" in [src_type, dst_type] or "Shell Company" in [src_type, dst_type] or "Crypto Wallet" in [src_type, dst_type]:
                        if amt > 0:
                            rel = "MONEY_TRANSFERRED"
                        elif "Crypto Wallet" in [src_type, dst_type]:
                            rel = "CRYPTO_TRANSFER"
                        else:
                            rel = "SUSPICIOUS_TRANSFER"
                    elif "Suspect" in [src_type, dst_type] and ("Phone" in [src_type, dst_type] or "Bank Account" in [src_type, dst_type] or "Crypto Wallet" in [src_type, dst_type]):
                        rel = "OWNERSHIP"
                    elif "Location" in [src_type, dst_type]:
                        rel = "CO_LOCATION"
                    elif "Social Media Handle" in [src_type, dst_type]:
                        rel = "SOCIAL_MENTION"
                    elif "Incident" in [src_type, dst_type]:
                        rel = "CO_ARREST"

                    edges.append({
                        "source": src,
                        "target": dst,
                        "relationship": rel,
                        "weight": 5,
                        "timestamp": "2026-03-01",
                        "amount": amt,
                        "details": f"NLP Co-occurrence: {sentence[:80]}..."
                    })

        df_nodes = pd.DataFrame(list(node_map.values()))
        df_edges = pd.DataFrame(edges)

        return df_nodes, df_edges
