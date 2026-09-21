"""
Automated Criminal Pattern & Anomaly Discovery Engine
"""

import networkx as nx
import pandas as pd

class PatternDetector:
    def __init__(self, G: nx.MultiDiGraph):
        self.G = G

    def detect_circular_money_trails(self, min_cycle_len=3, max_cycle_len=6):
        """
        Detects directed cycles in money transfers & crypto transactions
        indicative of Hawala or laundering loops (e.g. A -> B -> C -> D -> A).
        """
        # Create a directed graph with only money/crypto edges
        money_G = nx.DiGraph()
        for u, v, k, data in self.G.edges(keys=True, data=True):
            rel = data.get('relationship', '')
            if rel in ["MONEY_TRANSFERRED", "CRYPTO_TRANSFER"]:
                amt = data.get('amount', 0)
                if money_G.has_edge(u, v):
                    money_G[u][v]['total_amount'] += amt
                else:
                    money_G.add_edge(u, v, total_amount=amt, relationship=rel)

        # Simple cycles detection
        try:
            raw_cycles = list(nx.simple_cycles(money_G))
        except Exception:
            raw_cycles = []

        detected_loops = []
        for cycle in raw_cycles:
            if min_cycle_len <= len(cycle) <= max_cycle_len:
                # Reconstruct path details
                path_details = []
                total_loop_volume = 0
                for i in range(len(cycle)):
                    src = cycle[i]
                    dst = cycle[(i + 1) % len(cycle)]
                    edge_data = money_G.get_edge_data(src, dst, default={})
                    amt = edge_data.get('total_amount', 0)
                    total_loop_volume += amt
                    path_details.append({
                        "from": self.G.nodes[src].get('name', src),
                        "to": self.G.nodes[dst].get('name', dst),
                        "amount": amt,
                        "rel": edge_data.get('relationship', 'TRANSFER')
                    })

                cycle_names = [self.G.nodes[n].get('name', n) for n in cycle]
                detected_loops.append({
                    "cycle_nodes": cycle,
                    "cycle_names": cycle_names,
                    "length": len(cycle),
                    "total_volume": total_loop_volume,
                    "transfers": path_details,
                    "risk_flag": "CRITICAL - Money Laundering Loop Detected"
                })

        # Sort loops by total volume
        detected_loops.sort(key=lambda x: x['total_volume'], reverse=True)
        return detected_loops

    def detect_smurfing_structuring(self, threshold_count=3, max_tx_amount=10000):
        """
        Identifies destination bank/crypto accounts receiving multiple small
        transfers (smurfing/structuring) from disparate sources.
        """
        dest_accounts = {}
        for u, v, k, data in self.G.edges(keys=True, data=True):
            rel = data.get('relationship', '')
            amt = data.get('amount', 0)
            if rel in ["MONEY_TRANSFERRED", "CRYPTO_TRANSFER"] and 0 < amt <= max_tx_amount:
                if v not in dest_accounts:
                    dest_accounts[v] = []
                dest_accounts[v].append({
                    "from_id": u,
                    "from_name": self.G.nodes[u].get('name', u),
                    "amount": amt,
                    "timestamp": data.get('timestamp', ''),
                    "details": data.get('details', '')
                })

        smurfing_alerts = []
        for acc_id, tx_list in dest_accounts.items():
            if len(tx_list) >= threshold_count:
                total_smurfed = sum(t['amount'] for t in tx_list)
                acc_name = self.G.nodes[acc_id].get('name', acc_id)
                acc_type = self.G.nodes[acc_id].get('type', 'Account')
                smurfing_alerts.append({
                    "account_id": acc_id,
                    "account_name": acc_name,
                    "account_type": acc_type,
                    "tx_count": len(tx_list),
                    "total_structured_amount": total_smurfed,
                    "incoming_sources": tx_list,
                    "risk_flag": "HIGH - Smurfing / Structuring Pattern Detected"
                })

        smurfing_alerts.sort(key=lambda x: x['total_structured_amount'], reverse=True)
        return smurfing_alerts

    def detect_hidden_kingpin(self):
        """
        Identifies potential hidden kingpins: nodes with high base risk or betweenness,
        communicating via encrypted channels/burners, but insulated from direct money transfers.
        """
        G_simple = nx.Graph(self.G)
        if len(G_simple) == 0:
            return []

        betweenness = nx.betweenness_centrality(G_simple)
        kingpin_candidates = []

        for node, data in self.G.nodes(data=True):
            if data.get('type') != "Suspect":
                continue

            # Check if suspect has money transfers attached to them directly
            direct_financial = False
            for u, v, k, edata in self.G.edges(node, keys=True, data=True):
                if edata.get('relationship') in ["MONEY_TRANSFERRED", "CRYPTO_TRANSFER"]:
                    direct_financial = True
                    break

            bet_score = betweenness.get(node, 0)
            base_risk = data.get('risk_score', 0)

            # High risk or high betweenness + insulated from direct financial transfers
            if (base_risk >= 75 or bet_score > 0.1) and not direct_financial:
                # Count burner / encrypted chat links
                encrypted_links = 0
                for u, v, k, edata in self.G.edges(node, keys=True, data=True):
                    if edata.get('relationship') in ["ENCRYPTED_CHAT", "CALL_MADE"]:
                        encrypted_links += 1

                kingpin_candidates.append({
                    "id": node,
                    "name": data.get('name', node),
                    "status": data.get('status', ''),
                    "risk_score": base_risk,
                    "betweenness": round(bet_score, 4),
                    "encrypted_comm_links": encrypted_links,
                    "financial_insulation": "Fully Insulated (No Direct Bank Edges)",
                    "recommendation": "Target for wiretap & secondary buffer analysis."
                })

        kingpin_candidates.sort(key=lambda x: x['betweenness'], reverse=True)
        return kingpin_candidates

    def detect_colocation_hotspots(self):
        """
        Finds locations/events where 2 or more high-risk suspects were logged together.
        """
        location_map = {}
        for u, v, k, data in self.G.edges(keys=True, data=True):
            rel = data.get('relationship', '')
            if rel in ["CO_LOCATION", "VEHICLE_TRACKED"]:
                # Check which one is the location or incident node
                target_node = v if self.G.nodes[v].get('type') in ["Location", "Incident"] else u
                suspect_node = u if target_node == v else v

                if target_node not in location_map:
                    location_map[target_node] = []
                location_map[target_node].append({
                    "entity_id": suspect_node,
                    "entity_name": self.G.nodes[suspect_node].get('name', suspect_node),
                    "entity_type": self.G.nodes[suspect_node].get('type', 'Unknown'),
                    "timestamp": data.get('timestamp', ''),
                    "details": data.get('details', '')
                })

        hotspots = []
        for loc_id, presences in location_map.items():
            if len(presences) >= 2:
                loc_name = self.G.nodes[loc_id].get('name', loc_id)
                loc_type = self.G.nodes[loc_id].get('type', 'Location')
                hotspots.append({
                    "location_id": loc_id,
                    "location_name": loc_name,
                    "location_type": loc_type,
                    "co_located_count": len(presences),
                    "entities_present": presences,
                    "risk_flag": "SUSPICIOUS CO-PRESENCE / MEETING SPOT"
                })

        hotspots.sort(key=lambda x: x['co_located_count'], reverse=True)
        return hotspots

    def detect_call_burst_anomalies(self):
        """
        Identifies pairs of entities exhibiting intense burst communication (high edge weight).
        """
        bursts = []
        for u, v, k, data in self.G.edges(keys=True, data=True):
            rel = data.get('relationship', '')
            weight = float(data.get('weight', 1))
            if (rel in ["CALL_MADE", "ENCRYPTED_CHAT", "CALL_BURST"]) and weight >= 15:
                bursts.append({
                    "caller_id": u,
                    "caller_name": self.G.nodes[u].get('name', u),
                    "callee_id": v,
                    "callee_name": self.G.nodes[v].get('name', v),
                    "call_frequency": int(weight),
                    "relationship": rel,
                    "timestamp": data.get('timestamp', ''),
                    "risk_flag": "HIGH - Communication Burst Anomaly Detected"
                })

        bursts.sort(key=lambda x: x['call_frequency'], reverse=True)
        return bursts

    def detect_burner_phone_rotation(self):
        """
        Detects suspects associated with multiple temporary burner phones or rapid line switching.
        """
        suspect_phones = {}
        for u, v, k, data in self.G.edges(keys=True, data=True):
            if data.get('relationship') == "OWNERSHIP":
                if self.G.nodes[u].get('type') == "Suspect" and self.G.nodes[v].get('type') == "Phone":
                    if u not in suspect_phones:
                        suspect_phones[u] = []
                    suspect_phones[u].append(self.G.nodes[v].get('name', v))

        burner_alerts = []
        for s_id, phone_list in suspect_phones.items():
            if len(phone_list) >= 2:
                burner_alerts.append({
                    "suspect_id": s_id,
                    "suspect_name": self.G.nodes[s_id].get('name', s_id),
                    "phone_count": len(phone_list),
                    "phones": phone_list,
                    "risk_flag": "CRITICAL - Active Burner Line Rotation Pattern"
                })

        burner_alerts.sort(key=lambda x: x['phone_count'], reverse=True)
        return burner_alerts

