"""
Graph Intelligence Metrics, Centrality & Community Analytics
"""

import networkx as nx
import pandas as pd
import numpy as np

def compute_graph_metrics(G: nx.Graph):
    """
    Computes graph centralities and metrics for all nodes in graph G.
    Returns a pandas DataFrame sorted by combined risk index.
    """
    if len(G) == 0:
        return pd.DataFrame()

    # Convert MultiDiGraph to simple DiGraph or Graph for standard centrality metrics
    G_simple = nx.Graph(G)

    # 1. Centralities
    degree_cent = nx.degree_centrality(G_simple)
    betweenness_cent = nx.betweenness_centrality(G_simple)
    
    try:
        pagerank_cent = nx.pagerank(G_simple, max_iter=200)
    except Exception:
        pagerank_cent = {n: 0.0 for n in G_simple.nodes()}

    try:
        eigenvector_cent = nx.eigenvector_centrality(G_simple, max_iter=300)
    except Exception:
        eigenvector_cent = {n: 0.0 for n in G_simple.nodes()}

    # 2. Community Detection (Louvain / Greedy Modularity)
    try:
        communities = list(nx.community.greedy_modularity_communities(G_simple))
        community_map = {}
        for comm_id, comm_nodes in enumerate(communities):
            for node in comm_nodes:
                community_map[node] = f"Cell #{comm_id + 1}"
    except Exception:
        community_map = {node: "Cell #1" for node in G_simple.nodes()}

    # 3. Dynamic Composite AI Risk Computation
    records = []
    for node in G.nodes():
        node_data = G.nodes[node]
        base_risk = float(node_data.get('risk_score', 50))
        
        deg = degree_cent.get(node, 0.0)
        bet = betweenness_cent.get(node, 0.0)
        pr = pagerank_cent.get(node, 0.0)
        eig = eigenvector_cent.get(node, 0.0)
        cell = community_map.get(node, "Unclustered")

        # Dynamic AI Risk Boost Formula
        # High betweenness + High Base Risk boost score
        dynamic_risk = min(100, int(base_risk * 0.6 + bet * 100 * 0.25 + pr * 100 * 0.15))

        records.append({
            "id": node,
            "name": node_data.get('name', node),
            "type": node_data.get('type', 'Unknown'),
            "status": node_data.get('status', 'Active'),
            "base_risk": base_risk,
            "ai_risk_score": dynamic_risk,
            "betweenness": round(bet, 4),
            "pagerank": round(pr, 4),
            "degree": round(deg, 4),
            "eigenvector": round(eig, 4),
            "gang_community": cell
        })

    df_metrics = pd.DataFrame(records)
    if not df_metrics.empty:
        df_metrics = df_metrics.sort_values(by="ai_risk_score", ascending=False).reset_index(drop=True)

    return df_metrics
