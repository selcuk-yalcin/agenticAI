"""
Complete Example: AI-Powered Incident Investigation

This script demonstrates the full investigation workflow for a sample incident:
- Refinery fire in crude distillation unit
- Cooling water system failure
- Multiple evidence types
- Complete analysis through to report generation

Author: AI Development Team
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import configuration and agents
try:
    from config import config
    config_available = True
except ImportError:
    config_available = False

from agents.orchestrator import IncidentOrchestrator


def main():
    """Run complete investigation workflow example."""
    
    print("="*80)
    print(" AI-POWERED INCIDENT INVESTIGATION SYSTEM")
    print(" Example: Refinery Fire - Cooling System Failure")
    print("="*80)
    print()
    
    # Validate configuration
    if config_available:
        try:
            config.validate()
            print(f"✓ Configuration loaded successfully")
            print(f"  - Environment: {config.ENVIRONMENT}")
            print(f"  - OpenAI Model: {config.OPENAI_MODEL}")
            print(f"  - Company: {config.COMPANY_NAME}")
            print()
        except ValueError as e:
            print(f"✗ Configuration Error: {e}")
            print("\nPlease copy .env.example to .env and set your OPENAI_API_KEY")
            return
    else:
        print("⚠ Configuration module not found. Using environment variables.")
        if not os.getenv("OPENAI_API_KEY"):
            print("✗ OPENAI_API_KEY not set in environment")
            print("Please set OPENAI_API_KEY or create a .env file")
            return
        print()
    
    # ========================================================================
    # PHASE 1: INVESTIGATION INITIATION
    # ========================================================================
    
    print("\n" + "="*80)
    print("PHASE 1: INVESTIGATION INITIATION")
    print("="*80 + "\n")
    
    # Initialize orchestrator
    orchestrator = IncidentOrchestrator()
    
    # Create investigation case
    case = orchestrator.create_investigation({
        "incident_id": "INC-2024-REF-012",
        "date_occurred": "2024-12-15T14:30:00Z",
        "location": "Acme Refinery - Unit 3, Crude Distillation Tower",
        "industry": "oil_and_gas",
        "facility_type": "refinery",
        "incident_type": "fire",
        "severity": "major",
        "actual_consequences": {
            "injuries": 2,
            "fatalities": 0,
            "property_damage_usd": 500000,
            "environmental_release": True,
            "production_loss_days": 7
        },
        "regulatory_notification_required": True,
        "standards_applicable": [
            "OSHA_PSM",      # 29 CFR 1910.119
            "API_RP_754",    # Process Safety Performance Indicators
            "NFPA_921",      # Fire Investigation Guide
            "ISO_45001"      # Occupational Health and Safety
        ]
    })
    
    print(f"\n✓ Investigation case created successfully")
    print(f"  Case ID: {case.id}")
    print(f"  Incident ID: {case.incident_id}")
    
    # ========================================================================
    # PHASE 2: EVIDENCE COLLECTION
    # ========================================================================
    
    print("\n" + "="*80)
    print("PHASE 2: EVIDENCE COLLECTION")
    print("="*80 + "\n")
    
    print("Uploading evidence items...\n")
    
    # Evidence 1: Witness Statement - Control Room Operator
    print("1. Witness Statement - Control Room Operator")
    orchestrator.add_evidence(
        case_id=case.id,
        evidence_type="witness_statement",
        file_path="./evidence/witness_operator_smith.pdf",
        metadata={
            "witness_name": "John Smith",
            "role": "Control Room Operator",
            "shift": "Day shift",
            "interview_date": "2024-12-16",
            "interviewer": "Lead Investigator - Jane Doe"
        }
    )
    
    # Evidence 2: Witness Statement - Field Operator
    print("2. Witness Statement - Field Operator")
    orchestrator.add_evidence(
        case_id=case.id,
        evidence_type="witness_statement",
        file_path="./evidence/witness_operator_jones.pdf",
        metadata={
            "witness_name": "Mike Jones",
            "role": "Field Operator",
            "shift": "Day shift",
            "interview_date": "2024-12-16"
        }
    )
    
    # Evidence 3: P&ID Drawing
    print("3. P&ID Drawing - Unit 3 Cooling System")
    orchestrator.add_evidence(
        case_id=case.id,
        evidence_type="pid_drawing",
        file_path="./evidence/unit3_cooling_pid_sheet12.pdf",
        metadata={
            "drawing_number": "P-1234-12",
            "revision": "D",
            "date": "2023-03-15",
            "system": "Overhead cooling water system",
            "equipment_covered": ["V-301", "E-301", "P-301", "HV-305"]
        }
    )
    
    # Evidence 4: HAZOP Report
    print("4. HAZOP Study Report - Unit 3")
    orchestrator.add_evidence(
        case_id=case.id,
        evidence_type="hazop_report",
        file_path="./evidence/hazop_unit3_2022.pdf",
        metadata={
            "study_date": "2022-06-15",
            "scope": "Unit 3 Full Revalidation",
            "team_leader": "Dr. Sarah Williams",
            "open_recommendations": 12
        }
    )
    
    # Evidence 5: Incident Photos
    print("5. Incident Scene Photographs (3 images)")
    for i, description in enumerate([
        "Fire damage to vessel V-301",
        "Closed valve HV-305 position",
        "Overall unit damage assessment"
    ], 1):
        orchestrator.add_evidence(
            case_id=case.id,
            evidence_type="photo",
            file_path=f"./evidence/photos/incident_photo_{i:03d}.jpg",
            metadata={
                "description": description,
                "date_taken": "2024-12-15",
                "photographer": "Safety Inspector - Bob Wilson",
                "location": "Unit 3"
            }
        )
    
    # Evidence 6: SCADA Alarm History
    print("6. SCADA System - Alarm History")
    orchestrator.add_evidence(
        case_id=case.id,
        evidence_type="scada_log",
        file_path="./evidence/scada_alarm_history_20241215.csv",
        metadata={
            "time_range": "2024-12-15 14:00:00 to 15:00:00",
            "system": "Honeywell DCS",
            "tags_included": ["TI-301", "PI-302", "FI-303", "HV-305"],
            "alarm_count": 47,
            "export_format": "CSV"
        }
    )
    
    # Evidence 7: Maintenance Records
    print("7. Maintenance Work Orders - Pump P-302")
    orchestrator.add_evidence(
        case_id=case.id,
        evidence_type="maintenance_record",
        file_path="./evidence/maintenance_wo_p302_2024.pdf",
        metadata={
            "equipment": "Cooling Water Pump P-302",
            "work_order_number": "WO-24-5678",
            "date_started": "2024-12-15 12:00:00",
            "status": "In Progress",
            "technician": "Tom Anderson"
        }
    )
    
    # Evidence 8: Operating Procedure
    print("8. Operating Procedure - Cooling System")
    orchestrator.add_evidence(
        case_id=case.id,
        evidence_type="procedure",
        file_path="./evidence/sop_cooling_system_unit3.pdf",
        metadata={
            "procedure_number": "SOP-U3-CW-001",
            "revision": "5",
            "last_updated": "2023-11-20",
            "title": "Cooling Water System Operation and Maintenance"
        }
    )
    
    # Evidence 9: Training Records
    print("9. Operator Training Records")
    orchestrator.add_evidence(
        case_id=case.id,
        evidence_type="maintenance_record",
        file_path="./evidence/training_records_operators.xlsx",
        metadata={
            "type": "Training Matrix",
            "date_range": "2023-2024",
            "operators_included": ["John Smith", "Mike Jones", "Others"],
            "course": "Unit 3 Operations and Safety"
        }
    )
    
    # Evidence 10: Previous Audit Findings
    print("10. Previous PSM Audit Report")
    orchestrator.add_evidence(
        case_id=case.id,
        evidence_type="audit_report",
        file_path="./evidence/psm_audit_2023.pdf",
        metadata={
            "audit_date": "2023-09-12",
            "auditor": "Third-Party Consultant",
            "findings_count": 8,
            "corrective_actions_status": "Partially Implemented"
        }
    )
    
    print(f"\n✓ Total evidence items uploaded: 10+")
    
    # ========================================================================
    # PHASE 3: INVESTIGATION ANALYSIS
    # ========================================================================
    
    print("\n" + "="*80)
    print("PHASE 3: INVESTIGATION ANALYSIS")
    print("="*80 + "\n")
    
    # Run complete investigation
    results = orchestrator.investigate(case.id)
    
    # Display timeline
    print("\n" + "-"*80)
    print("TIMELINE OF EVENTS")
    print("-"*80)
    for event in results.get("timeline", []):
        print(f"  {event.get('time', 'Unknown')}: {event.get('event', 'Event')}")
    
    # Display root causes
    print("\n" + "-"*80)
    print("ROOT CAUSE ANALYSIS SUMMARY")
    print("-"*80)
    
    root_causes = results.get("root_causes", {})
    
    print("\nImmediate Causes:")
    for i, cause in enumerate(root_causes.get("immediate_causes", []), 1):
        print(f"  {i}. {cause.get('cause', 'Unknown')}")
        print(f"     Category: {cause.get('category', 'Unknown')}")
        print(f"     Confidence: {cause.get('confidence', 0)*100:.0f}%")
    
    print("\nSystemic Causes:")
    for i, cause in enumerate(root_causes.get("systemic_causes", []), 1):
        print(f"  {i}. {cause.get('cause', 'Unknown')}")
        print(f"     Category: {cause.get('category', 'Unknown')}")
        print(f"     Severity: {cause.get('severity', 'unknown').upper()}")
        if "standard_violated" in cause:
            print(f"     Standard Violated: {cause.get('standard_violated')}")
    
    # Display similar incidents
    print("\n" + "-"*80)
    print("SIMILAR HISTORICAL INCIDENTS")
    print("-"*80)
    
    similar = results.get("similar_cases", [])
    if similar:
        for i, incident in enumerate(similar[:3], 1):
            print(f"\n  {i}. {incident.get('title', 'Unknown Incident')}")
            print(f"     Case ID: {incident.get('case_id', 'Unknown')}")
            print(f"     Similarity: {incident.get('similarity_score', 0)*100:.0f}%")
    else:
        print("  No similar incidents found in knowledge base")
    
    # Display recommendations
    print("\n" + "-"*80)
    print("CORRECTIVE AND PREVENTIVE ACTIONS (CAPA)")
    print("-"*80)
    
    recommendations = results.get("recommendations", [])
    for i, rec in enumerate(recommendations, 1):
        print(f"\n  {i}. {rec.get('title', 'Unknown')}")
        print(f"     Priority: {rec.get('priority', 'unknown').upper()}")
        print(f"     Timeline: {rec.get('timeline', 'unknown').title()}")
    
    # ========================================================================
    # PHASE 4: DIAGRAM GENERATION
    # ========================================================================
    
    print("\n" + "="*80)
    print("PHASE 4: VISUAL ANALYSIS DIAGRAMS")
    print("="*80 + "\n")
    
    # Generate diagrams
    diagrams = [
        ("5_why", "5 Why Analysis"),
        ("fishbone", "Ishikawa (Fishbone) Diagram"),
        ("fault_tree", "Fault Tree Analysis (FTA)"),
        ("event_tree", "Event Tree Analysis (ETA)"),
        ("bowtie", "Bowtie Diagram")
    ]
    
    for diagram_type, diagram_name in diagrams:
        path = orchestrator.generate_diagram(
            case_id=case.id,
            diagram_type=diagram_type,
            output_format="png"
        )
        print(f"  ✓ {diagram_name}")
    
    # ========================================================================
    # PHASE 5: REPORT GENERATION
    # ========================================================================
    
    print("\n" + "="*80)
    print("PHASE 5: INVESTIGATION REPORT GENERATION")
    print("="*80 + "\n")
    
    # Generate OSHA PSM-compliant report
    print("Generating investigation reports...\n")
    
    report_pdf = orchestrator.generate_report(
        case_id=case.id,
        template="OSHA_PSM",
        language="en",
        format="pdf"
    )
    
    report_docx = orchestrator.generate_report(
        case_id=case.id,
        template="OSHA_PSM",
        language="en",
        format="docx"
    )
    
    # Generate API RP 754 metrics report
    metrics_report = orchestrator.generate_report(
        case_id=case.id,
        template="API_RP_754",
        format="pdf"
    )
    
    print(f"\n✓ All reports generated successfully")
    
    # ========================================================================
    # PHASE 6: CAPA TRACKING
    # ========================================================================
    
    print("\n" + "="*80)
    print("PHASE 6: CAPA TRACKING SETUP")
    print("="*80 + "\n")
    
    # Create CAPA tracker
    capa_tracker = orchestrator.create_capa_tracker(case.id)
    
    print(f"CAPA Tracker Summary:")
    print(f"  Total Actions: {capa_tracker['total_actions']}")
    print(f"  Completion Rate: {capa_tracker['completion_rate']}%")
    print(f"  Created: {capa_tracker['created_at']}")
    
    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    
    print("\n" + "="*80)
    print("INVESTIGATION COMPLETE - SUMMARY")
    print("="*80 + "\n")
    
    status = orchestrator.get_investigation_status(case.id)
    
    print("Investigation Status:")
    for key, value in status.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print("\nDeliverables Generated:")
    print(f"  ✓ Investigation Report (OSHA PSM) - PDF and Word")
    print(f"  ✓ Process Safety Metrics Report (API RP 754)")
    print(f"  ✓ 5 Visual Analysis Diagrams")
    print(f"  ✓ CAPA Tracking System")
    
    print("\nRegulatory Compliance:")
    for standard in case.standards_applicable:
        print(f"  ✓ {standard}")
    
    print("\n" + "="*80)
    print("INVESTIGATION WORKFLOW DEMONSTRATION COMPLETE")
    print("="*80 + "\n")
    
    print("Next Steps:")
    print("  1. Review investigation report with team")
    print("  2. Submit to regulatory authorities if required")
    print("  3. Implement CAPA recommendations")
    print("  4. Track completion of corrective actions")
    print("  5. Conduct effectiveness review after 6 months")
    print("  6. Update knowledge base with lessons learned")
    
    print("\n" + "="*80 + "\n")
    
    return case, results


if __name__ == "__main__":
    # Run complete investigation example
    case, results = main()
    
    print("\n✓ Example investigation completed successfully!")
    print(f"\nCase ID: {case.id}")
    print(f"Status: {case.status}")
    print(f"\nAll investigation artifacts saved to:")
    print(f"  - Reports: ./reports/")
    print(f"  - Diagrams: ./diagrams/")
    print(f"  - Evidence: ./evidence/")
    print()
