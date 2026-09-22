"""
NexusGraph AI - AI-Based Criminal Network & Investigative Graph Analytics Platform
Main Streamlit Application
"""

import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="NexusGraph AI | Investigative Network Platform",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
import numpy as np
import streamlit.components.v1 as components

from config import ENTITY_TYPES, RELATIONSHIP_TYPES
from sample_generator import generate_investigation_dataset
from graph_builder import CriminalGraphBuilder
from metrics import compute_graph_metrics
from pattern_detector import PatternDetector
from pathfinder import PathfinderEngine
from graph_renderer import render_pyvis_graph
from timeline_view import render_event_timeline
from map_view import render_geospatial_map
from query_parser import InvestiAIQueryEngine
from report_generator import generate_intelligence_dossier_html
from styles import apply_custom_css
from streamlit_folium import st_folium

# New Multi-Source & Intelligence Engines
from nlp_extractor import NLPEntityExtractor
from cdr_analyzer import CDRAnalyzer
from social_media_intel import SocialMediaIntelEngine
from multi_source_loader import MultiSourceDataLoader

# Apply Custom Theme Styling
apply_custom_css()

# Initialize Session State
if "scenario" not in st.session_state:
    st.session_state["scenario"] = "Operation Black Ice"

if "df_nodes" not in st.session_state or "df_edges" not in st.session_state:
    df_n, df_e = generate_investigation_dataset(st.session_state["scenario"])
    st.session_state["df_nodes"] = df_n
    st.session_state["df_edges"] = df_e

# Instantiate Graph Builder
builder = CriminalGraphBuilder(st.session_state["df_nodes"], st.session_state["df_edges"])
G_full = builder.graph

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/network.png", width=64)
    st.title("NexusGraph AI")
    st.caption("Multi-Source Criminal Intelligence Platform v3.0")

    st.markdown("---")
    st.subheader("🎯 Active Investigation")
    scenario_choice = st.selectbox(
        "Select Case Scenario",
        ["Operation Black Ice", "Operation Cyber Strike", "Operation Titan Gang"],
        index=0
    )
    if scenario_choice != st.session_state["scenario"]:
        st.session_state["scenario"] = scenario_choice
        df_n, df_e = generate_investigation_dataset(scenario_choice)
        st.session_state["df_nodes"] = df_n
        st.session_state["df_edges"] = df_e
        st.rerun()

    st.markdown("---")
    st.subheader("🎛️ Graph Filters")

    # Risk Score Slider
    min_risk, max_risk = st.slider("Entity Risk Score Range", 0, 100, (0, 100))

    # Entity Type Filter
    selected_entities = st.multiselect(
        "Entity Types",
        options=list(ENTITY_TYPES.keys()),
        default=list(ENTITY_TYPES.keys())
    )

    # Relationship Type Filter
    selected_rels = st.multiselect(
        "Relationship Types",
        options=RELATIONSHIP_TYPES,
        default=RELATIONSHIP_TYPES
    )

    # Search entity
    search_query = st.text_input("🔍 Quick Entity Search", placeholder="Name or ID...")

    st.markdown("---")
    st.caption("🔒 Law Enforcement Sensitive // Official Use Only")

# Filtered Graph
G_sub = builder.get_filtered_subgraph(
    entity_types=selected_entities,
    relationship_types=selected_rels,
    min_risk=min_risk,
    max_risk=max_risk,
    search_query=search_query
)

# Compute Metrics
metrics_df = compute_graph_metrics(G_sub)

# --- HEADER SECTION ---
st.markdown(f"## 🛡️ Case File: <span style='color:#38BDF8;'>{st.session_state['scenario']}</span>", unsafe_allow_html=True)

# Top Summary Metrics
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Entities</div>
            <div class="metric-value">{len(G_sub.nodes())}</div>
        </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Relationships</div>
            <div class="metric-value">{len(G_sub.edges())}</div>
        </div>
    """, unsafe_allow_html=True)
with c3:
    high_risk_cnt = len(metrics_df[metrics_df['ai_risk_score'] >= 75]) if not metrics_df.empty else 0
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">High Risk Entities</div>
            <div class="metric-value" style="color:#EF4444;">{high_risk_cnt}</div>
        </div>
    """, unsafe_allow_html=True)
