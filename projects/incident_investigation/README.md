# AI-Powered Incident Investigation System

## Project Overview

This is an enterprise-grade AI-powered incident investigation software designed for high-risk industries including:
- Oil & Gas
- Petrochemicals
- Energy & Utilities
- Mining
- Defense & Military-Industrial
- Manufacturing

The system assists investigation teams in identifying visible and systemic causes of incidents and generating comprehensive, standards-aligned reports.

## Key Features

### 1. Multi-Source Data Analysis
- **Witness Statements**: Natural language processing of testimonies
- **Technical Drawings**: P&ID (Piping and Instrumentation Diagrams) analysis
- **Safety Reports**: HAZOP, audits, inspections, risk assessments
- **Visual Evidence**: Images, sketches, photos, video footage
- **Physical Evidence**: Equipment failure data, material analysis
- **Electronic Records**: SCADA logs, alarm histories, maintenance records

### 2. Root Cause Analysis Framework
Based on industry-leading methodologies:
- **CCPS Guidelines** (AIChE Guidelines for Investigating Process Safety Incidents)
- **TapRoot® Root Cause Map™**
- **DNV Incident Cause Analysis Method (ICAM)**
- Custom taxonomies for specific industries

Classification includes:
- Immediate causes (unsafe acts, procedural violations)
- Contributing factors (environmental, equipment-related)
- Systemic causes (organizational failures, design flaws)
- Latent conditions (management system weaknesses)

### 3. Visual Analysis Tools
Automatically generates:
- **5 Why Analysis**: Iterative root cause drilling
- **Ishikawa (Fishbone) Diagrams**: Categorical cause mapping
- **Fault Tree Analysis (FTA)**: Top-down deductive failure analysis
- **Event Tree Analysis (ETA)**: Bottom-up consequence analysis
- **Bowtie Diagrams**: Combined preventive and mitigative barrier analysis
- **Timeline Diagrams**: Chronological event sequences

### 4. Knowledge Base Integration
Incorporates data from:
- **CSB (US Chemical Safety Board)** investigation reports
- **HSE UK** incident databases
- **OSHA** case studies and violations
- **NTSB** transportation incident reports
- Technical literature and guidelines
- Company-specific historical cases

### 5. Standards Compliance
Aligned with:
- OSHA 29 CFR 1910.119 (Process Safety Management)
- Seveso III Directive (EU Major Accident Hazards)
- NFPA 921 (Fire and Explosion Investigations)
- API RP 754 (Process Safety Performance Indicators)
- ISO 45001 (Occupational Health and Safety Management)
- ISO 31000 (Risk Management)
- Company-specific investigation protocols

### 6. Automated Report Generation
Creates comprehensive reports including:
- Executive summaries
- Detailed investigation findings
- Root cause analysis results
- Corrective and preventive actions (CAPA)
- Timeline of events
- Visual diagrams
- Regulatory compliance documentation

Output formats: Word (.docx), PDF, Excel

### 7. Multi-Language Support
- English (primary)
- Turkish
- Spanish
- French
- German
- Extensible for additional languages

## System Architecture

### Agent-Based Design

The system uses multiple specialized AI agents coordinated by an orchestrator:

1. **Evidence Analysis Agent**
   - Processes all input data types
   - Extracts key facts and findings
   - Identifies inconsistencies

2. **Root Cause Analysis Agent**
   - Applies structured frameworks
   - Maps causes to taxonomy
   - Identifies contributing and systemic factors

3. **Knowledge Base Agent**
   - Semantic search across historical cases
   - Retrieves similar incidents
   - Suggests learnings from past investigations

4. **Visual Diagram Generator Agent**
   - Creates analytical diagrams
   - Generates causal maps
   - Produces timeline visualizations

5. **Report Generation Agent**
   - Compiles findings into structured reports
   - Ensures regulatory compliance
   - Formats outputs for stakeholders

6. **Recommendation Agent**
   - Proposes corrective actions
   - Prioritizes by criticality and feasibility
   - Aligns with industry best practices

7. **Orchestrator Agent**
   - Coordinates all agents
   - Manages workflow
   - Ensures quality and completeness

## Technology Stack

- **LLM**: OpenAI GPT-4o / GPT-4o-mini (multimodal)
- **Vector Database**: ChromaDB / Pinecone for semantic search
- **OCR**: Tesseract / GPT-4 Vision for document/image analysis
- **Diagram Generation**: Graphviz, matplotlib, Pillow
- **Report Generation**: python-docx, ReportLab
- **Framework**: LangChain / LlamaIndex
- **Backend**: FastAPI
- **Frontend**: React (Admin panel from this workspace)

