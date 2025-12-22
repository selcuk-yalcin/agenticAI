# System Architecture - AI-Powered Incident Investigation

## Overview

This document describes the architecture of the AI-powered incident investigation system designed for high-risk industries. The system follows a **multi-agent architecture** where specialized agents collaborate to analyze incidents, identify root causes, and generate comprehensive reports.

## Architectural Principles

1. **Modularity**: Each agent has a single, well-defined responsibility
2. **Scalability**: Agents can be deployed independently and scaled based on load
3. **Extensibility**: New agents and frameworks can be added without disrupting existing functionality
4. **Security**: Data encryption, access control, and audit trails at every layer
5. **Standards Compliance**: Built-in support for OSHA, Seveso III, NFPA, API RP, and ISO standards

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                     │
│  (Web App, Mobile App, API, Document Upload Portal)         │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  Orchestrator Agent                          │
│  - Workflow Management                                       │
│  - Agent Coordination                                        │
│  - Quality Assurance                                         │
└──┬────┬────┬────┬────┬────┬────────────────────────────────┘
   │    │    │    │    │    │
   ▼    ▼    ▼    ▼    ▼    ▼
┌──────┬────────┬──────────┬────────────┬──────────────┐
│Evidence│Root    │Knowledge │Diagram    │Report       │
│Analyzer│Cause   │Base      │Generator  │Generator    │
│        │Analyzer│Agent     │           │             │
└────────┴────────┴──────────┴───────────┴─────────────┘
   │        │         │            │            │
   ▼        ▼         ▼            ▼            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Core Services Layer                      │
