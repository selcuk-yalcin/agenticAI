# Investigation Workflow - AI-Powered Incident Investigation System

## Overview

This document describes the end-to-end workflow for conducting an incident investigation using the AI-powered system. The workflow follows industry best practices and regulatory requirements (OSHA PSM, Seveso III, API RP 754).

## Investigation Phases

### Phase 1: Investigation Initiation
### Phase 2: Evidence Collection
### Phase 3: Analysis and Root Cause Determination
### Phase 4: Recommendation Development
### Phase 5: Report Generation and Review
### Phase 6: Implementation and Follow-up

---

## Phase 1: Investigation Initiation

### 1.1 Incident Notification

**Trigger**: Major incident, near-miss, or process safety event

**Actions**:
1. Incident is reported to investigation team
2. Initial severity assessment conducted
3. Investigation scope defined based on:
   - Actual consequences (injuries, environmental impact, property damage)
   - Potential consequences (worst case scenario)
   - Regulatory requirements

**System Actions**:
```python
# Create new investigation case
orchestrator = IncidentOrchestrator()

case = orchestrator.create_investigation({
    "incident_id": "INC-2024-012",
    "date_occurred": "2024-12-15T14:30:00Z",
    "location": "Refinery Unit 3 - Crude Distillation",
    "industry": "oil_and_gas",
    "facility_type": "refinery",
    "incident_type": "fire",
    "severity": "major",  # minor, moderate, major, catastrophic
    "actual_consequences": {
        "injuries": 2,
        "fatalities": 0,
        "property_damage_usd": 500000,
        "environmental_release": True
    },
    "regulatory_notification_required": True,
    "standards_applicable": ["OSHA_PSM", "API_RP_754", "NFPA_921"]
})

print(f"Investigation case created: {case.id}")
```

**Output**:
- Case ID assigned
- Investigation team notified
- Evidence upload portal activated
- Timeline tracker initiated

---

### 1.2 Team Assembly

**Investigation Team Roles**:
- **Lead Investigator**: Overall responsibility
- **Technical Experts**: Process, mechanical, electrical, instrumentation
- **Safety Representatives**: HSE perspective
- **Operations Representatives**: Operational knowledge
- **External Experts**: Independent review (if required)

**System Support**:
- Assign roles and permissions
- Create collaboration workspace
- Set up secure document sharing

---

## Phase 2: Evidence Collection

### 2.1 Evidence Types and Sources

**Physical Evidence**:
- Failed equipment and components
- Material samples
- Debris and remnants

**Documentary Evidence**:
- Operating procedures (SOPs)
- Maintenance records
- Training records
- Inspection and test reports
- HAZOP studies
- Risk assessments
- Previous audit findings
- Process safety information (PSI)

**Electronic Evidence**:
- SCADA/DCS logs
- Alarm histories
- Video surveillance footage
- Control system configurations
- Email communications
- Shift logs

**Human Evidence**:
- Witness statements
- Operator interviews
- Subject matter expert opinions

**Visual Evidence**:
- Incident scene photographs
- Pre/post-incident comparisons
- P&ID drawings
- Facility layout diagrams
- Equipment sketches

---

### 2.2 Evidence Upload and Processing

**Upload Process**:

```python
# Upload witness statement
case.add_evidence(
    evidence_type="witness_statement",
    file_path="./evidence/operator_interview_001.pdf",
    metadata={
        "witness_name": "John Smith",
        "role": "Control Room Operator",
        "date_collected": "2024-12-16",
        "interviewer": "Lead Investigator"
    }
)

# Upload P&ID drawing
case.add_evidence(
    evidence_type="pid_drawing",
    file_path="./evidence/unit3_pid_sheet5.pdf",
    metadata={
        "drawing_number": "P-1234-05",
        "revision": "C",
        "system": "Overhead condensing system"
    }
)

# Upload HAZOP report
case.add_evidence(
    evidence_type="hazop_report",
    file_path="./evidence/hazop_unit3_2022.pdf",
    metadata={
        "study_date": "2022-06-15",
        "scope": "Unit 3 Full Revalidation"
    }
)

# Upload incident photos
case.add_evidence(
    evidence_type="photo",
    file_path="./evidence/damage_photos/IMG_001.jpg",
    metadata={
        "date_taken": "2024-12-15",
        "photographer": "Safety Inspector",
        "description": "Fire damage to vessel V-301"
    }
)

# Upload SCADA logs
case.add_evidence(
    evidence_type="scada_log",
    file_path="./evidence/scada_export_20241215.csv",
    metadata={
        "time_range": "2024-12-15 14:00:00 to 15:00:00",
        "tags_included": ["TI-301", "PI-302", "FI-303"],
        "export_format": "CSV"
    }
)
```