## Use Cases

### Example 1: Refinery Fire Investigation
1. Upload witness statements, P&IDs, alarm logs
2. System analyzes sequence of events
3. Identifies failed safety barriers
4. Generates Bowtie diagram showing preventive/mitigative controls
5. Produces report aligned with OSHA PSM requirements

### Example 2: Mining Equipment Failure
1. Input maintenance records, failure photos, operator interviews
2. System compares with similar historical incidents
3. Identifies design flaw and inadequate inspection procedures
4. Recommends corrective actions with priority ranking
5. Generates FTA showing failure pathways

### Example 3: Chemical Plant Near-Miss
1. Analyze HAZOP reports, operator actions, control room logs
2. Identifies precursor signals and weak defenses
3. Maps organizational factors (training, procedures, culture)
4. Creates 5 Why and Fishbone diagrams
5. Proposes preventive measures

## Getting Started

### Installation

```bash
cd projects/incident_investigation
pip install -r requirements.txt
```

### Configuration

Copy the example environment file and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` file and set your configuration:
```env
# Required
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4o

# Optional - for advanced features
PINECONE_API_KEY=your-pinecone-key
DATABASE_URL=postgresql://user:password@localhost/incident_db
```

### Quick Start

```python
from incident_investigation import IncidentOrchestrator
from incident_investigation.config import config

# Validate configuration (checks for API keys)
config.validate()

# Initialize system
orchestrator = IncidentOrchestrator()

# Start new investigation
case = orchestrator.create_investigation({
    "incident_id": "INC-2024-001",
    "industry": "petrochemical",
    "incident_type": "fire",
    "severity": "major"
})

# Upload evidence
case.add_evidence(
    type="witness_statement",
    file_path="./evidence/operator_statement.pdf"
)
case.add_evidence(
    type="pid_drawing",
    file_path="./evidence/unit_drawing.pdf"
)

# Run investigation
results = orchestrator.investigate(case_id=case.id)

# Generate report
report = orchestrator.generate_report(
    case_id=case.id,
    format="pdf",
    standard="OSHA_PSM"
)
```

## Project Structure

```
incident_investigation/
├── README.md
├── ARCHITECTURE.md
├── WORKFLOW.md
├── requirements.txt
├── agents/
│   ├── evidence_analyzer.py
│   ├── root_cause_analyzer.py
│   ├── knowledge_base_agent.py
│   ├── diagram_generator.py
│   ├── report_generator.py
│   ├── recommendation_agent.py
│   └── orchestrator.py
├── core/
│   ├── taxonomies/
│   │   ├── ccps_framework.py
│   │   ├── taproot_map.py
│   │   └── custom_taxonomy.py
│   ├── evidence_processor.py
│   ├── diagram_builders/
│   │   ├── five_why.py
│   │   ├── fishbone.py
│   │   ├── fault_tree.py
│   │   ├── event_tree.py
│   │   └── bowtie.py
│   └── report_templates/
├── data/
│   ├── knowledge_base/
│   │   ├── csb_reports/
│   │   ├── hse_uk_reports/
│   │   ├── osha_cases/
│   │   └── company_cases/
│   └── vector_db/
├── tests/
│   ├── test_evidence_analyzer.py
│   ├── test_root_cause_analyzer.py
│   ├── test_diagram_generator.py
│   └── test_orchestrator.py
└── examples/
    └── sample_investigation.py
```

## Security and Compliance

- **Data Privacy**: All incident data encrypted at rest and in transit
- **Access Control**: Role-based access (investigators, reviewers, admins)
- **Audit Trail**: Complete logging of all system actions
- **Regulatory Compliance**: SOC 2, ISO 27001 aligned
- **Legal Privilege**: Attorney-client privilege protection options

## Roadmap

### Phase 1 (Current)
- Core agent development
- Basic evidence analysis
- Root cause framework implementation

### Phase 2
- Advanced visual diagram generation
- Multi-language support
- Mobile evidence collection app

### Phase 3
- Predictive analytics for incident prevention
- Real-time monitoring integration
- Advanced machine learning for pattern detection

### Phase 4
- Industry-specific customization packages
- API for third-party integrations
- Collaborative investigation platform

## License

Proprietary - Enterprise License Required

## Support

For technical support, training, or customization:
- Email: support@incident-ai.com
- Documentation: https://docs.incident-ai.com
- Training Portal: https://training.incident-ai.com

## Contributors

Development Team:
- AI/ML Engineering
- Process Safety Experts
- Regulatory Compliance Specialists
- UX/UI Designers
