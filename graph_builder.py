"""
NetworkX MultiGraph Builder & Filtering Engine
"""

import networkx as nx
import pandas as pd
from config import ENTITY_TYPES

class CriminalGraphBuilder:
    def __init__(self, df_nodes: pd.DataFrame, df_edges: pd.DataFrame):
        self.df_nodes = df_nodes
        self.df_edges = df_edges
        self.graph = None
        self.build_graph()

    def build_graph(self):
        """Constructs a NetworkX MultiDiGraph from dataframes."""
        G = nx.MultiDiGraph()

        # Add nodes with metadata
        for _, row in self.df_nodes.iterrows():
            node_id = str(row['id'])
            G.add_node(
                node_id,
                name=row.get('name', node_id),
                type=row.get('type', 'Unknown'),
                risk_score=int(row.get('risk_score', 50)),
                status=row.get('status', 'Active'),
                notes=row.get('notes', '')
            )

        # Add edges with attributes
        for _, row in self.df_edges.iterrows():
            src = str(row['source'])
            dst = str(row['target'])
            
            # Ensure both nodes exist
            if src not in G:
                G.add_node(src, name=src, type="Unknown", risk_score=50, status="Active", notes="")
            if dst not in G:
                G.add_node(dst, name=dst, type="Unknown", risk_score=50, status="Active", notes="")

            G.add_edge(
                src,
                dst,
                relationship=row.get('relationship', 'CONNECTED_TO'),
                weight=float(row.get('weight', 1.0)),
                timestamp=str(row.get('timestamp', '')),
                amount=float(row.get('amount', 0.0)),
                details=str(row.get('details', ''))
            )

        self.graph = G
        return G

    def get_filtered_subgraph(
        self,
        entity_types=None,
        relationship_types=None,
        min_risk=0,
        max_risk=100,
        search_query=""
    ):
        """Returns a filtered NetworkX MultiDiGraph based on criteria."""
        if self.graph is None:
            self.build_graph()

        # Filter nodes
        valid_nodes = set()
        for node, data in self.graph.nodes(data=True):
            n_type = data.get('type', 'Unknown')
            risk = data.get('risk_score', 50)
            name = str(data.get('name', '')).lower()
            n_id = str(node).lower()

            if entity_types and n_type not in entity_types:
                continue
            if not (min_risk <= risk <= max_risk):
                continue
            if search_query:
                q = search_query.lower()
                if q not in name and q not in n_id:
                    continue
            valid_nodes.add(node)

        # Create induced subgraph
        subgraph = self.graph.subgraph(valid_nodes).copy()

        # Filter edges if specified
        if relationship_types:
            edges_to_remove = []
            for u, v, k, data in subgraph.edges(keys=True, data=True):
                if data.get('relationship') not in relationship_types:
                    edges_to_remove.append((u, v, k))
            for u, v, k in edges_to_remove:
                subgraph.remove_edge(u, v, key=k)

        # Clean isolated orphan nodes if needed
        isolated = [node for node, degree in dict(subgraph.degree()).items() if degree == 0]
        # We keep isolated nodes if user explicitly searched for them, else we leave them intact
        return subgraph

    def get_node_dossier(self, node_id: str):
        """Compiles complete intelligence dossier for a given entity node."""
        if node_id not in self.graph:
            return None

        node_data = self.graph.nodes[node_id]
        
        # Incoming and Outgoing Edges
        in_edges = []
        for src, _, data in self.graph.in_edges(node_id, data=True):
            in_edges.append({
                "from_id": src,
                "from_name": self.graph.nodes[src].get('name', src),
                "from_type": self.graph.nodes[src].get('type', 'Unknown'),
                "relationship": data.get('relationship'),
                "amount": data.get('amount'),
                "timestamp": data.get('timestamp'),
                "details": data.get('details')
            })

        out_edges = []
        for _, dst, data in self.graph.out_edges(node_id, data=True):
            out_edges.append({
                "to_id": dst,
                "to_name": self.graph.nodes[dst].get('name', dst),
                "to_type": self.graph.nodes[dst].get('type', 'Unknown'),
                "relationship": data.get('relationship'),
                "amount": data.get('amount'),
                "timestamp": data.get('timestamp'),
                "details": data.get('details')
            })

        # Neighbors
        neighbors = []
        for n in set(list(self.graph.predecessors(node_id)) + list(self.graph.successors(node_id))):
            neighbors.append({
                "id": n,
                "name": self.graph.nodes[n].get('name', n),
                "type": self.graph.nodes[n].get('type', 'Unknown'),
                "risk_score": self.graph.nodes[n].get('risk_score', 0)
            })

        return {
            "id": node_id,
            "metadata": node_data,
            "inbound_connections": in_edges,
            "outbound_connections": out_edges,
            "neighbors": sorted(neighbors, key=lambda x: x['risk_score'], reverse=True)
        }
