# InvestiAI – AI-Powered Criminal Network Analysis System

> **One Case. Multiple Data Sources. One Connected Intelligence View.**

InvestiAI is an AI-powered investigative intelligence platform designed to help investigators analyze complex and fragmented investigation data from a single workspace.

In real investigations, useful information can be spread across FIRs, call records, financial transactions, case histories, social media intelligence, surveillance records, and other sources. Connecting this information manually can take a lot of time and may make it difficult to notice relationships between different entities.

InvestiAI brings these different data sources together and uses **NLP, graph analytics, pattern detection, and AI-assisted analysis** to help investigators explore relationships, identify recurring patterns, and generate structured investigation insights.

---

## 🚨 Problem Statement

Modern criminal activities can involve multiple people, phone numbers, organizations, locations, vehicles, financial accounts, and communication channels.

However, investigation data is often:

- Distributed across different sources
- Stored in different formats
- Unstructured and difficult to search
- Difficult to correlate manually
- Large enough to make relationship discovery time-consuming

Because of this, important connections between cases and entities may be difficult to discover using traditional manual analysis.

### Our Goal

The goal of InvestiAI is to provide a single analytical workspace where investigators can:

- Bring investigation data together
- Extract important entities from unstructured information
- Explore relationships between entities
- Analyze communication and financial patterns
- Discover unusual or recurring activity
- Ask investigation-related questions using natural language
- Generate a structured case dossier

InvestiAI is designed as a **decision-support system**. It provides analytical leads and relationships for human investigation and verification rather than automatically declaring a person guilty or criminal.

---

# 💡 Our Solution

InvestiAI follows a simple idea:

