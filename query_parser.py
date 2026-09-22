"""
Natural Language Query Engine over Criminal Knowledge Graph
"""

import networkx as nx
from pattern_detector import PatternDetector
from pathfinder import PathfinderEngine
from metrics import compute_graph_metrics

class InvestiAIQueryEngine:
    def __init__(self, G: nx.MultiDiGraph):
        self.G = G
        self.detector = PatternDetector(G)
        self.pathfinder = PathfinderEngine(G)

    def answer_query(self, query: str):
        """
        Parses NL query, maps to graph analytics modules, and produces structured answer.
        """
        q = query.lower().strip()

        # 1. KINGPIN / LEADERSHIP QUERY
        if any(w in q for w in ["kingpin", "leader", "boss", "spectre", "puppet master", "head"]):
            kingpins = self.detector.detect_hidden_kingpin()
            if kingpins:
                top_k = kingpins[0]
                return {
                    "intent": "KINGPIN_IDENTIFICATION",
                    "title": f"🚨 Primary Kingpin Candidate Identified: {top_k['name']}",
                    "summary": f"Entity **{top_k['name']}** holds a Betweenness Centrality of `{top_k['betweenness']}` and Base Risk of `{top_k['risk_score']}`. The entity operates through encrypted communications while maintaining strict financial insulation.",
                    "data": kingpins,
                    "action": "Initiate priority intercept orders on encrypted burner line PHN_001 and request offshore bank records for Apex Holdings."
                }
            else:
                return {
                    "intent": "KINGPIN_IDENTIFICATION",
                    "title": "Kingpin Search Result",
                    "summary": "No isolated high-betweenness suspect was detected in the active subgraph filter.",
                    "data": [],
                    "action": "Broaden the risk score range in the Workbench filters."
                }

        # 2. MONEY LAUNDERING / CIRCULAR TRAIL QUERY
        elif any(w in q for w in ["money laundering", "circular", "loop", "hawala", "cycle"]):
            loops = self.detector.detect_circular_money_trails()
            if loops:
                top_loop = loops[0]
                loop_chain = " → ".join(top_loop['cycle_names'])
                return {
                    "intent": "CIRCULAR_MONEY_TRAIL",
                    "title": f"💸 Money Laundering Cycle Detected (${top_loop['total_volume']:,.2f} Total)",
                    "summary": f"Detected a closed money loop across `{top_loop['length']}` nodes: **{loop_chain} → {top_loop['cycle_names'][0]}**.",
                    "data": loops,
                    "action": "Issue freezing orders under Anti-Money Laundering (AML) statutes for Apex Holdings and BlueWave Logistics."
                }
            else:
                return {
                    "intent": "CIRCULAR_MONEY_TRAIL",
                    "title": "Money Laundering Loop Search",
                    "summary": "No closed circular transaction loops found in the currently loaded financial graph.",
                    "data": [],
                    "action": "Check for smurfing/structuring patterns instead."
                }

        # 3. SMURFING / STRUCTURING QUERY
        elif any(w in q for w in ["smurf", "structuring", "micro", "10,000", "10000", "mule"]):
            smurfs = self.detector.detect_smurfing_structuring()
            if smurfs:
                top_s = smurfs[0]
                return {
                    "intent": "SMURFING_DETECTION",
                    "title": f"🏦 Smurfing / Structuring Alert: {top_s['account_name']}",
                    "summary": f"Account **{top_s['account_name']}** received `{top_s['tx_count']}` distinct transactions under the $10,000 threshold totaling **${top_s['total_structured_amount']:,.2f}**.",
                    "data": smurfs,
                    "action": "Subpoena bank records for all incoming straw account holders."
                }
            else:
                return {
                    "intent": "SMURFING_DETECTION",
                    "title": "Smurfing Search",
                    "summary": "No multi-source structured transactions under $10k detected.",
                    "data": [],
                    "action": "Review general transfer lists."
                }

        # 4. HIGH RISK / SUSPECT QUERY
        elif any(w in q for w in ["high risk", "top suspect", "dangerous", "score"]):
            df_m = compute_graph_metrics(self.G)
            if not df_m.empty:
                top_3 = df_m.head(3).to_dict(orient="records")
                names = ", ".join([f"**{r['name']}** (Score: {r['ai_risk_score']})" for r in top_3])
                return {
                    "intent": "HIGH_RISK_SUSPECTS",
                    "title": "🔥 Top High-Risk Entities in Network",
                    "summary": f"Highest AI Risk Entities: {names}.",
                    "data": top_3,
                    "action": "Cross-reference vehicle registration and cell tower co-location logs for these entities."
                }

        # 5. CO-LOCATION / MEETING QUERY
        elif any(w in q for w in ["meeting", "location", "colocation", "co-location", "tower", "warehouse"]):
            hotspots = self.detector.detect_colocation_hotspots()
            if hotspots:
                top_h = hotspots[0]
                return {
                    "intent": "COLOCATION_HOTSPOT",
                    "title": f"📍 Suspicious Meeting Spot Identified: {top_h['location_name']}",
                    "summary": f"Co-presence of `{top_h['co_located_count']}` suspects/vehicles detected at **{top_h['location_name']}**.",
                    "data": hotspots,
                    "action": "Request CCTV footage and cell tower dump files surrounding the location timestamp."
                }

        # 6. CDR & BURNER PHONE QUERY
        elif any(w in q for w in ["burner", "cdr", "call", "burst", "intercept", "phone"]):
            burners = self.detector.detect_burner_phone_rotation()
            bursts = self.detector.detect_call_burst_anomalies()
            if burners or bursts:
                b_cnt = len(burners)
                return {
                    "intent": "CDR_BURNER_INTELLIGENCE",
                    "title": "📱 Call Detail Record (CDR) & Burner Rotation Flagged",
                    "summary": f"Identified `{b_cnt}` suspect(s) actively rotating burner lines and `{len(bursts)}` high-frequency call burst anomalies.",
                    "data": {"burners": burners, "call_bursts": bursts},
                    "action": "Obtain emergency wiretap authorizations for flagged burner IMEIs."
                }

        # 7. SOCIAL MEDIA & ALIAS QUERY
        elif any(w in q for w in ["social", "telegram", "alias", "handle", "osint", "twitter"]):
            handles = [d for n, d in self.G.nodes(data=True) if d.get('type') == "Social Media Handle"]
            return {
                "intent": "SOCIAL_MEDIA_INTELLIGENCE",
                "title": f"🌐 Social Media & Digital Alias Intelligence ({len(handles)} Handles)",
                "summary": f"Found `{len(handles)}` digital handles linked across encrypted platforms, Telegram, and social networks.",
                "data": handles,
                "action": "Perform digital footprint correlation across cross-platform OSINT databases."
            }


        # DEFAULT FALLBACK
        df_metrics = compute_graph_metrics(self.G)
        return {
            "intent": "GENERAL_EXPLORATION",
            "title": f"🔍 Investigative Graph Summary ({len(self.G.nodes())} Nodes, {len(self.G.edges())} Connections)",
            "summary": f"Processed active network containing `{len(self.G.nodes())}` entities and `{len(self.G.edges())}` multi-modal connections. Try asking about 'kingpin', 'money laundering', 'smurfing', or 'high risk suspects'.",
            "data": df_metrics.head(5).to_dict(orient="records") if not df_metrics.empty else [],
            "action": "Use the Workbench tabs to explore specific subgraphs."
        }
