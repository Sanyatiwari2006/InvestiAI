"""
Social Media Intelligence (SOCMINT) & Digital Alias Resolution Engine
Cross-references online handles, encrypted chat usernames, darknet personas, and social media footprints.
"""

import pandas as pd
import networkx as nx
from typing import Dict, List

class SocialMediaIntelEngine:
    def __init__(self, G: nx.MultiDiGraph):
        self.G = G

    def resolve_aliases(self) -> List[Dict]:
        """
        Scans graph for Social Media Handle nodes and maps them to suspect master profiles.
        """
        alias_mappings = []
        for node, data in self.G.nodes(data=True):
            if data.get('type') in ["Social Media Handle", "Suspect"]:
                # Find ALIAS_OF or SOCIAL_MENTION edges
                connected_handles = []
                connected_suspects = []

                for u, v, k, edata in self.G.edges(node, keys=True, data=True):
                    other_id = v if u == node else u
                    other_data = self.G.nodes[other_id]

                    if edata.get('relationship') in ["ALIAS_OF", "SOCIAL_MENTION", "OWNERSHIP"]:
                        if other_data.get('type') == "Social Media Handle":
                            connected_handles.append(other_data.get('name', other_id))
                        elif other_data.get('type') == "Suspect":
                            connected_suspects.append(other_data.get('name', other_id))

                if data.get('type') == "Social Media Handle" or connected_handles:
                    alias_mappings.append({
                        "node_id": node,
                        "name": data.get('name', node),
                        "type": data.get('type'),
                        "risk_score": data.get('risk_score', 50),
                        "linked_suspects": list(set(connected_suspects)),
                        "linked_handles": list(set(connected_handles)),
                        "notes": data.get('notes', '')
                    })

        return alias_mappings

    def get_digital_footprint_matrix(self) -> pd.DataFrame:
        """
        Generates a summary matrix of digital personas, Telegram handles, burner lines, and crypto wallets per suspect.
        """
        suspects = [n for n, d in self.G.nodes(data=True) if d.get('type') == "Suspect"]
        records = []

        for s_id in suspects:
            s_name = self.G.nodes[s_id].get('name', s_id)
            phones = []
            wallets = []
            handles = []
            accounts = []

            for u, v, k, edata in self.G.edges(s_id, keys=True, data=True):
                target_id = v if u == s_id else u
                t_data = self.G.nodes[target_id]
                t_type = t_data.get('type')
                t_name = t_data.get('name', target_id)

                if t_type == "Phone":
                    phones.append(t_name)
                elif t_type == "Crypto Wallet":
                    wallets.append(t_name)
                elif t_type == "Social Media Handle":
                    handles.append(t_name)
                elif t_type in ["Bank Account", "Shell Company"]:
                    accounts.append(t_name)

            records.append({
                "Suspect ID": s_id,
                "Suspect Name": s_name,
                "Risk Score": self.G.nodes[s_id].get('risk_score', 50),
                "Burner Phones": ", ".join(phones) if phones else "None Linked",
                "Crypto Wallets": ", ".join(wallets) if wallets else "None Linked",
                "Social Handles": ", ".join(handles) if handles else "None Linked",
                "Bank/Shell Accounts": ", ".join(accounts) if accounts else "None Linked"
            })

        df_footprint = pd.DataFrame(records)
        if not df_footprint.empty:
            df_footprint = df_footprint.sort_values(by="Risk Score", ascending=False)
        return df_footprint