**Evidence Processing Pipeline**:

```
Upload → Evidence Analysis Agent → Extract Facts → Create Timeline
```

**Agent Actions**:
1. **Text Extraction** (if PDF/scan): OCR processing
2. **Entity Recognition**: Identify people, equipment, chemicals, locations
3. **Fact Extraction**: Key statements and observations
4. **Timeline Construction**: Chronological event sequence
5. **Inconsistency Detection**: Flag contradictions between sources
6. **Linkage**: Connect related evidence items

**Example Output**:

```json
{
  "evidence_id": "EVD-001",
  "type": "witness_statement",
  "status": "processed",
  "key_facts": [
    "Operator noticed high temperature alarm at 14:28",
    "Manual valve HV-305 was found in closed position",
    "Cooling water flow was stopped approximately 10 minutes before alarm"
  ],
  "timeline_events": [
    {
      "time": "2024-12-15T14:18:00Z",
      "event": "Cooling water isolation valve closed",
      "source": "Witness statement - Operator",
      "confidence": 0.85
    },
    {
      "time": "2024-12-15T14:28:00Z",
      "event": "High temperature alarm activated",
      "source": "Witness statement + SCADA log",
      "confidence": 0.95
    }
  ],
  "entities": {
    "people": ["John Smith - Operator", "Mike Johnson - Supervisor"],
    "equipment": ["HV-305 valve", "V-301 vessel", "TI-301 temperature indicator"],
    "chemicals": ["Crude oil", "Cooling water"]
  },
  "contradictions": []
}
```

---

## Phase 3: Analysis and Root Cause Determination

### 3.1 Timeline Development

**Objective**: Create comprehensive chronological sequence of events

**Process**:
1. Aggregate all timeline events from evidence
2. Resolve time conflicts
3. Identify critical decision points
4. Mark barrier failures

**System Action**:

```python
# Generate integrated timeline
timeline = orchestrator.generate_timeline(case.id)

# Timeline includes:
# - Precursor events (hours/days before incident)
# - Immediate sequence (minutes before/during incident)
# - Response actions (during and after incident)
# - Recovery activities
```

**Timeline Output**:

```
T-2 hours:  Maintenance started on cooling water pump P-302
T-1 hour:   Cooling water flow reduced to 50% capacity
T-30 min:   Operator acknowledged low flow alarm (failed to investigate)
T-10 min:   Manual valve HV-305 inadvertently closed during rounds
T-0:        Temperature exceeded safe limit - Fire initiated
T+2 min:    Emergency shutdown activated
T+5 min:    Fire suppression system triggered
T+15 min:   Fire extinguished
```

---

### 3.2 Root Cause Analysis

**Objective**: Identify immediate, contributing, and systemic causes

**Process Flow**:

```
Evidence → Root Cause Analysis Agent → Apply Frameworks → Classify Causes
```

**Step 1: Apply CCPS Framework**

```python
# Run root cause analysis
rca_results = orchestrator.run_root_cause_analysis(
    case_id=case.id,
    frameworks=["CCPS", "TapRoot", "5M_E"]
)
```

**CCPS Analysis Output**:

```json
{
  "immediate_causes": [
    {
      "cause": "Cooling water flow to V-301 was stopped",
      "category": "Equipment/Material - Valve misposition",
      "evidence": ["EVD-001", "EVD-007"],
      "confidence": 0.95
    },
    {
      "cause": "Temperature monitoring alarm was not responded to",
      "category": "Human/Personnel - Procedural non-compliance",
      "evidence": ["EVD-001", "EVD-003"],
      "confidence": 0.88
    }
  ],
  "contributing_factors": [
    {
      "factor": "Valve HV-305 not clearly labeled",
      "category": "Equipment - Design deficiency",
      "impact": "medium"
    },
    {
      "factor": "Low flow alarm was frequently nuisance alarm",
      "category": "Organizational - Alarm management inadequate",
      "impact": "high"
    },
    {
      "factor": "No written procedure for valve lineup during maintenance",
      "category": "Organizational - Procedure deficiency",
      "impact": "high"
    }
  ],
  "systemic_causes": [
    {
      "cause": "Management of Change (MOC) process not followed for maintenance",
      "category": "Organizational - Management system failure",
      "standard_violated": "OSHA PSM Element 8 - Management of Change",
      "severity": "critical"
    },
    {
      "cause": "Inadequate training on cooling system operation",
      "category": "Organizational - Training deficiency",
      "standard_violated": "OSHA PSM Element 9 - Training",
      "severity": "major"
    },
    {
      "cause": "Mechanical integrity program did not include valve position verification",
      "category": "Organizational - Asset management deficiency",
      "standard_violated": "OSHA PSM Element 11 - Mechanical Integrity",
      "severity": "major"
    }
  ]
}
```

