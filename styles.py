"""
Dark Law Enforcement Command Center Theme & Custom CSS Styles
"""

import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
            /* Main background styling */
            .stApp {
                background-color: #0B0F19;
                color: #F8FAFC;
            }
            
            /* Sidebar styling */
            [data-testid="stSidebar"] {
                background-color: #111827;
                border-right: 1px solid #1E293B;
            }

            /* Custom metric card styling */
            .metric-card {
                background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
                border: 1px solid #334155;
                border-radius: 10px;
                padding: 16px;
                text-align: center;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
            }
            .metric-value {
                font-size: 28px;
                font-weight: 800;
                color: #38BDF8;
                margin-top: 4px;
            }
            .metric-label {
                font-size: 12px;
                color: #94A3B8;
                text-transform: uppercase;
                letter-spacing: 1px;
            }

            /* Risk Badges */
            .badge-critical {
                background-color: #DC2626;
                color: white;
                padding: 3px 8px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            .badge-high {
                background-color: #D97706;
                color: white;
                padding: 3px 8px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            .badge-medium {
                background-color: #CA8A04;
                color: white;
                padding: 3px 8px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }

            /* Tab bar styling */
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
                background-color: #111827;
                padding: 8px;
                border-radius: 8px;
                border: 1px solid #1E293B;
            }
            .stTabs [data-baseweb="tab"] {
                height: 45px;
                border-radius: 6px;
                color: #94A3B8;
                font-weight: 600;
            }
            .stTabs [aria-selected="true"] {
                background-color: #2563EB !important;
                color: #FFFFFF !important;
            }

            /* Alert Boxes */
            .alert-critical-box {
                background: #450A0A;
                border-left: 4px solid #EF4444;
                padding: 14px;
                border-radius: 6px;
                margin-bottom: 12px;
            }
            .alert-warning-box {
                background: #451A03;
                border-left: 4px solid #F59E0B;
                padding: 14px;
                border-radius: 6px;
                margin-bottom: 12px;
            }
        </style>
    """, unsafe_allow_html=True)
