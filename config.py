"""
NexusGraph AI Configuration & Schema Definitions
"""

import os

# Entity Types & Visual Styles
ENTITY_TYPES = {
    "Suspect": {"color": "#FF4B4B", "shape": "dot", "icon": "👤", "label_prefix": "Suspect"},
    "Phone": {"color": "#36A2EB", "shape": "dot", "icon": "📱", "label_prefix": "Phone"},
    "Bank Account": {"color": "#4BC0C0", "shape": "dot", "icon": "🏦", "label_prefix": "Acc"},
    "Shell Company": {"color": "#9966FF", "shape": "diamond", "icon": "🏢", "label_prefix": "Company"},
    "Crypto Wallet": {"color": "#FFCE56", "shape": "star", "icon": "🪙", "label_prefix": "Wallet"},
    "Vehicle": {"color": "#FF9F40", "shape": "triangle", "icon": "🚗", "label_prefix": "Vehicle"},
    "Location": {"color": "#00CC99", "shape": "square", "icon": "📍", "label_prefix": "Location"},
    "Incident": {"color": "#E74C3C", "shape": "hexagon", "icon": "🚨", "label_prefix": "Incident"},
    "Social Media Handle": {"color": "#EC4899", "shape": "ellipse", "icon": "🌐", "label_prefix": "Social"},
    "Organization": {"color": "#8B5CF6", "shape": "box", "icon": "🏛️", "label_prefix": "Org"},
    "Intel Report": {"color": "#10B981", "shape": "star", "icon": "📑", "label_prefix": "Intel"},
    "Watchlist Flag": {"color": "#F43F5E", "shape": "triangleDown", "icon": "⚠️", "label_prefix": "Watchlist"},
}

# Relationship Types
RELATIONSHIP_TYPES = [
    "CALL_MADE",
    "MONEY_TRANSFERRED",
    "ENCRYPTED_CHAT",
    "CO_LOCATION",
    "CO_ARREST",
    "OWNERSHIP",
    "CRYPTO_TRANSFER",
    "VEHICLE_TRACKED",
    "ALIAS_OF",
    "CALL_BURST",
    "SOCIAL_MENTION",
    "SUSPICIOUS_TRANSFER",
    "CO_OFFENDER",
    "SANCTIONED_BY",
    "ASSOCIATED_WITH",
]

# Color map for edges based on relationship
EDGE_COLORS = {
    "CALL_MADE": "#36A2EB",
    "MONEY_TRANSFERRED": "#2ECC71",
    "ENCRYPTED_CHAT": "#9B59B6",
    "CO_LOCATION": "#E67E22",
    "CO_ARREST": "#E74C3C",
    "OWNERSHIP": "#34495E",
    "CRYPTO_TRANSFER": "#F1C40F",
    "VEHICLE_TRACKED": "#1ABC9C",
    "ALIAS_OF": "#EC4899",
    "CALL_BURST": "#FF5722",
    "SOCIAL_MENTION": "#A855F7",
    "SUSPICIOUS_TRANSFER": "#EF4444",
    "CO_OFFENDER": "#DC2626",
    "SANCTIONED_BY": "#B91C1C",
    "ASSOCIATED_WITH": "#64748B",
}

# Risk Thresholds
RISK_LEVELS = {
    "CRITICAL": {"min": 80, "color": "#FF0000"},
    "HIGH": {"min": 60, "color": "#FF6600"},
    "MEDIUM": {"min": 35, "color": "#FFAA00"},
    "LOW": {"min": 0, "color": "#28A745"},
}

# Default App Settings
DEFAULT_GRAPH_PHYSICS = {
    "solver": "forceAtlas2Based",
    "forceAtlas2Based": {
        "gravitationalConstant": -50,
        "centralGravity": 0.01,
        "springLength": 100,
        "springConstant": 0.08,
    },
}

DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "ingested")
os.makedirs(DATA_DIR, exist_ok=True)