**Step 2: TapRoot® Analysis**

Uses decision tree approach to systematically drill down:

```
Equipment Problem?
  └─ Yes → Equipment Design Problem?
            └─ No → Equipment Operation Problem?
                      └─ Yes → Valve Position Error
                                └─ Work Direction Problem?
                                      └─ Yes → Procedure Not Adequate
```

**Step 3: 5M+E Analysis (Fishbone)**

Categories:
- **Man**: Operator did not verify valve position
- **Machine**: Valve labeling inadequate
- **Method**: No procedure for valve lineup
- **Material**: N/A
- **Measurement**: Alarm system had nuisance alarms
- **Environment**: Maintenance ongoing in adjacent area (distraction)
- **Management**: MOC process not enforced

---

### 3.3 Knowledge Base Search

**Objective**: Find similar historical incidents

**Process**:

```python
# Search for similar incidents
similar_cases = orchestrator.search_knowledge_base(
    case_id=case.id,
    filters={
        "industry": "oil_and_gas",
        "incident_type": "fire",
        "root_causes": ["valve_misposition", "cooling_failure"]
    },
    top_k=5
)
```

**Results**:

```json
{
  "similar_incidents": [
    {
      "case_id": "CSB-2019-04",
      "title": "Williams Olefins Plant Fire and Explosions",
      "date": "2013-06-13",
      "location": "Geismar, Louisiana",
      "similarity_score": 0.82,
      "common_factors": [
        "Heat exchanger cooling water failure",
        "Inadequate alarm response",
        "Management of change not followed"
      ],
      "lessons_learned": [
        "Implement lockout/tagout for critical isolation valves",
        "Alarm rationalization to reduce nuisance alarms",
        "Enhanced MOC training and compliance auditing"
      ],
      "url": "https://www.csb.gov/williams-olefins-plant-explosion-and-fire-/"
    },
    {
      "case_id": "HSE-UK-2015-02",
      "title": "Refinery Crude Unit Fire",
      "similarity_score": 0.76,
      "common_factors": [
        "Valve left in wrong position",
        "Operator error",
        "Inadequate procedures"
      ]
    }
  ]
}
```

---

### 3.4 Visual Diagram Generation

**Objective**: Create analytical diagrams for clear communication

**Diagrams Generated**:

1. **5 Why Analysis**

```python
five_why = orchestrator.generate_diagram(
    case_id=case.id,
    diagram_type="5_why",
    starting_event="Fire in vessel V-301"
)
```

Output:
```
Why did fire occur in V-301?
  └─ Because vessel overheated above auto-ignition temperature
     └─ Why did vessel overheat?
        └─ Because cooling water flow stopped
           └─ Why did cooling water stop?
              └─ Because valve HV-305 was closed
                 └─ Why was valve closed?
                    └─ Because no procedure existed for valve lineup during maintenance
                       └─ ROOT CAUSE: Management of Change process not followed
```

2. **Ishikawa (Fishbone) Diagram**

```
                Man                    Machine
                 │                        │
    No valve ────┤           Valve HV-305 ┤
    verification │           not labeled  │
                 │                        │
                 └────────┬───────────────┘
                          │
                    ┌─────▼──────┐
                    │ FIRE IN    │
                    │ VESSEL     │
                    │ V-301      │
                    └─────┬──────┘
                 ┌────────┴───────────┐
                 │                    │
    No MOC   ────┤        Nuisance ───┤
    followed     │        alarms      │
                 │        ignored     │
              Method              Measurement
```