```text
Fragmented Investigation Data
            ↓
      Data Ingestion
            ↓
   NLP & Entity Extraction
            ↓
      Entity Resolution
            ↓
     Knowledge Graph
            ↓
 Graph & Pattern Analytics
            ↓
 AI Investigator Assistant
            ↓
    Structured Case Dossier

✨ Key Features
1. Multi-Source Data Integration

InvestiAI is designed to work with different types of investigation-related data such as:

*FIR / police reports
*Call Detail Records (CDR)
*Financial transactions
*Criminal case history
*Social media intelligence
*Surveillance-related records
*Locations
*Vehicle information
*Phone numbers
*Organizations
*Intelligence/watchlist information

The system brings these sources into a common analytical workflow.

2. NLP-Based Entity Extraction

Investigation reports can contain a large amount of unstructured text.

Our NLP module helps extract useful entities such as:

*Persons
*Phone numbers
*Locations
*Vehicles
*Organizations
*Bank accounts
*Crypto wallets
*Social media handles
*FIR numbers
*Other investigation-related identifiers

This extracted information can then be used for further analysis.

3. Knowledge Graph

One of the main features of InvestiAI is the Interactive Knowledge Graph.

The graph represents entities as nodes and their relationships as connections.

For example:
             Person A
             /      \
            /        \
       Phone 1      Account 1
          |             |
          |             |
       Person B       Case 102
          |
       Location X
This makes it easier to explore relationships that may not be obvious when looking at individual datasets.

4. Graph Analytics

The system can analyze the investigation network using graph-based techniques.

Examples include:

*Relationship analysis
*Centrality analysis
*Community detection
*Path finding
*Network clustering
*Important node identification
*Connection exploration

These analytical results can help investigators decide which relationships require further verification.

5. CDR Analysis

InvestiAI provides analytical support for communication records.

The system can help examine:

*Frequently communicating numbers
*Call frequency
*Call duration
*Odd-hour communication
*Repeated communication patterns
*Possible burner-phone relationships
*Communication clusters

These results are intended as investigative signals and should be verified using appropriate evidence.

6. Financial Pattern Analysis

Financial relationships can sometimes involve multiple accounts and transactions.

InvestiAI can be used to explore:

*Transaction relationships
*Repeated transfers
*Transaction networks
*Possible transaction loops
*Unusual transaction patterns
*Connected accounts

The purpose is to help investigators identify relationships and patterns that may need further investigation.

7. Social Media & Alias Intelligence

The platform can organize digital-footprint information and explore relationships between:

*Social media handles
*Suspects/entities
*Aliases
*Phone numbers
*Locations
*Other available investigation data

This can help investigators explore whether different identifiers may be connected.

8. Pattern & Anomaly Detection

InvestiAI looks for recurring or unusual patterns across investigation data.

Examples include:

*Repeated relationships between entities
*Communication bursts
*Unusual communication timings
*Repeated financial connections
*Account/phone rotation patterns
*Co-location patterns
*Network clusters
*Connected aliases

The system presents these as analytical signals rather than final conclusions.

9. AI Investigator Assistant

Investigators do not always want to manually search through multiple datasets.

InvestiAI includes an AI-assisted interface where users can ask investigation-related questions in natural language.

Example:

"Who is the kingpin candidate?"

Other examples:

"Show the most connected entities."

"Which phone numbers have frequent communication?"

"Which entities are connected to this suspect?"

"Show important relationships in this case."

The assistant helps users interact with the available analytical information more naturally.

10. Case Dossier Generator

Important investigation findings can be organized into a structured case dossier.

The dossier can contain information such as:

*Case overview
*Important entities
*Relationships
*Analytical findings
*Communication insights
*Financial insights
*Social intelligence
*Network observations

This provides a more organized way to review and share investigation findings.

🖥️ Main Modules

The project is organized into different modules for different analytical tasks.
InvestiAI
│
├── app.py
│
├── ai_assistant/
│
├── data/
│
├── engine/
│   ├── cdr_analyzer.py
│   ├── graph_builder.py
│   ├── metrics.py
│   ├── nlp_extractor.py
│   ├── pathfinder.py
│   ├── pattern_detector.py
│   └── social_media_intel.py
│
├── visualization/
│   ├── graph_renderer.py
│   ├── map_view.py
│   └── timeline_view.py
│
├── lib/
├── utils/
│
├── config.py
└── README.md
| Module                  | Purpose                                        |
| ----------------------- | ---------------------------------------------- |
| `app.py`                | Main Streamlit application                     |
| `nlp_extractor.py`      | Extracts useful information from text          |
| `graph_builder.py`      | Builds entity relationships                    |
| `cdr_analyzer.py`       | Analyzes communication records                 |
| `pattern_detector.py`   | Detects recurring and unusual patterns         |
| `pathfinder.py`         | Finds relationships/paths between entities     |
| `metrics.py`            | Performs graph/network measurements            |
| `social_media_intel.py` | Handles social-media/alias-related analysis    |
| `graph_renderer.py`     | Displays interactive graph information         |
| `map_view.py`           | Displays location-related information          |
| `timeline_view.py`      | Displays events and activity over time         |
| `app.py`                | Connects the modules into the main application |

🔄 How InvestiAI Works

The complete workflow can be understood in six major steps.

Step 1 – Data Ingestion

Investigation data is collected from supported sources and converted into a format that the system can process.

Step 2 – Information Extraction

NLP techniques are used to extract important entities and information from unstructured text.

Step 3 – Entity Linking

Related entities are connected using available identifiers and relationships.

Step 4 – Knowledge Graph Creation

The extracted entities and relationships are represented as a graph.

Step 5 – Analytics

Graph analytics, CDR analysis, financial analysis, pattern detection, and other analytical modules are applied.

Step 6 – Investigator View

The results are shown through dashboards, graphs, analytical views, the AI assistant, and the case dossier.

🧠 Technologies Used

The project is primarily built using Python and data-analysis technologies.

Core Technologies-
*Python
*Streamlit
*Pandas
*NumPy
*Natural Language Processing (NLP)
*Graph Analytics
*Machine Learning / AI-assisted analytics
*Data Visualization

Application Areas-
*Criminal network analysis
*Knowledge graphs
*Entity extraction
*Relationship analysis
*Anomaly detection
*Communication analytics
*Financial network analysis
*Social network analysis

📂 Dataset

The project can work with structured investigation-style datasets.

For development and demonstration, synthetic/sample data can be used.

Example data categories include:
Persons
Locations
FIRs
Call Detail Records
Transactions
Social Connections
Case History
Ground Truth

Important-

The demonstration dataset should contain synthetic or properly authorized data.

No real criminal records, personal phone numbers, bank details, or confidential investigation information should be uploaded to this public repository.

🖥️ Application Workflow

A typical investigation workflow in InvestiAI looks like this:
        Case Data
           ↓
    Data Processing
           ↓
   Entity Extraction
           ↓
    Entity Linking
           ↓
   Knowledge Graph
           ↓
 ┌─────────┼──────────┐
 ↓         ↓          ↓
CDR    Financial   Social Media
 ↓         ↓          ↓
 └─────────┼──────────┘
           ↓
   Pattern & Network
       Analysis
           ↓
   AI Investigator
       Assistant
           ↓
    Case Dossier

🎯 Example Use Case

Suppose an investigator is working on a case where information is available across multiple records.

For example:
Case A
 ├── Person A
 ├── Phone Number 1
 ├── Vehicle 1
 └── Location X

Case B
 ├── Person B
 ├── Phone Number 1
 ├── Account 2
 └── Location Y
The same phone number appears in both cases.

Instead of checking the records separately, InvestiAI can represent the relationship:
Person A
    |
Phone Number 1
    |
Person B
    |
Account 2
    |
Case B
This gives the investigator a connected view that can be explored further.

The relationship itself is not treated as proof of criminal activity. It is an analytical lead that requires human verification.

🌟 What Makes InvestiAI Different?

Traditional investigation workflows may look like:
Separate Data Sources
        ↓
Manual Searching
        ↓
Manual Cross-Checking
        ↓
Relationship Identification
        ↓
Investigation Report
InvestiAI aims to provide:
Multiple Data Sources
        ↓
AI + NLP Processing
        ↓
Entity Linking
        ↓
Knowledge Graph
        ↓
Pattern & Network Analytics
        ↓
AI Investigator Assistant
        ↓
Structured Case Dossier

Our USP-

InvestiAI turns fragmented investigation data into one connected, AI-powered investigative view.

🔐 Security & Responsible Use

InvestiAI is designed as an investigative decision-support platform, not an automated criminal identification system.

Important principles include:

*AI-generated insights should be verified by investigators.
*A relationship between two entities does not automatically mean criminal involvement.
*False positives are possible in automated analysis.
*Sensitive investigation data must be handled only through authorized systems.
*Real personal data should not be used in public demonstrations.
*Access control and secure data handling should be implemented before real-world deployment.
*Final investigative decisions should remain with authorized human professionals.

⚠️ Limitations

The current project is a prototype and demonstration platform.

Some limitations include:

*Results depend on the quality of available data.
*Synthetic/demo datasets may not represent all real investigation scenarios.
*Entity matching can produce false or incomplete relationships.
*AI-assisted analysis can generate incorrect interpretations.
*Real-world deployment would require stronger security and access controls.
*Integration with government or law-enforcement systems would require proper authorization and technical compliance.

🔮 Future Scope

The project can be extended in several directions.

1. Advanced Entity Resolution

Improve matching of the same entity across different datasets, even when names, identifiers, or spellings are different.

2. Real-Time Data Processing

Support continuous ingestion and analysis of new investigation records.

3. Advanced Graph Intelligence

Add more advanced graph algorithms for:

*Community detection
*Influence analysis
*Relationship prediction
*Multi-hop relationship discovery
4. Improved NLP

Support multilingual investigation documents and more advanced document-level entity and relationship extraction.

5. Secure Deployment

Introduce:

*Role-based access control
*Authentication
*Audit logs
*Encryption
*Secure API communication
6. Authorized System Integration

The platform could potentially be integrated with authorized law-enforcement systems in the future, subject to access, security, legal, and organizational requirements.

📚 Research Areas

The project is based on research areas including:

*Graph-Based Criminal Network Analysis
*Natural Language Processing for Information Extraction
*Anomaly Detection
*Social Network and Community Analysis

Some useful research references:

1. Graph and Network Theory for the Analysis of Criminal Networks
https://arxiv.org/abs/2103.02504

2. A Survey on Open Information Extraction: From Rule-based Model to Large Language Model
https://aclanthology.org/2024.findings-emnlp.560/

3. Financial Fraud: A Review of Anomaly Detection Techniques and Recent Advances
https://doi.org/10.1016/j.eswa.2021.116429

4. Community Detection in Social Networks Using Machine Learning: A Systematic Mapping Study
https://link.springer.com/article/10.1007/s10115-024-02201-8

🏛️ Government / Domain References

The project is developed in the context of publicly available information and potential future integration with authorized systems.

Relevant domain sources include:

1. National Crime Records Bureau (NCRB)
https://ncrb.gov.in/

2.Crime in India – data.gov.in
https://www.data.gov.in/catalog/crime-india-2023

3.National Cyber Crime Reporting Portal
https://www.cybercrime.gov.in/

4.Ministry of Home Affairs – CCTNS
https://www.mha.gov.in/en/divisionofmha/women-safety-division/cctns

These references provide domain context. InvestiAI is an independent project and is not officially affiliated with or connected to these government systems.

⭐ Project Summary

InvestiAI brings together fragmented investigation data and converts it into a connected analytical view.
FIRs
CDRs
Financial Data
Social Intelligence
Case History
Locations
      ↓
   InvestiAI
      ↓
NLP + Entity Extraction
      ↓
Knowledge Graph
      ↓
Pattern & Network Analysis
      ↓
AI Investigator Assistant
      ↓
Structured Case Dossier

One Case. Multiple Data Sources. One Connected Intelligence View.