│  - Evidence Processing  - Taxonomy Engine                    │
│  - OCR & Vision        - Diagram Builders                    │
│  - NLP Engine          - Report Templates                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                     Data Layer                               │
│  - Vector Database (Semantic Search)                         │
│  - Document Store (Evidence, Reports)                        │
│  - Knowledge Base (CSB, HSE, OSHA Cases)                     │
│  - Case Database (PostgreSQL)                                │
└─────────────────────────────────────────────────────────────┘
```

## Agent Descriptions

### 1. Orchestrator Agent

**Purpose**: Master coordinator for the entire investigation workflow

**Responsibilities**:
- Receive investigation requests and create new cases
- Route evidence to appropriate processing agents
- Coordinate agent execution in correct sequence
- Manage investigation state and progress tracking
- Perform quality checks on agent outputs
- Handle errors and retry failed operations
- Generate final deliverables

**Key Methods**:
```python
create_investigation(incident_details)
add_evidence(case_id, evidence_data)
run_investigation(case_id)
get_investigation_status(case_id)
generate_deliverables(case_id, format)
```

**Technology**: LangChain orchestration, State machine pattern

---

### 2. Evidence Analysis Agent

**Purpose**: Process and extract insights from all evidence types

**Responsibilities**:
- **Text Analysis**: Process witness statements, reports, emails using NLP
- **Document Analysis**: Extract information from PDFs, Word docs, Excel sheets
- **Image Analysis**: Analyze photos, sketches, diagrams using vision models
- **Drawing Analysis**: Interpret P&ID drawings, facility layouts, equipment diagrams
- **Log Analysis**: Parse SCADA logs, alarm histories, system logs
- **Video Analysis**: Extract frames and analyze video evidence
- Identify key facts, timelines, and inconsistencies
- Create structured evidence summaries

**Input Types**:
- Witness statements (text, audio transcripts)
- P&ID and technical drawings
- HAZOP reports, audit reports, risk assessments
- Photos and videos
- Equipment logs and sensor data
- Inspection checklists and forms

**Output**:
```json
{
  "evidence_id": "EVD-001",
  "type": "witness_statement",
  "key_facts": [...],
  "timeline_events": [...],
  "entities_mentioned": [...],
  "inconsistencies": [...],
  "confidence_score": 0.85
}
```

**Technology**: GPT-4o Vision, Tesseract OCR, spaCy NER, PyPDF2

---

### 3. Root Cause Analysis Agent

**Purpose**: Identify immediate, contributing, and systemic causes

**Responsibilities**:
- Apply structured root cause frameworks:
  - **CCPS Guidelines**: Human factors, organizational factors, technical failures
  - **TapRoot®**: Systematic cause analysis using decision trees
  - **DNV ICAM**: Incident Cause Analysis Method
- Map causes to standardized taxonomies
- Distinguish between:
  - **Immediate causes**: Direct triggers (equipment failure, human error)
  - **Contributing factors**: Conditions enabling the incident
  - **Systemic causes**: Organizational and design-level failures
  - **Latent conditions**: Long-standing weaknesses
- Calculate cause confidence scores
- Identify causal chains and relationships

**Frameworks Integrated**:
1. **CCPS Framework**:
   - Equipment/Material factors
   - Human/Personnel factors
   - Organizational/Management factors
   - External factors

2. **TapRoot® Categories**:
   - Management System
   - Human Performance
   - Equipment/Components
   - Work Direction
   - Quality Control

3. **5M+E (Custom)**:
   - Man (Human factors)
   - Machine (Equipment)
   - Material (Substances)
   - Method (Procedures)
   - Measurement (Monitoring)
   - Environment
   - Management

**Output**:
```json
{
  "immediate_causes": [
    {
      "cause": "Pressure relief valve failed to open",
      "category": "Equipment failure",
      "confidence": 0.92,
      "evidence_refs": ["EVD-003", "EVD-007"]
    }
  ],
  "contributing_factors": [...],
  "systemic_causes": [...],
  "causal_chain": [...]
}
```

**Technology**: LLM reasoning, Rule-based classification, Decision trees

---

### 4. Knowledge Base Agent

**Purpose**: Retrieve similar incidents and lessons learned

**Responsibilities**:
- Maintain vector database of historical incidents
- Perform semantic search across:
  - CSB investigation reports
  - HSE UK incident database
  - OSHA case files
  - Company-specific historical cases
  - Technical literature (CCPS books, API standards)
- Find similar incidents based on:
  - Industry sector
  - Equipment type
  - Failure mode
  - Root causes
- Extract lessons learned and best practices
- Suggest preventive measures from past cases

**Knowledge Sources**:
- **CSB Reports**: 400+ major chemical incidents (1990-2024)
- **HSE UK**: Mining, offshore, manufacturing incidents
- **OSHA**: Process safety violations and citations
- **NTSB**: Transportation-related incidents
- **Company Archives**: Client-specific historical data
- **Technical Standards**: API, NFPA, ASME, ISO documents

**Search Methods**:
- Semantic similarity (vector embeddings)
- Keyword/metadata filtering
- Causal pattern matching
- Equipment taxonomy matching

**Output**:
```json
{
  "similar_cases": [
    {
      "case_id": "CSB-2019-05",
      "title": "Williams Olefins Plant Explosion",
      "similarity_score": 0.87,
      "common_factors": ["pressure relief failure", "inadequate inspection"],
      "lessons_learned": [...],
      "url": "https://www.csb.gov/..."
    }
  ],
  "best_practices": [...],
  "regulatory_citations": [...]
}
```

**Technology**: ChromaDB/Pinecone, Sentence-transformers, RAG pipeline

---

### 5. Visual Diagram Generator Agent

**Purpose**: Create analytical diagrams for root cause visualization

**Responsibilities**:
- Generate multiple diagram types:

**5 Why Analysis**:
```
Why did the explosion occur?
└─ Because flammable vapor ignited
   └─ Why was there flammable vapor?
      └─ Because the relief valve vented to atmosphere
         └─ Why did it vent to atmosphere?
            └─ Because flare system was isolated
               └─ Why was it isolated?
                  └─ ROOT: Inadequate permit-to-work system
```

**Fishbone (Ishikawa) Diagram**:
```
                    Man              Machine
                     │                  │
         Training ───┤      Failed  ────┤
         Inadequate  │      Relief      │
                     │      Valve       │
                     └──────┬───────────┘
                            │
                     ┌──────┴───────────┐
                     │   EXPLOSION      │
                     └──────┬───────────┘
                     ┌──────┴───────────┐
                     │                  │
        Procedure ───┤      Isolated ───┤
        Not Followed │      Flare       │
                     │      System      │
                   Method           Environment