3. **Fault Tree Analysis (FTA)**

```
                    Fire in V-301
                         │
                    ┌────┴────┐
                    │   AND   │
                    └────┬────┘
              ┌──────────┴──────────┐
              │                     │
      Flammable Vapor          Ignition Source
      Present (P=0.9)          Present (P=0.8)
              │                     │
         ┌────┴────┐           Temperature
         │   OR    │           > 450°C
         └────┬────┘                │
    ┌─────────┴─────────┐      ┌────┴────┐
    │                   │      │   AND   │
Overheat          Leak  │      └────┬────┘
(P=0.95)          (P=0.1)  ┌────────┴────────┐
    │                      │                 │
Cooling                Cooling            No Heat
Failure                Stopped            Removal
(P=1.0)                (P=1.0)            (P=1.0)
```

4. **Bowtie Diagram**

```
THREATS                    HAZARD              CONSEQUENCES
                             │
Maintenance    ──┐          │          ┌──  Fire
Work             │          │          │
                 ├──►  Loss of   ──────┤
Operator         │    Cooling    │     └──  Equipment
Error            │    Water      │         Damage
                 │          │    │
Valve            │          │    └──  Injuries
Misposition   ──┘          │
                            │
PREVENTIVE              TOP EVENT          MITIGATIVE
BARRIERS                                   BARRIERS

- MOC Process         (Failed)         - Fire Detection (OK)
- Procedures          (Missing)        - Auto Shutdown (OK)
- Training            (Inadequate)     - Fire Suppression (OK)
- Valve Labels        (Missing)        - Emergency Response (OK)
- Alarms              (Ineffective)
```

5. **Event Tree Analysis (ETA)**

Starting from initiating event: "Cooling water flow stopped"

```
                                              Success  Fail
Cooling Flow Stopped ──┐
                       │
                  Alarm Response? ───┐  (0.7)  Safe shutdown
                       │              └─ (0.3)  Temperature rises
                       │                          │
                       │                   Manual Intervention? ──┐
                       │                          │               │
                       │                     (0.5) Shutdown    (0.5) Overheat
                       │                          │                 │
                       │                          OK          Auto Shutdown? ──┐
                       │                                          │            │
                       │                                      (0.9) OK    (0.1) Fire
```

---

## Phase 4: Recommendation Development

### 4.1 Generate Corrective Actions

**Objective**: Develop CAPA (Corrective and Preventive Actions)

**Process**:

```python
# Generate recommendations
recommendations = orchestrator.generate_recommendations(
    case_id=case.id,
    prioritization_method="risk_matrix"  # criticality × feasibility
)
```

**Recommendation Categories**:

1. **Immediate Actions** (0-7 days)
   - Stop further incidents
   - Temporary safeguards

2. **Short-Term Actions** (1-3 months)
   - Fix immediate causes
   - Quick wins

3. **Long-Term Actions** (3-12 months)
   - Systemic improvements
   - Cultural change

**Example Recommendations**:

```json
{
  "recommendations": [
    {
      "id": "REC-001",
      "title": "Install lockable valve caps on critical isolation valves",
      "category": "Engineering Control",
      "priority": "High",
      "timeline": "Immediate (7 days)",
      "root_cause_addressed": "Valve HV-305 inadvertently closed",
      "hierarchy_of_controls": "Engineering",
      "responsible_party": "Maintenance Manager",
      "estimated_cost": "$5,000",
      "implementation_steps": [
        "Identify all critical isolation valves",
        "Procure lockable caps",
        "Install and test",
        "Update procedures"
      ],
      "success_criteria": "All 25 critical valves have lockable caps installed",
      "regulatory_driver": "OSHA PSM - Mechanical Integrity"
    },
    {
      "id": "REC-002",
      "title": "Conduct alarm rationalization study",
      "category": "Administrative Control",
      "priority": "High",
      "timeline": "Short-term (3 months)",
      "root_cause_addressed": "Nuisance alarms led to alarm fatigue",
      "hierarchy_of_controls": "Administrative",
      "responsible_party": "Control Systems Engineer",
      "estimated_cost": "$50,000",
      "implementation_steps": [
        "Benchmark against ISA 18.2 standard",
        "Review all alarm setpoints",
        "Eliminate/rationalize nuisance alarms",
        "Retrain operators"
      ],
      "success_criteria": "Average alarm rate < 6 per hour per operator",
      "regulatory_driver": "Industry Best Practice (ISA 18.2)"
    },
    {
      "id": "REC-003",
      "title": "Revise and enforce MOC procedure",
      "category": "Management System",
      "priority": "Critical",
      "timeline": "Short-term (1 month)",
      "root_cause_addressed": "MOC process not followed for maintenance work",
      "hierarchy_of_controls": "Administrative",
      "responsible_party": "Operations Manager",
      "estimated_cost": "$20,000",
      "implementation_steps": [
        "Review and update MOC procedure",
        "Mandatory MOC training for all supervisors",
        "Implement MOC compliance auditing",
        "Establish consequences for non-compliance"
      ],
      "success_criteria": "100% MOC compliance in quarterly audits",
      "regulatory_driver": "OSHA PSM Element 8 - MOC",
      "regulatory_citation": "29 CFR 1910.119(l)"
    }
  ]
}
```

