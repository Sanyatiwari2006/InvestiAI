"""
Plotly Temporal Sequence & Timeline Visualization
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import networkx as nx

def render_event_timeline(G: nx.MultiDiGraph):
    """
    Generates a Plotly scatter timeline chart for edge events in G.
    """
    events = []
    for u, v, k, data in G.edges(keys=True, data=True):
        ts = data.get('timestamp', '')
        if ts:
            src_name = G.nodes[u].get('name', u)
            dst_name = G.nodes[v].get('name', v)
            rel = data.get('relationship', 'EVENT')
            amt = data.get('amount', 0)
            details = data.get('details', '')

            events.append({
                "Timestamp": ts,
                "Event": f"{src_name} → {dst_name}",
                "Relationship": rel,
                "Amount": amt,
                "Source": src_name,
                "Target": dst_name,
                "Details": details
            })

    if not events:
        fig = go.Figure()
        fig.update_layout(
            title="No Timestamps Available in Current Subgraph",
            template="plotly_dark"
        )
        return fig

    df_ev = pd.DataFrame(events)
    df_ev['Timestamp'] = pd.to_datetime(df_ev['Timestamp'])
    df_ev = df_ev.sort_values(by="Timestamp")

    fig = px.scatter(
        df_ev,
        x="Timestamp",
        y="Event",
        color="Relationship",
        size=df_ev['Amount'].apply(lambda x: max(10, min(50, x / 10000))) if (df_ev['Amount'] > 0).any() else None,
        hover_data=["Source", "Target", "Amount", "Details"],
        title="Chronological Investigation Event Sequence Timeline",
        template="plotly_dark",
        height=500
    )

    fig.update_layout(
        xaxis_title="Timeline Date",
        yaxis_title="Entity Interaction Pair",
        hoverlabel=dict(bgcolor="#1E293B", font_size=12),
        font=dict(color="#F8FAFC")
    )

    return fig
