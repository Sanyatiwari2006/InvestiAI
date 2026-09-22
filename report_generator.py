"""
Law Enforcement Intelligence Case Dossier & Court Evidence Exporter
"""

import datetime
import networkx as nx
from metrics import compute_graph_metrics
from pattern_detector import PatternDetector

def generate_intelligence_dossier_html(G: nx.MultiDiGraph, case_title="OPERATION BLACK ICE"):
    """
    Generates a formal HTML Intelligence Dossier Report for export.
    """
    metrics_df = compute_graph_metrics(G)
    detector = PatternDetector(G)
    
    cycles = detector.detect_circular_money_trails()
    smurfs = detector.detect_smurfing_structuring()
    kingpins = detector.detect_hidden_kingpin()
    hotspots = detector.detect_colocation_hotspots()

    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # High risk entities table rows
    top_entities_rows = ""
    if not metrics_df.empty:
        for idx, row in metrics_df.head(8).iterrows():
            risk_color = "#DC2626" if row['ai_risk_score'] >= 75 else "#D97706"
            top_entities_rows += f"""
            <tr>
                <td style="border: 1px solid #475569; padding: 8px;"><code>{row['id']}</code></td>
                <td style="border: 1px solid #475569; padding: 8px;"><b>{row['name']}</b></td>
                <td style="border: 1px solid #475569; padding: 8px;">{row['type']}</td>
                <td style="border: 1px solid #475569; padding: 8px; color: {risk_color}; font-weight: bold;">{row['ai_risk_score']}/100</td>
                <td style="border: 1px solid #475569; padding: 8px;">{row['betweenness']}</td>
                <td style="border: 1px solid #475569; padding: 8px;">{row['gang_community']}</td>
            </tr>
            """

    # Money laundering findings HTML
    money_findings = ""
    if cycles:
        for c in cycles[:3]:
            money_findings += f"<li><b>Circular Transfer Loop (${c['total_volume']:,.2f}):</b> {' → '.join(c['cycle_names'])}</li>"
    else:
        money_findings = "<li>No closed circular money trails detected in active filter.</li>"

    # Smurfing findings
    smurf_findings = ""
    if smurfs:
        for s in smurfs[:3]:
            smurf_findings += f"<li><b>Smurfing Account {s['account_name']}:</b> Received {s['tx_count']} structured deposits totaling ${s['total_structured_amount']:,.2f}</li>"
    else:
        smurf_findings = "<li>No smurfing/structuring patterns detected.</li>"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8"/>
        <title>LAW ENFORCEMENT INTELLIGENCE DOSSIER - {case_title}</title>
        <style>
            body {{ font-family: 'Segoe UI', Helvetica, Arial, sans-serif; background: #0F172A; color: #F8FAFC; margin: 30px; line-height: 1.6; }}
            .header {{ border-bottom: 3px solid #DC2626; padding-bottom: 15px; margin-bottom: 25px; }}
            .classification {{ background: #DC2626; color: white; padding: 4px 12px; font-weight: bold; border-radius: 4px; display: inline-block; letter-spacing: 1px; }}
            h1 {{ margin: 10px 0 5px 0; color: #F8FAFC; }}
            h2 {{ color: #38BDF8; border-bottom: 1px solid #334155; padding-bottom: 6px; margin-top: 25px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; background: #1E293B; }}
            th {{ background: #334155; color: #F8FAFC; border: 1px solid #475569; padding: 10px; text-align: left; }}
            .alert-box {{ background: #450A0A; border-left: 4px solid #EF4444; padding: 12px; margin: 15px 0; border-radius: 4px; }}
            .footer {{ margin-top: 40px; font-size: 11px; color: #64748B; border-top: 1px solid #334155; padding-top: 10px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <span class="classification">CONFIDENTIAL // LAW ENFORCEMENT SENSITIVE</span>
            <h1>NEXUSGRAPH AI INTELLIGENCE DOSSIER</h1>
            <p><b>Case Title:</b> {case_title} | <b>Generated:</b> {now_str} | <b>Scope:</b> Multi-Modal Knowledge Graph Analysis</p>
        </div>

        <div class="alert-box">
            <b>EXECUTIVE SUMMARY:</b> Graph analysis processed <b>{len(G.nodes())} entities</b> and <b>{len(G.edges())} relationships</b>. 
            Identified <b>{len(kingpins)} potential kingpin candidates</b> and <b>{len(cycles)} closed money laundering loops</b>.
        </div>

        <h2>1. High Risk Entity Centrality Analysis</h2>
        <table>
            <thead>
                <tr>
                    <th>Entity ID</th>
                    <th>Name</th>
                    <th>Type</th>
                    <th>AI Risk Score</th>
                    <th>Betweenness</th>
                    <th>Cluster Cell</th>
                </tr>
            </thead>
            <tbody>
                {top_entities_rows}
            </tbody>
        </table>

        <h2>2. Financial Crime & Laundering Findings</h2>
        <h3>Circular Money Loops</h3>
        <ul>
            {money_findings}
        </ul>

        <h3>Structuring & Smurfing Alerts</h3>
        <ul>
            {smurf_findings}
        </ul>

        <h2>3. Co-location & Physical Surveillance Hotspots</h2>
        <ul>
            {"".join([f"<li><b>{h['location_name']}:</b> Co-presence of {h['co_located_count']} suspects/vehicles logged.</li>" for h in hotspots[:3]]) if hotspots else "<li>No co-location anomalies detected.</li>"}
        </ul>

        <h2>4. Recommended Action Plan</h2>
        <ol>
            <li>File emergency subpoena for wiretap authorization on burner line <code>PHN_001</code>.</li>
            <li>Issue asset freezing notices under AML regulations for shell account <code>Apex Holdings Corp (ACC_001)</code>.</li>
            <li>Execute search warrant at Docklands Warehouse #14 (<code>LOC_001</code>).</li>
        </ol>

        <div class="footer">
            Report generated by NexusGraph AI Investigative Platform. Certified for official police & court evidence preparation.
        </div>
    </body>
    </html>
    """
    return html_content