---

### 4.2 Prioritization Matrix

**Risk Matrix** (Criticality × Feasibility):

```
         Feasibility
         Low    Medium   High
       ┌──────┬────────┬────────┐
High   │  P3  │   P1   │   P1   │  Criticality
       ├──────┼────────┼────────┤
Medium │  P3  │   P2   │   P1   │
       ├──────┼────────┼────────┤
Low    │  P4  │   P3   │   P2   │
       └──────┴────────┴────────┘

P1 = Immediate action
P2 = Short-term
P3 = Long-term
P4 = Consider/defer
```

---

## Phase 5: Report Generation

### 5.1 Compile Investigation Report

**Objective**: Create comprehensive, regulatory-compliant report

**Process**:

```python
# Generate report
report = orchestrator.generate_report(
    case_id=case.id,
    template="OSHA_PSM",  # or "Seveso_III", "NFPA_921", "API_RP_754"
    language="en",  # or "tr" for Turkish
    format="pdf"  # or "docx", "both"
)
```

**Report Structure**:

```
1. EXECUTIVE SUMMARY
   - Incident overview
   - Key findings
   - Critical recommendations

2. INCIDENT DESCRIPTION
   - Date, time, location
   - Facility and process description
   - Chemicals involved
   - Actual and potential consequences

3. INVESTIGATION TEAM AND METHODOLOGY
   - Team members and roles
   - Investigation approach
   - Standards and frameworks used

4. TIMELINE OF EVENTS
   - Chronological sequence
   - Critical decision points
   - Barrier failures marked

5. EVIDENCE SUMMARY
   - List of all evidence collected
   - Key findings from each source

6. ROOT CAUSE ANALYSIS
   6.1 Immediate Causes
   6.2 Contributing Factors
   6.3 Systemic Causes
   6.4 Causal Chain Diagram

7. VISUAL ANALYSIS
   7.1 5 Why Analysis
   7.2 Fishbone Diagram
   7.3 Fault Tree Analysis
   7.4 Bowtie Diagram

8. SIMILAR INCIDENTS AND LESSONS LEARNED
   - Comparable historical cases
   - Industry recommendations

9. CORRECTIVE AND PREVENTIVE ACTIONS
   - Prioritized CAPA list
   - Responsible parties
   - Target completion dates

10. RECOMMENDATIONS
    10.1 Immediate Actions
    10.2 Short-Term Improvements
    10.3 Long-Term Strategic Changes

11. REGULATORY COMPLIANCE ASSESSMENT
    - OSHA PSM elements affected
    - Potential violations
    - Compliance roadmap

12. APPENDICES
    A. Evidence inventory
    B. Witness statements
    C. Technical drawings
    D. Regulatory references
    E. Glossary of terms
```

**Output Files**:
- `Investigation_Report_INC-2024-012.pdf`
- `Investigation_Report_INC-2024-012.docx`
- `CAPA_Tracker_INC-2024-012.xlsx`

---

### 5.2 Quality Review

**Review Checklist**:
- [ ] All evidence properly referenced
- [ ] Root causes linked to evidence
- [ ] Recommendations address root causes
- [ ] Regulatory requirements met
- [ ] Diagrams clear and accurate
- [ ] Timeline verified
- [ ] No confidential information exposed
- [ ] Spelling and grammar checked
- [ ] Report follows template standards

**Reviewers**:
- Lead Investigator (technical accuracy)
- Legal Counsel (privilege, liability)
- HSE Manager (regulatory compliance)
- Site Manager (operational feasibility)

