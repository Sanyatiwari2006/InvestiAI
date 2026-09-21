"""
PyVis Interactive Network Graph Renderer for Streamlit
"""

import pyvis.network as net
import networkx as nx
from config import ENTITY_TYPES, EDGE_COLORS
import tempfile
import os

def render_pyvis_graph(
    G: nx.MultiDiGraph,
    height="750px",
    width="100%",
    physics_solver="forceAtlas2Based",
    selected_node_id=None
):
    """
    Renders NetworkX MultiDiGraph as an interactive PyVis HTML widget.
    Returns path to temporary HTML file or HTML string for Streamlit embedding.
    """
    pyvis_net = net.Network(
        height=height,
        width=width,
        directed=True,
        notebook=False,
        bgcolor="#111827",  # Dark criminal command center background
        font_color="#FFFFFF"
    )

    # Configure physics
    if physics_solver == "forceAtlas2Based":
        pyvis_net.force_atlas_2based(
            gravity=-60,
            central_gravity=0.015,
            spring_length=120,
            spring_strength=0.08,
            damping=0.4
        )
    elif physics_solver == "barnesHut":
        pyvis_net.barnes_hut(gravity=-3000, central_gravity=0.2, spring_length=150)
    elif physics_solver == "hierarchical":
        pyvis_net.hhierarchical_repulsion(central_gravity=0.0, spring_length=100)

    # Add Nodes
    for node, data in G.nodes(data=True):
        n_type = data.get('type', 'Unknown')
        style = ENTITY_TYPES.get(n_type, {"color": "#999999", "shape": "dot", "icon": "❓"})
        
        name = data.get('name', str(node))
        risk = data.get('risk_score', 50)
        status = data.get('status', 'Active')
        notes = data.get('notes', '')

        # Size scales with risk score
        size = 15 + (risk / 100.0) * 25
        
        # Color highlight for selected node
        color = style['color']
        border_color = "#FFFFFF"
        if selected_node_id and str(node) == str(selected_node_id):
            border_color = "#FFFF00"
            size += 15

        # Custom HTML Tooltip
        tooltip_html = f"""
        <div style="font-family: Arial; padding: 10px; background-color: #1E293B; color: #F8FAFC; border-radius: 8px; border: 1px solid #475569; width: 220px;">
            <div style="font-weight: bold; font-size: 14px; border-bottom: 1px solid #475569; padding-bottom: 4px; margin-bottom: 6px;">
                {style['icon']} {name}
            </div>
            <div><b>Type:</b> {n_type}</div>
            <div><b>ID:</b> <code style="color: #38BDF8;">{node}</code></div>
            <div><b>Risk Score:</b> <span style="color: {'#EF4444' if risk >= 75 else '#F59E0B' if risk >= 50 else '#10B981'}; font-weight: bold;">{risk}/100</span></div>
            <div><b>Status:</b> {status}</div>
            {f'<div style="margin-top: 6px; font-style: italic; color: #94A3B8; font-size: 11px;">"{notes}"</div>' if notes else ''}
        </div>
        """

        pyvis_net.add_node(
            str(node),
            label=f"{style['icon']} {name}",
            title=tooltip_html,
            color={"background": color, "border": border_color, "highlight": {"background": "#FF0000", "border": "#FFFFFF"}},
            shape=style['shape'],
            size=size,
            borderWidth=2 if selected_node_id and str(node) == str(selected_node_id) else 1,
            font={"color": "#FFFFFF", "size": 12, "face": "Courier New"}
        )

    # Add Edges
    for u, v, k, data in G.edges(keys=True, data=True):
        rel = data.get('relationship', 'CONNECTED_TO')
        amt = data.get('amount', 0)
        edge_color = EDGE_COLORS.get(rel, "#64748B")
        weight = float(data.get('weight', 1.0))

        label_text = rel
        if amt > 0:
            label_text += f" (${amt:,.0f})"

        edge_tooltip = f"""
        <div style="font-family: Arial; padding: 8px; background: #0F172A; color: #F8FAFC; border-radius: 6px; border: 1px solid #334155;">
            <div style="font-weight: bold; color: {edge_color};">{rel}</div>
            {f'<div>Amount: <b>${amt:,.2f}</b></div>' if amt > 0 else ''}
            <div>Timestamp: {data.get('timestamp', 'N/A')}</div>
            <div>Details: {data.get('details', 'N/A')}</div>
        </div>
        """

        pyvis_net.add_edge(
            str(u),
            str(v),
            title=edge_tooltip,
            label=label_text if amt > 0 else "",
            color=edge_color,
            width=max(1, min(weight, 6)),
            arrows="to",
            smooth={"type": "curvedCW", "roundness": 0.15}
        )

    # Export to HTML file
    tmp_dir = tempfile.gettempdir()
    html_path = os.path.join(tmp_dir, "nexus_graph.html")
    pyvis_net.save_graph(html_path)

    with open(html_path, "r", encoding="utf-8") as f:
        html_code = f.read()

    return html_code