```

**Fault Tree Analysis (FTA)**:
- Top-down deductive analysis
- Logic gates (AND, OR)
- Basic events and intermediate events
- Quantitative probability calculations

**Event Tree Analysis (ETA)**:
- Bottom-up consequence analysis
- Success/failure paths for safety barriers
- Probability-weighted outcomes

**Bowtie Diagram**:
- Central hazard (e.g., "Loss of containment")
- Left side: Preventive barriers
- Right side: Mitigative barriers
- Threats and consequences

**Output Formats**:
- PNG images
- SVG (scalable)
- PDF (for reports)
- Graphviz DOT files

**Technology**: Graphviz, matplotlib, Pillow, networkx

---

### 6. Report Generation Agent

**Purpose**: Create comprehensive investigation reports

**Responsibilities**:
- Compile all investigation findings
- Apply regulatory-compliant templates:
  - **OSHA PSM** (29 CFR 1910.119) format
  - **Seveso III** (EU Major Accident Directive)
  - **NFPA 921** (Fire investigation)
  - **API RP 754** (Process safety indicators)
  - **ISO 45001** (OH&S management)
  - Custom company templates
- Structure reports with sections:
  1. Executive Summary
  2. Incident Description
  3. Investigation Team and Methodology
  4. Timeline of Events
  5. Evidence Summary
  6. Root Cause Analysis
  7. Contributing and Systemic Factors
  8. Visual Analysis (diagrams)
  9. Similar Incidents and Lessons Learned
  10. Corrective and Preventive Actions (CAPA)
  11. Recommendations (prioritized)
  12. Appendices (evidence, references)
- Generate outputs in Word (.docx), PDF, Excel
- Support multi-language reports (English, Turkish, Spanish, etc.)

**Template Customization**:
- Industry-specific sections (e.g., offshore vs. refinery)
- Company branding and formatting
- Regulatory requirement mapping

**Output**:
- Professional Word document with:
  - Table of contents
  - Embedded diagrams
  - Evidence references
  - Formatted tables and charts
- PDF for distribution
- Excel spreadsheet for CAPA tracking

**Technology**: python-docx, ReportLab, Jinja2 templates

---

### 7. Recommendation Agent

**Purpose**: Propose corrective and preventive actions

**Responsibilities**:
- Generate recommendations based on:
  - Root causes identified
  - Industry best practices
  - Similar incident learnings
  - Regulatory requirements
- Categorize recommendations:
  - **Immediate**: Stop further incidents
  - **Short-term**: Implement within 30 days
  - **Long-term**: Strategic improvements
- Prioritize by:
  - **Criticality**: Severity of risk
  - **Feasibility**: Cost and complexity
  - **Effectiveness**: Impact on risk reduction
- Map recommendations to:
  - Hierarchy of controls (elimination, substitution, engineering, admin, PPE)
  - Responsible parties
  - Implementation timelines
  - Success metrics

**Recommendation Types**:
- **Technical**: Equipment upgrades, design changes
- **Procedural**: New/revised procedures, checklists
- **Training**: Competency development, refresher courses
- **Organizational**: Management system improvements
- **Monitoring**: New inspection/testing regimes

**Output**:
```json
{
  "recommendations": [
    {
      "id": "REC-001",
      "title": "Replace all pressure relief valves",
      "category": "technical",
      "priority": "high",
      "timeline": "immediate",
      "cost_estimate": "$50,000",
      "responsible_party": "Maintenance Manager",
      "success_criteria": "100% PRV replacement completed",
      "regulatory_driver": "OSHA PSM Element 8"
    }
  ]
}
```

**Technology**: LLM reasoning, Cost-benefit analysis, Priority matrices

---

## Data Flow

### Investigation Workflow

```
1. Create Investigation
   ↓
2. Upload Evidence → Evidence Analysis Agent
   ↓
3. Extract Facts & Timeline
   ↓
4. Root Cause Analysis Agent ← Knowledge Base Agent
   ↓                             (retrieve similar cases)
5. Identify Causes (Immediate, Contributing, Systemic)
   ↓
6. Generate Diagrams ← Diagram Generator Agent
   ↓
7. Develop Recommendations ← Recommendation Agent
   ↓
8. Compile Report ← Report Generation Agent
   ↓
9. Review & Approve (Human oversight)
   ↓