---

## Phase 6: Implementation and Follow-up

### 6.1 CAPA Tracking

**System Features**:
- Assign recommendations to owners
- Set due dates
- Track progress
- Send automatic reminders
- Flag overdue items

```python
# Create CAPA tracking
capa_tracker = orchestrator.create_capa_tracker(
    case_id=case.id,
    recommendations=recommendations
)

# Update progress
capa_tracker.update_status(
    recommendation_id="REC-001",
    status="in_progress",
    percent_complete=75,
    notes="Valve caps ordered, installation scheduled for next week"
)
```

---

### 6.2 Effectiveness Review

**3-6 months after incident**:
- Verify all CAPAs implemented
- Measure effectiveness (KPIs)
- Conduct follow-up audits
- Update knowledge base with learnings

**Metrics**:
- Recommendation completion rate
- Time to completion
- Recurring incident rate
- Near-miss reporting trends

---

## Workflow Summary Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ PHASE 1: INITIATION                                          │
│ - Create case                                                │
│ - Assemble team                                              │
│ - Define scope                                               │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│ PHASE 2: EVIDENCE COLLECTION                                 │
│ - Upload documents, photos, logs                             │
│ - Evidence Analysis Agent processes                          │
│ - Extract facts and timeline                                 │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│ PHASE 3: ANALYSIS                                            │
│ - Root Cause Analysis Agent (CCPS, TapRoot)                  │
│ - Knowledge Base Agent (similar cases)                       │
│ - Diagram Generator (5Why, Fishbone, FTA, Bowtie)           │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│ PHASE 4: RECOMMENDATIONS                                     │
│ - Generate CAPA                                              │
│ - Prioritize by risk                                         │
│ - Assign owners                                              │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│ PHASE 5: REPORT GENERATION                                   │
│ - Compile findings                                           │
│ - Apply regulatory template                                  │
│ - Generate Word/PDF                                          │
│ - Quality review                                             │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│ PHASE 6: IMPLEMENTATION                                      │
│ - Track CAPA completion                                      │
│ - Verify effectiveness                                       │
│ - Update knowledge base                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## API Usage Examples

### Complete Investigation Workflow

```python
from incident_investigation.orchestrator import IncidentOrchestrator

# Initialize orchestrator
orchestrator = IncidentOrchestrator()

# 1. Create investigation
case = orchestrator.create_investigation({
    "incident_id": "INC-2024-012",
    "industry": "oil_and_gas",
    "incident_type": "fire",
    "severity": "major"
})

# 2. Upload evidence
case.add_evidence("witness_statement", "./evidence/operator_001.pdf")
case.add_evidence("pid_drawing", "./evidence/unit3_pid.pdf")
case.add_evidence("scada_log", "./evidence/alarm_history.csv")
case.add_evidence("photo", "./evidence/damage_001.jpg")

# 3. Run investigation
results = orchestrator.investigate(case.id)

# Access results
print(results["timeline"])
print(results["root_causes"])
print(results["similar_cases"])

# 4. Generate diagrams
orchestrator.generate_diagram(case.id, "fishbone")
orchestrator.generate_diagram(case.id, "bowtie")
orchestrator.generate_diagram(case.id, "fault_tree")

# 5. Generate recommendations
recommendations = orchestrator.generate_recommendations(case.id)

# 6. Create report
report_pdf = orchestrator.generate_report(
    case_id=case.id,
    template="OSHA_PSM",
    format="pdf"
)

# 7. Set up CAPA tracking
capa = orchestrator.create_capa_tracker(case.id, recommendations)

print(f"Investigation complete. Report saved to: {report_pdf}")
```

---

## Conclusion

This workflow provides a systematic, repeatable, and compliant approach to incident investigation. The AI-powered system accelerates analysis while ensuring thoroughness and consistency with industry standards.

Key benefits:
- **Speed**: Automated evidence processing and analysis
- **Consistency**: Standardized frameworks applied every time
- **Completeness**: No missed causes due to comprehensive taxonomy
- **Compliance**: Regulatory requirements embedded in templates
- **Learning**: Knowledge base grows with each investigation
- **Collaboration**: Multi-user platform with role-based access

The system augments—not replaces—human expertise, providing investigators with powerful tools to identify root causes and prevent future incidents.