with c4:
    detector = PatternDetector(G_sub)
    cycles = detector.detect_circular_money_trails()
    total_laundering = sum(c['total_volume'] for c in cycles) if cycles else 0
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Laundering Volume</div>
            <div class="metric-value" style="color:#10B981;">${total_laundering:,.0f}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# --- NAVIGATION TABS ---
tab_workbench, tab_nlp, tab_patterns, tab_cdr, tab_socmint, tab_pathfinder, tab_geotemp, tab_ai, tab_ingest = st.tabs([
    "🔍 Graph Workbench",
    "🧠 NLP Report Extractor",
    "🚨 Pattern & Anomaly Discovery",
    "📱 CDR Analytics",
    "🌐 SOCMINT & Aliases",
    "🕸️ Pathfinder & Link Tracing",
    "📍 Geo-Temporal Intelligence",
    "🤖 AI Assistant & Case Dossier",
    "📥 Multi-Source Data Ingestion"
])


# =============================================================================
# TAB 1: GRAPH WORKBENCH
# =============================================================================
with tab_workbench:
    col_graph, col_dossier = st.columns([3, 1])

    with col_graph:
        st.subheader("Interactive Knowledge Graph Workbench")
        
        physics_choice = st.selectbox(
            "Physics Layout Engine",
            ["forceAtlas2Based", "barnesHut", "hierarchical"],
            index=0,
            key="physics_select"
        )

        if len(G_sub.nodes()) == 0:
            st.warning("No entities match the current sidebar filter criteria.")
        else:
            html_code = render_pyvis_graph(G_sub, height="650px", physics_solver=physics_choice)
            components.html(html_code, height=670, scrolling=False)

    with col_dossier:
        st.subheader("📋 Entity Dossier Inspector")
        node_options = [f"{data.get('name')} ({node})" for node, data in G_sub.nodes(data=True)]
        if node_options:
            selected_option = st.selectbox("Select Target Entity", node_options)
            sel_node_id = selected_option.split("(")[-1].replace(")", "").strip()
            
            dossier = builder.get_node_dossier(sel_node_id)
            if dossier:
                meta = dossier['metadata']
                r_score = meta.get('risk_score', 50)
                r_class = "badge-critical" if r_score >= 75 else "badge-high" if r_score >= 50 else "badge-medium"
                
                st.markdown(f"""
                    <div style="background: #1E293B; padding: 15px; border-radius: 8px; border: 1px solid #334155;">
                        <h4 style="margin:0; color:#38BDF8;">{meta.get('name')}</h4>
                        <p style="margin:4px 0;"><b>Type:</b> {meta.get('type')}</p>
                        <p style="margin:4px 0;"><b>Risk Score:</b> <span class="{r_class}">{r_score}/100</span></p>
                        <p style="margin:4px 0;"><b>Status:</b> {meta.get('status')}</p>
                        <p style="font-size:12px; font-style:italic; color:#94A3B8;">{meta.get('notes')}</p>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("##### Direct Connections")
                st.markdown(f"**Inbound Connections:** `{len(dossier['inbound_connections'])}`")
                for conn in dossier['inbound_connections'][:3]:
                    st.caption(f"⬅️ **{conn['from_name']}**: {conn['relationship']} ({conn['details']})")

                st.markdown(f"**Outbound Connections:** `{len(dossier['outbound_connections'])}`")
                for conn in dossier['outbound_connections'][:3]:
                    st.caption(f"➡️ **{conn['to_name']}**: {conn['relationship']} ({conn['details']})")
        else:
            st.info("No entities available.")

# =============================================================================
# TAB 2: NLP REPORT EXTRACTOR
# =============================================================================
with tab_nlp:
    st.subheader("🧠 NLP Rule-Based Unstructured Text & FIR Entity Extractor")
    st.markdown("Paste raw unstructured text (FIR reports, police narratives, surveillance logs, intelligence briefs) to automatically extract entities and relationship graphs.")

    sample_report_text = """FIRST INFORMATION REPORT (FIR-2026-0982)
Date: 2026-03-01 | Station: Metro Central Precinct

Narrative:
During surveillance of suspect Victor Vance near Grand Palace Hotel Suite 804, investigators intercepted encrypted calls on burner phone +1-555-987-001 to associate Elena Rostova on +1-555-987-002. 

Elena Rostova managed bank transfers from Apex Holdings Corp to straw account ACC_884005 totaling $450,000 for invoice clearing. Further SIGINT revealed darknet handle @spectre_shadow linked to crypto wallet 0x71C884920039F which processed $250,000 in USDT. 

Vehicle Black SUV with license plate KNG-990 was tracked heading towards Docklands Warehouse #14. High-risk associate Marco Rossi was spotted at Cell Tower #409."""

    input_narrative = st.text_area("Paste FIR Narrative / Police Report Text", value=sample_report_text, height=220)

    if st.button("🚀 Process Text & Build Graph Nodes"):
        if input_narrative.strip():
            df_n_ext, df_e_ext = MultiSourceDataLoader.load_fir_narrative(input_narrative)
            
            st.session_state["df_nodes"] = df_n_ext
            st.session_state["df_edges"] = df_e_ext
            st.session_state["scenario"] = "Extracted FIR Narrative Case"
            st.success(f"Successfully extracted {len(df_n_ext)} entities and {len(df_e_ext)} relationships!")
            st.rerun()

# =============================================================================
# TAB 3: PATTERN & ANOMALY DISCOVERY
# =============================================================================
with tab_patterns:
    st.subheader("🚨 Automated AI Pattern & Criminal Anomaly Discovery")
    
    p_tab1, p_tab2, p_tab3, p_tab4, p_tab5, p_tab6, p_tab7 = st.tabs([
        "💸 Circular Money Trails",
        "🏦 Smurfing & Structuring",
        "👑 Hidden Kingpin Analysis",
        "📍 Co-Location Hotspots",
        "📱 Call Burst Anomalies",
        "🔥 Burner Line Rotation",
        "🧩 Gang Clustering"
    ])

    detector = PatternDetector(G_sub)

    with p_tab1:
        st.markdown("### 🔄 Money Laundering Cycles (A → B → C → A)")
        loops = detector.detect_circular_money_trails()
        if loops:
            for l_idx, loop in enumerate(loops):
                st.markdown(f"""
                    <div class="alert-critical-box">
                        <h4 style="margin:0; color:#EF4444;">Cycle Alert #{l_idx+1}: {loop['risk_flag']}</h4>
                        <p style="margin:4px 0;"><b>Path:</b> {' ➔ '.join(loop['cycle_names'])} ➔ {loop['cycle_names'][0]}</p>
                        <p style="margin:4px 0;"><b>Total Loop Volume:</b> <span style="color:#10B981; font-weight:bold;">${loop['total_volume']:,.2f}</span> | <b>Hops:</b> {loop['length']}</p>
                    </div>
                """, unsafe_allow_html=True)
                with st.expander(f"View Transfer Breakdown for Cycle #{l_idx+1}"):
                    st.table(pd.DataFrame(loop['transfers']))
        else:
            st.success("No circular money laundering cycles detected in the current view.")

    with p_tab2:
        st.markdown("### 🏦 Structuring / Smurfing Detection (< $10,000 Deposits)")
        smurfs = detector.detect_smurfing_structuring()
        if smurfs:
            for sm in smurfs:
                st.markdown(f"""
                    <div class="alert-warning-box">
                        <h4 style="margin:0; color:#F59E0B;">Target Account: {sm['account_name']} ({sm['account_id']})</h4>
                        <p style="margin:4px 0;"><b>Transactions Received:</b> {sm['tx_count']} under $10k limit | <b>Total Structured Volume:</b> ${sm['total_structured_amount']:,.2f}</p>
                    </div>
                """, unsafe_allow_html=True)
                with st.expander("View Incoming Micro-Transactions"):
                    st.table(pd.DataFrame(sm['incoming_sources']))
        else:
            st.success("No smurfing or structured deposit patterns detected.")

    with p_tab3:
        st.markdown("### 👑 Insulated Kingpins & Buffer Leaders")
        kingpins = detector.detect_hidden_kingpin()
        if kingpins:
            for kp in kingpins:
                st.markdown(f"""
                    <div class="alert-critical-box">
                        <h4 style="margin:0; color:#EF4444;">Suspect: {kp['name']} ({kp['id']})</h4>
                        <p style="margin:4px 0;"><b>Betweenness Centrality:</b> {kp['betweenness']} | <b>Base Risk:</b> {kp['risk_score']}/100</p>
                        <p style="margin:4px 0;"><b>Financial Insulation:</b> {kp['financial_insulation']}</p>
                        <p style="margin:4px 0; color:#38BDF8;"><b>Action Plan:</b> {kp['recommendation']}</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No insulated kingpin candidates flagged in current view.")

    with p_tab4:
        st.markdown("### 📍 Physical Co-Location & Surveillance Hotspots")
        hotspots = detector.detect_colocation_hotspots()
        if hotspots:
            for hs in hotspots:
                st.markdown(f"""
                    <div class="alert-warning-box">
                        <h4 style="margin:0; color:#F59E0B;">Location: {hs['location_name']}</h4>
                        <p style="margin:4px 0;"><b>Co-Present Suspects/Vehicles:</b> {hs['co_located_count']}</p>
                    </div>
                """, unsafe_allow_html=True)
                with st.expander("View Co-Present Entities"):
                    st.table(pd.DataFrame(hs['entities_present']))
        else:
            st.info("No co-location meeting hotspots detected.")

    with p_tab5:
        st.markdown("### 📱 High Frequency Communication Call Bursts")
        bursts = detector.detect_call_burst_anomalies()
        if bursts:
            for b in bursts:
                st.markdown(f"""
                    <div class="alert-warning-box">
                        <h4 style="margin:0; color:#F59E0B;">Call Burst: {b['caller_name']} ➔ {b['callee_name']}</h4>
                        <p style="margin:4px 0;"><b>Call Frequency:</b> {b['call_frequency']} calls | <b>Channel:</b> {b['relationship']}</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No high-frequency call burst anomalies flagged.")

    with p_tab6:
        st.markdown("### 🔥 Rapid Burner Phone Line Rotation")
        burners = detector.detect_burner_phone_rotation()
        if burners:
            for br in burners:
                st.markdown(f"""
                    <div class="alert-critical-box">
                        <h4 style="margin:0; color:#EF4444;">Suspect: {br['suspect_name']} ({br['suspect_id']})</h4>
                        <p style="margin:4px 0;"><b>Active Burner Phone Lines:</b> {br['phone_count']} ({', '.join(br['phones'])})</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No multi-burner rotation patterns detected.")

    with p_tab7:
        st.markdown("### 🧩 Louvain Gang Community Clustering")
        if not metrics_df.empty:
            st.dataframe(metrics_df[['id', 'name', 'type', 'ai_risk_score', 'betweenness', 'pagerank', 'gang_community']], use_container_width=True)

# =============================================================================
# TAB 4: CDR ANALYTICS
# =============================================================================
with tab_cdr:
    st.subheader("📱 Call Detail Record (CDR) & Communication Intelligence")
    
    cdr_eng = CDRAnalyzer(G_sub)
    stats = cdr_eng.get_cdr_summary_stats()

    col_cdr1, col_cdr2, col_cdr3 = st.columns(3)
    with col_cdr1:
        st.metric("Total Intercepted Calls", stats['total_calls'])
    with col_cdr2:
        st.metric("Unique Phone Entities", stats['unique_callers'])
    with col_cdr3:
        st.metric("Top Frequent Link", stats['top_call_pair'])

    st.markdown("---")
    st.markdown("### 🌙 Odd-Hour & Encrypted Channel Intercepts (23:00 - 05:00)")
    odd_calls = cdr_eng.detect_odd_hour_calls()
    if odd_calls:
        st.dataframe(pd.DataFrame(odd_calls), use_container_width=True)
    else:
        st.info("No odd-hour intercepts logged in current graph view.")

# =============================================================================
# TAB 5: SOCMINT & ALIAS INTELLIGENCE
# =============================================================================
with tab_socmint:
    st.subheader("🌐 Social Media Intelligence (SOCMINT) & Digital Footprints")
    
    soc_eng = SocialMediaIntelEngine(G_sub)
    
    st.markdown("### 👤 Suspect Digital Footprint Matrix")
    df_footprint = soc_eng.get_digital_footprint_matrix()
    if not df_footprint.empty:
        st.dataframe(df_footprint, use_container_width=True)
    else:
        st.info("No digital footprints mapped for suspects in current view.")

    st.markdown("### 🔗 Alias Resolution & Online Handles")
    aliases = soc_eng.resolve_aliases()
    if aliases:
        st.dataframe(pd.DataFrame(aliases), use_container_width=True)

# =============================================================================
# TAB 6: PATHFINDER & LINK TRACING
# =============================================================================
with tab_pathfinder:
    st.subheader("🕸️ Multi-Hop Pathfinder & Link Analysis")
    
    col_src, col_dst, col_btn = st.columns([2, 2, 1])
    
    all_nodes_list = list(G_sub.nodes())
    node_names_map = {n: f"{G_sub.nodes[n].get('name', n)} ({n})" for n in all_nodes_list}

    with col_src:
        src_selection = st.selectbox("Source Entity (A)", options=all_nodes_list, format_func=lambda x: node_names_map[x], index=0 if all_nodes_list else None)
    with col_dst:
        dst_selection = st.selectbox("Target Entity (B)", options=all_nodes_list, format_func=lambda x: node_names_map[x], index=min(1, len(all_nodes_list)-1) if all_nodes_list else None)

    with col_btn:
        st.markdown("<br/>", unsafe_allow_html=True)
        find_btn = st.button("🔎 Trace Path", use_container_width=True)

    if find_btn and src_selection and dst_selection:
        pf = PathfinderEngine(G_sub)
        res = pf.find_shortest_paths(src_selection, dst_selection)

        if res['status'] == "SUCCESS":
            st.success(f"Found {res['path_count']} shortest path connection(s)!")
            for idx, p in enumerate(res['paths']):
                st.markdown(f"#### Path #{idx+1} ({p['hop_count']} Hops): {' ➔ '.join(p['path_names'])}")
                st.table(pd.DataFrame(p['steps']))
        else:
            st.error(f"Pathfinder Result: {res['message']}")

# =============================================================================
# TAB 7: GEO-TEMPORAL INTELLIGENCE
# =============================================================================
with tab_geotemp:
    st.subheader("📍 Geospatial Mapping & Temporal Timeline")
    
    col_map, col_time = st.columns([1, 1])
    
    with col_map:
        st.markdown("#### Cell Towers, Crime Sites & Movement Map")
        m = render_geospatial_map(G_sub)
        st_folium(m, width=550, height=450)

    with col_time:
        st.markdown("#### Chronological Interception Timeline")
        fig_time = render_event_timeline(G_sub)
        st.plotly_chart(fig_time, use_container_width=True)

# =============================================================================
# TAB 8: AI ASSISTANT & CASE DOSSIER
# =============================================================================
with tab_ai:
    st.subheader("🤖 InvestiAI Natural Language Assistant & Dossier Generator")
    
    col_q, col_rep = st.columns([2, 1])
    
    with col_q:
        query_input = st.text_input(
            "Ask the AI Assistant a question about the graph:",
            value="Who is the kingpin candidate?",
            placeholder="e.g., Find money laundering loops / Check burner phones / Who is high risk?"
        )
        ask_btn = st.button("⚡ Query Knowledge Graph")

        if ask_btn and query_input:
            ai_engine = InvestiAIQueryEngine(G_sub)
            answer = ai_engine.answer_query(query_input)

            st.markdown(f"### {answer['title']}")
            st.write(answer['summary'])
            
            if answer.get('data'):
                with st.expander("Inspect Raw Graph Analytical Evidence"):
                    st.write(answer['data'])

            st.info(f"💡 **Recommended Action:** {answer['action']}")

    with col_rep:
        st.markdown("#### 📄 Export Case Dossier")
        st.caption("Generate official law enforcement intelligence dossier report for court submission.")
        
        if st.button("📥 Generate Intelligence Report (HTML)", use_container_width=True):
            html_report = generate_intelligence_dossier_html(G_sub, case_title=st.session_state["scenario"])
            st.download_button(
                label="⬇️ Download Official Dossier (.html)",
                data=html_report,
                file_name=f"NexusGraph_Dossier_{st.session_state['scenario'].replace(' ', '_')}.html",
                mime="text/html",
                use_container_width=True
            )

# =============================================================================
# TAB 9: MULTI-SOURCE DATA INGESTION
# =============================================================================
with tab_ingest:
    st.subheader("📥 Multi-Source Data Ingestion & Custom Loader")
    st.markdown("Upload structured or unstructured investigation files (CDR CSVs, Financial CSVs, Custom Nodes/Edges CSVs) to construct new knowledge graphs.")

    ingest_type = st.radio("Select Input Data Source Type", ["Custom Nodes & Edges CSV", "CDR File (CSV)", "Financial Log (CSV)"], horizontal=True)

    if ingest_type == "Custom Nodes & Edges CSV":
        col_u1, col_u2 = st.columns(2)
        with col_u1:
            nodes_file = st.file_uploader("Upload Entities (Nodes CSV)", type=["csv"], key="n_csv")
        with col_u2:
            edges_file = st.file_uploader("Upload Relationships (Edges CSV)", type=["csv"], key="e_csv")

        if nodes_file and edges_file:
            try:
                df_n_upload = pd.read_csv(nodes_file)
                df_e_upload = pd.read_csv(edges_file)
                
                if st.button("🚀 Ingest & Build Knowledge Graph", key="btn_build_csv"):
                    st.session_state["df_nodes"] = df_n_upload
                    st.session_state["df_edges"] = df_e_upload
                    st.session_state["scenario"] = "Custom Ingested CSV Case"
                    st.success("Successfully ingested custom dataset!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error parsing uploaded files: {str(e)}")

    elif ingest_type == "CDR File (CSV)":
        cdr_file = st.file_uploader("Upload Call Detail Record (CDR CSV)", type=["csv"])
        if cdr_file:
            try:
                df_n_cdr, df_e_cdr = MultiSourceDataLoader.load_cdr_csv(cdr_file)
                if st.button("🚀 Process CDR File"):
                    st.session_state["df_nodes"] = df_n_cdr
                    st.session_state["df_edges"] = df_e_cdr
                    st.session_state["scenario"] = "Uploaded CDR Investigation"
                    st.success(f"Successfully processed CDR file! Ingested {len(df_n_cdr)} phone entities.")
                    st.rerun()
            except Exception as e:
                st.error(f"Error processing CDR file: {str(e)}")

    elif ingest_type == "Financial Log (CSV)":
        fin_file = st.file_uploader("Upload Financial Transaction Log (CSV)", type=["csv"])
        if fin_file:
            try:
                df_n_fin, df_e_fin = MultiSourceDataLoader.load_financial_csv(fin_file)
                if st.button("🚀 Process Financial Log"):
                    st.session_state["df_nodes"] = df_n_fin
                    st.session_state["df_edges"] = df_e_fin
                    st.session_state["scenario"] = "Uploaded Financial Log"
                    st.success(f"Successfully processed financial log! Ingested {len(df_n_fin)} accounts.")
                    st.rerun()
            except Exception as e:
                st.error(f"Error processing financial log: {str(e)}")
