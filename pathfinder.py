"""
Pathfinder & Multi-Hop Link Analysis Engine
"""

import networkx as nx

class PathfinderEngine:
    def __init__(self, G: nx.MultiDiGraph):
        self.G = G
        self.undirected_G = nx.Graph(G)

    def find_shortest_paths(self, source_id: str, target_id: str, max_depth=5):
        """
        Finds shortest connection paths between two entities.
        """
        if source_id not in self.undirected_G or target_id not in self.undirected_G:
            return {"status": "NOT_FOUND", "message": "Source or Target entity not in graph.", "paths": []}

        if source_id == target_id:
            return {"status": "SAME_NODE", "message": "Source and Target are the same entity.", "paths": []}

        try:
            # All shortest paths
            all_paths = list(nx.all_shortest_paths(self.undirected_G, source=source_id, target=target_id))
        except nx.NetworkXNoPath:
            return {"status": "NO_PATH", "message": f"No network path exists between {source_id} and {target_id}.", "paths": []}
        except Exception as e:
            return {"status": "ERROR", "message": str(e), "paths": []}

        formatted_paths = []
        for path in all_paths:
            if len(path) - 1 > max_depth:
                continue

            steps = []
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]
                
                # Fetch relationship details from multi-graph edges
                edge_attrs = []
                if self.G.has_edge(u, v):
                    for k, data in self.G[u][v].items():
                        edge_attrs.append(f"{data.get('relationship')} (${data.get('amount', 0):,.0f})" if data.get('amount') else data.get('relationship'))
                if self.G.has_edge(v, u):
                    for k, data in self.G[v][u].items():
                        edge_attrs.append(f"REVERSE: {data.get('relationship')}")

                steps.append({
                    "hop": i + 1,
                    "from_id": u,
                    "from_name": self.G.nodes[u].get('name', u),
                    "from_type": self.G.nodes[u].get('type', 'Unknown'),
                    "to_id": v,
                    "to_name": self.G.nodes[v].get('name', v),
                    "to_type": self.G.nodes[v].get('type', 'Unknown'),
                    "relationships": ", ".join(edge_attrs) if edge_attrs else "CONNECTED"
                })

            path_names = [self.G.nodes[n].get('name', n) for n in path]
            formatted_paths.append({
                "path_nodes": path,
                "path_names": path_names,
                "hop_count": len(path) - 1,
                "steps": steps
            })

        return {
            "status": "SUCCESS",
            "path_count": len(formatted_paths),
            "paths": formatted_paths
        }