10. Finalize & Distribute
```

### Data Storage

**PostgreSQL** (Structured Data):
- Investigation cases
- User accounts and permissions
- Audit logs
- CAPA tracking

**Vector Database** (Semantic Search):
- Embedded historical incidents
- Technical literature chunks
- Standards and regulations

**Object Storage** (S3/MinIO):
- Evidence files (images, PDFs, videos)
- Generated reports
- Diagram outputs

**File System**:
- Templates
- Configuration files
- Taxonomy definitions

---

## Security Architecture

### Authentication & Authorization
- **SSO Integration**: SAML 2.0, OAuth 2.0
- **Role-Based Access Control (RBAC)**:
  - Investigator: Create cases, upload evidence
  - Reviewer: Review findings, approve reports
  - Admin: System configuration, user management
  - Auditor: Read-only access to all cases

### Data Protection
- **Encryption at Rest**: AES-256 for all stored data
- **Encryption in Transit**: TLS 1.3 for all communications
- **Tokenization**: Sensitive PII tokenized in database
- **Data Masking**: Automatic redaction of confidential info in reports

### Compliance
- **Audit Trail**: Immutable log of all system actions
- **Data Retention**: Configurable policies per jurisdiction
- **Privacy**: GDPR, CCPA compliant
- **Attorney-Client Privilege**: Special handling for legal investigations

---

## Scalability & Performance

### Horizontal Scaling
- **Agent Pods**: Each agent type deployed in Kubernetes
- **Load Balancing**: Distribute evidence processing across multiple instances
- **Queue-Based Processing**: RabbitMQ/Celery for async tasks

### Performance Optimization
- **Caching**: Redis for frequently accessed data
- **Lazy Loading**: Stream large evidence files
- **Batch Processing**: Process multiple cases in parallel
- **GPU Acceleration**: For vision and NLP models

### Monitoring
- **Application Monitoring**: Prometheus + Grafana
- **LLM Usage Tracking**: Token consumption, cost analysis
- **Error Tracking**: Sentry for exception monitoring
- **Performance Metrics**: Response times, throughput

---

## Technology Stack Summary

| Layer | Technology |
|-------|-----------|
| LLM | OpenAI GPT-4o, GPT-4o-mini |
| Framework | LangChain, LlamaIndex |
| Vector DB | ChromaDB, Pinecone |
| Database | PostgreSQL, Redis |
| Storage | MinIO (S3-compatible) |
| OCR | Tesseract, GPT-4 Vision |
| NLP | spaCy, Sentence-transformers |
| Diagrams | Graphviz, matplotlib |
| Reports | python-docx, ReportLab |
| Backend | FastAPI, Celery |
| Frontend | React, TypeScript |
| Infrastructure | Kubernetes, Docker |
| Monitoring | Prometheus, Grafana, Sentry |

---

## Deployment Architecture

### Cloud Deployment (AWS Example)

```
┌─────────────────────────────────────────────────────────────┐
│                     CloudFront (CDN)                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              Application Load Balancer                       │
└──┬────────────────────────────────────────────────────────┬─┘
   │                                                          │
   ▼                                                          ▼
┌─────────────────┐                                  ┌──────────────┐
│   EKS Cluster   │                                  │  API Gateway │
│  (Agent Pods)   │                                  │   (REST API) │
└────────┬────────┘                                  └──────┬───────┘
         │                                                  │
         ▼                                                  ▼
┌─────────────────────────────────────────────────────────────┐
│                     RDS PostgreSQL                           │
│                     ElastiCache Redis                        │
│                     S3 (Evidence Storage)                    │
│                     OpenSearch (Vector DB)                   │
└─────────────────────────────────────────────────────────────┘
```

### On-Premises Deployment

For organizations with data sovereignty requirements:
- Kubernetes on bare metal or VMware
- Self-hosted PostgreSQL cluster
- Local object storage (MinIO)
- Air-gapped LLM deployment (GPT-4 alternatives: LLaMA, Mistral)

---

## Future Enhancements

1. **Predictive Analytics**: Use ML to predict incident probability
2. **Real-Time Monitoring Integration**: Connect to plant DCS/SCADA for live alerts
3. **Mobile Evidence Collection**: iOS/Android apps for field investigators
4. **Collaborative Platform**: Multi-user simultaneous editing
5. **Industry-Specific Models**: Fine-tuned LLMs for refineries, mining, etc.
6. **Advanced Computer Vision**: 3D reconstruction from photos, damage assessment
7. **Natural Language Querying**: "Show me all valve failures in 2023"
8. **Blockchain Audit Trail**: Immutable investigation records

---

## Conclusion

This architecture provides a robust, scalable, and secure foundation for AI-powered incident investigation. The multi-agent design ensures modularity and extensibility while maintaining compliance with industry standards and regulations.
