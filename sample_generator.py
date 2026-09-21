"""
Realistic Multi-Scenario Synthetic Data Generator for Investigation Graph Analytics
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_investigation_dataset(scenario="Operation Black Ice"):
    """
    Generates realistic nodes (entities) and edges (relationships) dataframe.
    Scenarios:
    - Operation Black Ice (Money Laundering, Drug Syndicate, Kingpin)
    - Operation Cyber Strike (Crypto Smurfing, Phishing, Mule Accounts)
    - Operation Titan Gang (Co-location, Encrypted Chats, Crime Incidents)
    """
    random.seed(42)
    np.random.seed(42)

    nodes = []
    edges = []

    if scenario == "Operation Black Ice":
        # --- KINGPIN & TOP LIEUTENANTS ---
        nodes.append({"id": "PER_001", "name": "Victor Vance 'The Spectre'", "type": "Suspect", "risk_score": 95, "status": "Under Surveillance", "notes": "Alleged Syndicate Leader. Operates through buffer nodes."})
        nodes.append({"id": "PER_002", "name": "Elena Rostova", "type": "Suspect", "risk_score": 88, "status": "Prime Suspect", "notes": "Chief Financial Officer of Shell Network."})
        nodes.append({"id": "PER_003", "name": "Marco Rossi", "type": "Suspect", "risk_score": 82, "status": "Under Investigation", "notes": "Logistics & Narcotics Handler."})
        nodes.append({"id": "PER_004", "name": "Tariq Mansoor", "type": "Suspect", "risk_score": 79, "status": "Person of Interest", "notes": "Hawala Operator."})
        nodes.append({"id": "PER_005", "name": "David Miller", "type": "Suspect", "risk_score": 75, "status": "Mule Recruiter", "notes": "Recruits straw bank account holders."})
        
        # MULES & STRAW SUSPECTS
        for i in range(6, 16):
            nodes.append({"id": f"PER_{i:03d}", "name": f"Mule Suspect {i}", "type": "Suspect", "risk_score": random.randint(30, 65), "status": "Flagged Account Holder", "notes": "Straw account provider."})

        # --- PHONE NUMBERS ---
        nodes.append({"id": "PHN_001", "name": "+1-555-987-001 (Burner Alpha)", "type": "Phone", "risk_score": 90, "status": "Active", "notes": "Encrypted Burner Phone used by Victor."})
        nodes.append({"id": "PHN_002", "name": "+1-555-987-002 (Elena Direct)", "type": "Phone", "risk_score": 85, "status": "Monitored", "notes": "Registered to Elena."})
        nodes.append({"id": "PHN_003", "name": "+1-555-987-003 (Rossi Comms)", "type": "Phone", "risk_score": 80, "status": "Active", "notes": "Used for logistics."})
        nodes.append({"id": "PHN_004", "name": "+1-555-987-004 (Tariq Hawala line)", "type": "Phone", "risk_score": 78, "status": "Monitored", "notes": "Hawala dispatch phone."})
        
        for i in range(5, 12):
            nodes.append({"id": f"PHN_{i:03d}", "name": f"+1-555-019-{i:03d}", "type": "Phone", "risk_score": random.randint(40, 70), "status": "Active", "notes": "Associate line."})

        # --- BANK ACCOUNTS & SHELL COMPANIES ---
        nodes.append({"id": "ACC_001", "name": "Apex Holdings Corp (SG Bank)", "type": "Shell Company", "risk_score": 92, "status": "Frozen", "notes": "Primary Offshore Laundering entity."})
        nodes.append({"id": "ACC_002", "name": "BlueWave Logistics Ltd (Panama)", "type": "Shell Company", "risk_score": 89, "status": "Under Audit", "notes": "Trade-based money laundering front."})
        nodes.append({"id": "ACC_003", "name": "SilkRoad Trading FZE (Dubai)", "type": "Shell Company", "risk_score": 86, "status": "Flagged", "notes": "Hawala clearance company."})

        # Mule accounts for structuring
        for i in range(4, 14):
            nodes.append({"id": f"ACC_{i:03d}", "name": f"Account #{884000+i} (Mule)", "type": "Bank Account", "risk_score": random.randint(45, 75), "status": "High Velocity", "notes": "Straw account used for smurfing."})

        # --- CRYPTO WALLETS ---
        nodes.append({"id": "WLT_001", "name": "0x71C...39F (Tornado Mixer Out)", "type": "Crypto Wallet", "risk_score": 94, "status": "Tainted", "notes": "Mixer wallet receiving darknet proceeds."})
        nodes.append({"id": "WLT_002", "name": "0x98A...11B (Cold Storage Alpha)", "type": "Crypto Wallet", "risk_score": 88, "status": "Monitored", "notes": "Connected to Victor Vance."})
        nodes.append({"id": "WLT_003", "name": "0x34D...66C (Off-ramp Exchange)", "type": "Crypto Wallet", "risk_score": 70, "status": "Exchange KYC", "notes": "KYC registered to Elena Rostova."})

        # --- VEHICLES & LOCATIONS ---
        nodes.append({"id": "VEH_001", "name": "Black SUV (Lic: KNG-990)", "type": "Vehicle", "risk_score": 75, "status": "Tracked", "notes": "Spotted at multiple meeting sites."})
        nodes.append({"id": "VEH_002", "name": "Delivery Van (Lic: TRK-412)", "type": "Vehicle", "risk_score": 81, "status": "Impounded", "notes": "Contraband transport vehicle."})
        
        nodes.append({"id": "LOC_001", "name": "Docklands Warehouse #14", "type": "Location", "risk_score": 85, "status": "Raid Site", "notes": "Narcotics drop point."})
        nodes.append({"id": "LOC_002", "name": "Grand Palace Hotel Suite 804", "type": "Location", "risk_score": 78, "status": "Monitored", "notes": "Meeting spot between Victor & Elena."})
        nodes.append({"id": "LOC_003", "name": "Cell Tower #409 (Downtown Financial)", "type": "Location", "risk_score": 50, "status": "Infrastructure", "notes": "Co-location hub."})

        # --- SOCIAL MEDIA HANDLES & INTEL REPORTS ---
        nodes.append({"id": "SOC_001", "name": "@spectre_shadow", "type": "Social Media Handle", "risk_score": 92, "status": "SOCMINT Flagged", "notes": "Encrypted Telegram handle linked to Victor Vance."})
        nodes.append({"id": "SOC_002", "name": "@elena_finance", "type": "Social Media Handle", "risk_score": 84, "status": "Monitored", "notes": "X (Twitter) handle used for offshore promos."})
        nodes.append({"id": "INT_001", "name": "INTERPOL Red Notice #2026-90", "type": "Intel Report", "risk_score": 98, "status": "High Priority Flag", "notes": "Sanctioned international money laundering syndicate."})

        edges.append({"source": "PER_001", "target": "SOC_001", "relationship": "ALIAS_OF", "weight": 5, "timestamp": "2026-01-08", "amount": 0, "details": "Darknet alias linked by SIGINT."})
        edges.append({"source": "PER_002", "target": "SOC_002", "relationship": "ALIAS_OF", "weight": 3, "timestamp": "2026-01-09", "amount": 0, "details": "Public OSINT alias."})
        edges.append({"source": "PER_001", "target": "INT_001", "relationship": "SANCTIONED_BY", "weight": 10, "timestamp": "2026-01-01", "amount": 0, "details": "Flagged under global sanctions list."})

        # --- INCIDENTS ---
        nodes.append({"id": "INC_001", "name": "FIR-2025-0899 (Seizure of $2.4M Cash)", "type": "Incident", "risk_score": 95, "status": "Closed Investigation", "notes": "Cash seized from vehicle TRK-412."})
        nodes.append({"id": "INC_002", "name": "FIR-2026-0104 (Customs Narcotics Bust)", "type": "Incident", "risk_score": 90, "status": "Active Trial", "notes": "50kg contraband seized at Warehouse #14."})


        # =========================================================================
        # EDGES / RELATIONSHIPS
        # =========================================================================
        start_date = datetime(2026, 1, 1)

        # 1. KINGPIN CONNECTIONS (Buffer model: Victor rarely directly contacts lower mules)
        edges.append({"source": "PER_001", "target": "PHN_001", "relationship": "OWNERSHIP", "weight": 5, "timestamp": "2026-01-05", "amount": 0, "details": "Encrypted burner owned by Victor."})
        edges.append({"source": "PHN_001", "target": "PHN_002", "relationship": "ENCRYPTED_CHAT", "weight": 42, "timestamp": "2026-01-10", "amount": 0, "details": "42 Signal calls to Elena Rostova."})
        edges.append({"source": "PHN_001", "target": "PHN_004", "relationship": "CALL_MADE", "weight": 18, "timestamp": "2026-01-12", "amount": 0, "details": "Calls to Tariq Hawala operator."})
        
        # Elena -> Financial & Shells
        edges.append({"source": "PER_002", "target": "PHN_002", "relationship": "OWNERSHIP", "weight": 1, "timestamp": "2026-01-02", "amount": 0, "details": "Registered mobile."})
        edges.append({"source": "PER_002", "target": "ACC_001", "relationship": "OWNERSHIP", "weight": 10, "timestamp": "2026-01-03", "amount": 0, "details": "Authorized signatory of Apex Holdings."})
        edges.append({"source": "PER_002", "target": "WLT_003", "relationship": "OWNERSHIP", "weight": 5, "timestamp": "2026-01-15", "amount": 0, "details": "KYC linked crypto wallet."})

        # 2. CIRCULAR MONEY LAUNDERING TRAIL (A -> B -> C -> D -> A)
        # Apex (ACC_001) -> BlueWave (ACC_002) -> SilkRoad (ACC_003) -> Mule ACC_004 -> Apex (ACC_001)
        edges.append({"source": "ACC_001", "target": "ACC_002", "relationship": "MONEY_TRANSFERRED", "weight": 8, "timestamp": "2026-02-01", "amount": 450000, "details": "Wire transfer for fake invoices."})
        edges.append({"source": "ACC_002", "target": "ACC_003", "relationship": "MONEY_TRANSFERRED", "weight": 6, "timestamp": "2026-02-03", "amount": 420000, "details": "Consulting fee payout."})
        edges.append({"source": "ACC_003", "target": "ACC_004", "relationship": "MONEY_TRANSFERRED", "weight": 12, "timestamp": "2026-02-05", "amount": 400000, "details": "Hawala disbursement to straw account."})
        edges.append({"source": "ACC_004", "target": "ACC_001", "relationship": "MONEY_TRANSFERRED", "weight": 4, "timestamp": "2026-02-08", "amount": 390000, "details": "Loan repayment back to Apex."}) # LOOP CLOSED!

        # 3. SMURFING / STRUCTURING (Multiple Mules transfers -> Single Shell ACC_001)
        mule_accs = [f"ACC_{i:03d}" for i in range(5, 12)]
        for acc in mule_accs:
            amount = random.randint(9000, 9900) # Under $10k reporting limit
            edges.append({"source": acc, "target": "ACC_001", "relationship": "MONEY_TRANSFERRED", "weight": random.randint(5, 15), "timestamp": "2026-02-12", "amount": amount, "details": f"Structuring cash deposit ${amount}"})
            
            # Connect Mules to recruiter David Miller (PER_005)
            mule_id = f"PER_{int(acc.split('_')[1]):03d}"
            if any(n['id'] == mule_id for n in nodes):
                edges.append({"source": "PER_005", "target": mule_id, "relationship": "CALL_MADE", "weight": random.randint(3, 10), "timestamp": "2026-01-20", "amount": 0, "details": "Recruitment & instruction calls."})
                edges.append({"source": mule_id, "target": acc, "relationship": "OWNERSHIP", "weight": 1, "timestamp": "2026-01-22", "amount": 0, "details": "Account holder."})

        # 4. CRYPTO LAYERING TRAIL
        edges.append({"source": "ACC_001", "target": "WLT_001", "relationship": "CRYPTO_TRANSFER", "weight": 9, "timestamp": "2026-02-15", "amount": 250000, "details": "Off-ramp buy order into USDT."})
        edges.append({"source": "WLT_001", "target": "WLT_002", "relationship": "CRYPTO_TRANSFER", "weight": 7, "timestamp": "2026-02-16", "amount": 245000, "details": "Mixer transfer to Cold storage."})
        edges.append({"source": "WLT_002", "target": "WLT_003", "relationship": "CRYPTO_TRANSFER", "weight": 4, "timestamp": "2026-02-18", "amount": 100000, "details": "Transfer to Elena's KYC wallet."})

        # 5. CO-LOCATION & INCIDENT LINKS
        edges.append({"source": "PER_001", "target": "LOC_002", "relationship": "CO_LOCATION", "weight": 4, "timestamp": "2026-02-20", "amount": 0, "details": "Checked in Suite 804."})
        edges.append({"source": "PER_002", "target": "LOC_002", "relationship": "CO_LOCATION", "weight": 4, "timestamp": "2026-02-20", "amount": 0, "details": "Checked in Suite 804 (Co-presence detected)."})
        edges.append({"source": "PER_003", "target": "LOC_001", "relationship": "CO_LOCATION", "weight": 14, "timestamp": "2026-02-22", "amount": 0, "details": "Cell tower log near Warehouse #14."})
        edges.append({"source": "VEH_002", "target": "LOC_001", "relationship": "VEHICLE_TRACKED", "weight": 10, "timestamp": "2026-02-22", "amount": 0, "details": "LPR match at Warehouse #14 entrance."})
        
        edges.append({"source": "PER_003", "target": "INC_002", "relationship": "CO_ARREST", "weight": 1, "timestamp": "2026-02-22", "amount": 0, "details": "Arrested at crime scene."})
        edges.append({"source": "VEH_002", "target": "INC_002", "relationship": "VEHICLE_TRACKED", "weight": 1, "timestamp": "2026-02-22", "amount": 0, "details": "Vehicle seized in FIR-2026-0104."})
        edges.append({"source": "VEH_001", "target": "INC_001", "relationship": "VEHICLE_TRACKED", "weight": 1, "timestamp": "2026-01-28", "amount": 0, "details": "SUV impounded with cash."})

    else:
        # Default fallback lightweight scenario generator for demo
        for i in range(1, 15):
            nodes.append({"id": f"PER_{i:03d}", "name": f"Suspect {i}", "type": "Suspect", "risk_score": random.randint(20, 95), "status": "Active", "notes": "Generated suspect."})
            nodes.append({"id": f"PHN_{i:03d}", "name": f"+1-555-777-{i:03d}", "type": "Phone", "risk_score": random.randint(20, 90), "status": "Active", "notes": "Generated line."})
            nodes.append({"id": f"ACC_{i:03d}", "name": f"Account #{99000+i}", "type": "Bank Account", "risk_score": random.randint(20, 90), "status": "Active", "notes": "Generated bank account."})
            
            edges.append({"source": f"PER_{i:03d}", "target": f"PHN_{i:03d}", "relationship": "OWNERSHIP", "weight": 1, "timestamp": "2026-01-01", "amount": 0, "details": "Owner"})
            edges.append({"source": f"PER_{i:03d}", "target": f"ACC_{i:03d}", "relationship": "OWNERSHIP", "weight": 1, "timestamp": "2026-01-01", "amount": 0, "details": "Owner"})
            
            if i > 1:
                edges.append({"source": f"PHN_{i:03d}", "target": f"PHN_{i-1:03d}", "relationship": "CALL_MADE", "weight": random.randint(1, 15), "timestamp": "2026-01-05", "amount": 0, "details": "Call"})
                edges.append({"source": f"ACC_{i:03d}", "target": f"ACC_{i-1:03d}", "relationship": "MONEY_TRANSFERRED", "weight": 5, "timestamp": "2026-01-10", "amount": random.randint(5000, 50000), "details": "Transfer"})

    df_nodes = pd.DataFrame(nodes)
    df_edges = pd.DataFrame(edges)

    return df_nodes, df_edges
