"""
Folium Geospatial Map Viewer for Suspect Movements & Crime Locations
"""

import folium
from folium.plugins import MarkerCluster
import networkx as nx

def render_geospatial_map(G: nx.MultiDiGraph):
    """
    Renders Folium map showing Location and Incident nodes with connected suspect routes.
    """
    # Define realistic default coordinates (e.g. Metro Police Jurisdiction)
    base_lat, base_lon = 28.6139, 77.2090  # Default Delhi / Capital Metro coordinates

    # Map mock coordinates for locations
    location_coords = {
        "LOC_001": {"lat": 28.6250, "lon": 77.2180, "title": "Docklands Warehouse #14 (Raid Site)"},
        "LOC_002": {"lat": 28.6010, "lon": 77.2250, "title": "Grand Palace Hotel Suite 804"},
        "LOC_003": {"lat": 28.6180, "lon": 77.2000, "title": "Cell Tower #409 (Downtown Financial)"},
        "INC_001": {"lat": 28.6300, "lon": 77.2050, "title": "FIR-2025-0899 (Seizure Site)"},
        "INC_002": {"lat": 28.6252, "lon": 77.2182, "title": "FIR-2026-0104 (Customs Bust Site)"},
    }

    m = folium.Map(
        location=[base_lat, base_lon],
        zoom_start=13,
        tiles="CartoDB dark_matter"
    )

    marker_cluster = MarkerCluster().add_to(m)

    # Add Location & Incident markers
    for node, data in G.nodes(data=True):
        n_type = data.get('type')
        if n_type in ["Location", "Incident"] or node in location_coords:
            coord_info = location_coords.get(node, {
                "lat": base_lat + (hash(node) % 100) * 0.0005,
                "lon": base_lon + (hash(node) % 100) * 0.0005,
                "title": data.get('name', node)
            })

            icon_color = "red" if n_type == "Incident" else "orange" if data.get('risk_score', 0) >= 80 else "blue"
            icon_symbol = "exclamation-triangle" if n_type == "Incident" else "building"

            # Find connected suspects
            connected_suspects = []
            for u, v, k, edata in G.edges(keys=True, data=True):
                if u == node or v == node:
                    other_id = v if u == node else u
                    other_name = G.nodes[other_id].get('name', other_id)
                    connected_suspects.append(f"{other_name} ({edata.get('relationship')})")

            popup_html = f"""
            <div style="font-family: Arial; width: 200px;">
                <h4 style="margin: 0; color: #DC2626;">{coord_info['title']}</h4>
                <p><b>Type:</b> {n_type}</p>
                <p><b>Risk Score:</b> {data.get('risk_score', 50)}</p>
                <p><b>Connected Entities:</b><br/>{', '.join(connected_suspects[:3]) if connected_suspects else 'None'}</p>
            </div>
            """

            folium.Marker(
                location=[coord_info['lat'], coord_info['lon']],
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=coord_info['title'],
                icon=folium.Icon(color=icon_color, icon=icon_symbol, prefix="fa")
            ).add_to(marker_cluster)

    return m
