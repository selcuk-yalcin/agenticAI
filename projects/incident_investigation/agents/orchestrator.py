"""
Orchestrator Agent for AI-Powered Incident Investigation System.

This is the master coordinator that manages the entire investigation workflow,
coordinating all specialized agents to conduct comprehensive incident investigations.

Author: AI Development Team
Version: 1.0.0
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent))
try:
    from config import config
except ImportError:
    config = None


class IncidentSeverity(Enum):
    """Incident severity classification."""
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    CATASTROPHIC = "catastrophic"


class InvestigationStatus(Enum):
    """Investigation case status."""
    INITIATED = "initiated"
    EVIDENCE_COLLECTION = "evidence_collection"
    ANALYSIS = "analysis"
    REPORT_GENERATION = "report_generation"
    COMPLETED = "completed"
    CLOSED = "closed"


@dataclass
class InvestigationCase:
    """Investigation case data model."""
    id: str
    incident_id: str
    date_occurred: str
    location: str
    industry: str
    facility_type: str
    incident_type: str
    severity: str
    actual_consequences: Dict[str, Any]
    regulatory_notification_required: bool
    standards_applicable: List[str]
    status: str
    created_at: str
    evidence_items: List[Dict] = None
    timeline: List[Dict] = None
    root_causes: Dict = None
    recommendations: List[Dict] = None
    
    def __post_init__(self):
        if self.evidence_items is None:
            self.evidence_items = []
        if self.timeline is None:
            self.timeline = []


class IncidentOrchestrator:
    """
    Master orchestrator for incident investigations.
    
    Coordinates all specialized agents:
    - Evidence Analysis Agent
    - Root Cause Analysis Agent
    - Knowledge Base Agent
    - Diagram Generator Agent
    - Report Generation Agent
    - Recommendation Agent
    
    Example:
        >>> orchestrator = IncidentOrchestrator()
        >>> case = orchestrator.create_investigation({
        ...     "incident_id": "INC-2024-001",
        ...     "industry": "oil_and_gas",
        ...     "incident_type": "fire"
        ... })
        >>> orchestrator.investigate(case.id)
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the orchestrator.
        
        Args:
            config_path: Path to configuration file (deprecated, use .env instead)
        """
        self.cases: Dict[str, InvestigationCase] = {}
        
        # Load configuration from .env or use provided config file (legacy)
        if config:
            # Validate configuration and get API key from config
            config.validate()
            self.api_key = config.OPENAI_API_KEY
            self.openai_config = config.get_openai_client_config()
            self.config = {
                'company_name': config.COMPANY_NAME,
                'organization_id': config.ORGANIZATION_ID,
                'environment': config.ENVIRONMENT
            }
        else:
            # Fallback to legacy config file or environment variables
            self.config = self._load_config(config_path) if config_path else {}
            self.api_key = os.getenv("OPENAI_API_KEY", "")
            self.openai_config = {
                'api_key': self.api_key,
                'model': os.getenv('OPENAI_MODEL', 'gpt-4o'),
                'temperature': float(os.getenv('OPENAI_TEMPERATURE', '0.2'))
            }
        
        # Initialize agents (will be imported from respective modules)
        self.evidence_agent = None  # EvidenceAnalysisAgent()
        self.root_cause_agent = None  # RootCauseAnalysisAgent()
        self.knowledge_base_agent = None  # KnowledgeBaseAgent()
        self.diagram_agent = None  # DiagramGeneratorAgent()
        self.report_agent = None  # ReportGenerationAgent()
        self.recommendation_agent = None  # RecommendationAgent()
        
        print("IncidentOrchestrator initialized")
        if config:
            print(f"  - Environment: {config.ENVIRONMENT}")
            print(f"  - Company: {config.COMPANY_NAME}")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from file (legacy method)."""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return {}
    
    def create_investigation(self, incident_details: Dict[str, Any]) -> InvestigationCase:
        """
        Create a new investigation case.
        
        Args:
            incident_details: Dictionary containing incident information
                Required fields:
                - incident_id: Unique incident identifier
                - industry: Industry sector
                - incident_type: Type of incident (fire, explosion, leak, etc.)
                
                Optional fields:
                - date_occurred: ISO format datetime
                - location: Facility location
                - facility_type: refinery, chemical_plant, offshore, etc.
                - severity: minor, moderate, major, catastrophic
                - actual_consequences: Dictionary of impacts
                - regulatory_notification_required: Boolean
                - standards_applicable: List of regulatory standards
        
        Returns:
            InvestigationCase: Created case object
            
        Example:
            >>> case = orchestrator.create_investigation({
            ...     "incident_id": "INC-2024-012",
            ...     "industry": "petrochemical",
            ...     "incident_type": "fire",
            ...     "severity": "major"
            ... })
        """
        # Generate unique case ID
        case_id = f"CASE-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        # Set defaults
        incident_details.setdefault("date_occurred", datetime.now().isoformat())
        incident_details.setdefault("location", "Unknown")
        incident_details.setdefault("facility_type", "industrial")
        incident_details.setdefault("severity", "moderate")
        incident_details.setdefault("actual_consequences", {})
        incident_details.setdefault("regulatory_notification_required", False)
        incident_details.setdefault("standards_applicable", [])
        
        # Create case
        case = InvestigationCase(
            id=case_id,
            incident_id=incident_details["incident_id"],
            date_occurred=incident_details["date_occurred"],
            location=incident_details["location"],
            industry=incident_details["industry"],
            facility_type=incident_details["facility_type"],
            incident_type=incident_details["incident_type"],
            severity=incident_details["severity"],
            actual_consequences=incident_details["actual_consequences"],
            regulatory_notification_required=incident_details["regulatory_notification_required"],
            standards_applicable=incident_details["standards_applicable"],
            status=InvestigationStatus.INITIATED.value,
            created_at=datetime.now().isoformat()
        )
        
        # Store case
        self.cases[case_id] = case
        
        print(f"✓ Investigation case created: {case_id}")
        print(f"  Incident ID: {case.incident_id}")
        print(f"  Industry: {case.industry}")
        print(f"  Type: {case.incident_type}")
        print(f"  Severity: {case.severity}")
        
        return case
    
    def add_evidence(
        self,
        case_id: str,
        evidence_type: str,
        file_path: str,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Add evidence to an investigation case.
        
        Args:
            case_id: Case identifier
            evidence_type: Type of evidence
                - witness_statement
                - pid_drawing
                - hazop_report
                - photo
                - scada_log
                - maintenance_record
                - procedure
                - video
            file_path: Path to evidence file
            metadata: Additional metadata about the evidence
        
        Returns:
            Evidence record with ID and processing status
            
        Example:
            >>> case.add_evidence(
            ...     case_id="CASE-001",
            ...     evidence_type="witness_statement",
            ...     file_path="./evidence/operator_001.pdf",
            ...     metadata={"witness_name": "John Smith"}
            ... )
        """
        if case_id not in self.cases:
            raise ValueError(f"Case {case_id} not found")
        
        case = self.cases[case_id]
        
        # Generate evidence ID
        evidence_id = f"EVD-{len(case.evidence_items) + 1:03d}"
        
        evidence_record = {
            "evidence_id": evidence_id,
            "type": evidence_type,
            "file_path": file_path,
            "metadata": metadata or {},
            "uploaded_at": datetime.now().isoformat(),
            "status": "pending_processing"
        }
        
        case.evidence_items.append(evidence_record)
        case.status = InvestigationStatus.EVIDENCE_COLLECTION.value
        
        print(f"✓ Evidence added: {evidence_id} ({evidence_type})")
        
        # Trigger evidence processing (async in production)
        if self.evidence_agent:
            processed = self.evidence_agent.process_evidence(evidence_record)
            evidence_record["status"] = "processed"
            evidence_record["analysis"] = processed
        
        return evidence_record
    
    def investigate(self, case_id: str) -> Dict[str, Any]:
        """
        Run the complete investigation workflow.
        
        This orchestrates all agents in the correct sequence:
        1. Process all evidence
        2. Build timeline
        3. Perform root cause analysis
        4. Search knowledge base for similar incidents
        5. Generate visual diagrams
        6. Develop recommendations
        
        Args:
            case_id: Case identifier
        
        Returns:
            Investigation results containing:
            - timeline: Chronological event sequence
            - root_causes: Immediate, contributing, and systemic causes
            - similar_cases: Historical incident comparisons
            - diagrams: Generated analytical diagrams
            - recommendations: CAPA list
            
        Example:
            >>> results = orchestrator.investigate("CASE-001")
            >>> print(results["root_causes"]["immediate_causes"])
        """
        if case_id not in self.cases:
            raise ValueError(f"Case {case_id} not found")
        
        case = self.cases[case_id]
        case.status = InvestigationStatus.ANALYSIS.value
        
        print(f"\n{'='*60}")
        print(f"INVESTIGATION WORKFLOW: {case_id}")
        print(f"{'='*60}\n")
        
        results = {}
        
        # Step 1: Process evidence and build timeline
        print("Step 1: Processing evidence and building timeline...")
        timeline = self._build_timeline(case)
        case.timeline = timeline
        results["timeline"] = timeline
        print(f"✓ Timeline created with {len(timeline)} events\n")
        
        # Step 2: Root cause analysis
        print("Step 2: Performing root cause analysis...")
        root_causes = self._perform_root_cause_analysis(case)
        case.root_causes = root_causes
        results["root_causes"] = root_causes
        print(f"✓ Identified {len(root_causes.get('immediate_causes', []))} immediate causes")
        print(f"✓ Identified {len(root_causes.get('systemic_causes', []))} systemic causes\n")
        
        # Step 3: Search knowledge base
        print("Step 3: Searching knowledge base for similar incidents...")
        similar_cases = self._search_knowledge_base(case)
        results["similar_cases"] = similar_cases
        print(f"✓ Found {len(similar_cases)} similar incidents\n")
        
        # Step 4: Generate diagrams
        print("Step 4: Generating visual analysis diagrams...")
        diagrams = self._generate_diagrams(case)
        results["diagrams"] = diagrams
        print(f"✓ Generated {len(diagrams)} diagrams\n")
        
        # Step 5: Develop recommendations
        print("Step 5: Developing corrective and preventive actions...")
        recommendations = self._generate_recommendations(case)
        case.recommendations = recommendations
        results["recommendations"] = recommendations
        print(f"✓ Generated {len(recommendations)} recommendations\n")
        
        case.status = InvestigationStatus.COMPLETED.value
        
        print(f"{'='*60}")
        print("INVESTIGATION COMPLETE")
        print(f"{'='*60}\n")
        
        return results
    
    def _build_timeline(self, case: InvestigationCase) -> List[Dict]:
        """Build chronological timeline from evidence."""
        # Placeholder - in production, this calls EvidenceAnalysisAgent
        timeline = [
            {
                "time": case.date_occurred,
                "event": f"{case.incident_type.capitalize()} incident occurred",
                "source": "Incident report",
                "type": "incident"
            }
        ]
        return timeline
    
    def _perform_root_cause_analysis(self, case: InvestigationCase) -> Dict:
        """Perform root cause analysis using multiple frameworks."""
        # Placeholder - in production, this calls RootCauseAnalysisAgent
        root_causes = {
            "immediate_causes": [
                {
                    "cause": f"{case.incident_type.capitalize()} initiated",
                    "category": "Equipment/Technical",
                    "confidence": 0.85
                }
            ],
            "contributing_factors": [],
            "systemic_causes": []
        }
        return root_causes
    
    def _search_knowledge_base(self, case: InvestigationCase) -> List[Dict]:
        """Search for similar historical incidents."""
        # Placeholder - in production, this calls KnowledgeBaseAgent
        similar_cases = []
        return similar_cases
    
    def _generate_diagrams(self, case: InvestigationCase) -> List[str]:
        """Generate analytical diagrams."""
        # Placeholder - in production, this calls DiagramGeneratorAgent
        diagrams = ["fishbone", "5_why", "fault_tree", "bowtie"]
        return diagrams
    
    def _generate_recommendations(self, case: InvestigationCase) -> List[Dict]:
        """Generate CAPA recommendations."""
        # Placeholder - in production, this calls RecommendationAgent
        recommendations = [
            {
                "id": "REC-001",
                "title": "Implement corrective action for immediate cause",
                "priority": "high",
                "timeline": "immediate"
            }
        ]
        return recommendations
    
    def generate_report(
        self,
        case_id: str,
        template: str = "OSHA_PSM",
        language: str = "en",
        format: str = "pdf"
    ) -> str:
        """
        Generate investigation report.
        
        Args:
            case_id: Case identifier
            template: Report template
                - OSHA_PSM: OSHA Process Safety Management
                - Seveso_III: EU Major Accident Directive
                - NFPA_921: Fire and Explosion Investigation
                - API_RP_754: Process Safety Performance Indicators
                - ISO_45001: Occupational Health and Safety
            language: Report language (en, tr, es, fr, de)
            format: Output format (pdf, docx, both)
        
        Returns:
            Path to generated report file
            
        Example:
            >>> report_path = orchestrator.generate_report(
            ...     case_id="CASE-001",
            ...     template="OSHA_PSM",
            ...     format="pdf"
            ... )
        """
        if case_id not in self.cases:
            raise ValueError(f"Case {case_id} not found")
        
        case = self.cases[case_id]
        case.status = InvestigationStatus.REPORT_GENERATION.value
        
        print(f"\n{'='*60}")
        print(f"GENERATING REPORT: {template}")
        print(f"{'='*60}\n")
        
        # Placeholder - in production, this calls ReportGenerationAgent
        report_filename = f"Investigation_Report_{case.incident_id}_{template}.{format}"
        report_path = f"./reports/{report_filename}"
        
        print(f"✓ Report generated: {report_path}")
        print(f"  Template: {template}")
        print(f"  Language: {language}")
        print(f"  Format: {format}\n")
        
        return report_path
    
    def generate_diagram(
        self,
        case_id: str,
        diagram_type: str,
        output_format: str = "png"
    ) -> str:
        """
        Generate a specific analytical diagram.
        
        Args:
            case_id: Case identifier
            diagram_type: Type of diagram
                - 5_why: 5 Why analysis
                - fishbone: Ishikawa/Fishbone diagram
                - fault_tree: Fault Tree Analysis (FTA)
                - event_tree: Event Tree Analysis (ETA)
                - bowtie: Bowtie diagram
            output_format: Image format (png, svg, pdf)
        
        Returns:
            Path to generated diagram file
            
        Example:
            >>> diagram = orchestrator.generate_diagram(
            ...     case_id="CASE-001",
            ...     diagram_type="bowtie"
            ... )
        """
        if case_id not in self.cases:
            raise ValueError(f"Case {case_id} not found")
        
        case = self.cases[case_id]
        
        # Placeholder - in production, this calls DiagramGeneratorAgent
        diagram_filename = f"{case.incident_id}_{diagram_type}.{output_format}"
        diagram_path = f"./diagrams/{diagram_filename}"
        
        print(f"✓ Diagram generated: {diagram_path}")
        print(f"  Type: {diagram_type}")
        print(f"  Format: {output_format}")
        
        return diagram_path
    
    def search_knowledge_base(
        self,
        case_id: str,
        filters: Optional[Dict] = None,
        top_k: int = 5
    ) -> List[Dict]:
        """
        Search knowledge base for similar incidents.
        
        Args:
            case_id: Case identifier
            filters: Optional filters
                - industry: Industry sector
                - incident_type: Type of incident
                - root_causes: List of root cause categories
                - date_range: Tuple of (start_date, end_date)
            top_k: Number of similar cases to return
        
        Returns:
            List of similar incidents with similarity scores
            
        Example:
            >>> similar = orchestrator.search_knowledge_base(
            ...     case_id="CASE-001",
            ...     filters={"industry": "oil_and_gas"},
            ...     top_k=5
            ... )
        """
        if case_id not in self.cases:
            raise ValueError(f"Case {case_id} not found")
        
        # Placeholder - in production, this calls KnowledgeBaseAgent
        similar_cases = [
            {
                "case_id": "CSB-2019-04",
                "title": "Sample historical incident",
                "similarity_score": 0.82,
                "common_factors": ["equipment_failure", "inadequate_procedure"]
            }
        ]
        
        return similar_cases[:top_k]
    
    def create_capa_tracker(
        self,
        case_id: str,
        recommendations: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Create CAPA (Corrective and Preventive Action) tracker.
        
        Args:
            case_id: Case identifier
            recommendations: List of recommendations (uses case recommendations if None)
        
        Returns:
            CAPA tracker configuration
            
        Example:
            >>> capa = orchestrator.create_capa_tracker("CASE-001")
            >>> capa.update_status("REC-001", status="completed")
        """
        if case_id not in self.cases:
            raise ValueError(f"Case {case_id} not found")
        
        case = self.cases[case_id]
        
        if recommendations is None:
            recommendations = case.recommendations or []
        
        capa_tracker = {
            "case_id": case_id,
            "created_at": datetime.now().isoformat(),
            "total_actions": len(recommendations),
            "actions": recommendations,
            "completion_rate": 0.0
        }
        
        print(f"✓ CAPA tracker created for {case_id}")
        print(f"  Total actions: {len(recommendations)}")
        
        return capa_tracker
    
    def get_investigation_status(self, case_id: str) -> Dict:
        """
        Get current status of an investigation.
        
        Args:
            case_id: Case identifier
        
        Returns:
            Status dictionary with progress information
        """
        if case_id not in self.cases:
            raise ValueError(f"Case {case_id} not found")
        
        case = self.cases[case_id]
        
        status = {
            "case_id": case_id,
            "incident_id": case.incident_id,
            "status": case.status,
            "evidence_count": len(case.evidence_items),
            "timeline_events": len(case.timeline) if case.timeline else 0,
            "root_causes_identified": bool(case.root_causes),
            "recommendations_count": len(case.recommendations) if case.recommendations else 0,
            "created_at": case.created_at
        }
        
        return status
    
    def export_case(self, case_id: str, output_path: str) -> str:
        """
        Export complete case data to JSON.
        
        Args:
            case_id: Case identifier
            output_path: Path to save JSON file
        
        Returns:
            Path to exported file
        """
        if case_id not in self.cases:
            raise ValueError(f"Case {case_id} not found")
        
        case = self.cases[case_id]
        case_dict = asdict(case)
        
        with open(output_path, 'w') as f:
            json.dump(case_dict, f, indent=2)
        
        print(f"✓ Case exported to: {output_path}")
        
        return output_path


if __name__ == "__main__":
    # Example usage
    print("AI-Powered Incident Investigation System")
    print("=========================================\n")
    
    # Initialize orchestrator
    orchestrator = IncidentOrchestrator()
    
    # Create investigation case
    case = orchestrator.create_investigation({
        "incident_id": "INC-2024-012",
        "industry": "oil_and_gas",
        "facility_type": "refinery",
        "incident_type": "fire",
        "severity": "major",
        "location": "Refinery Unit 3 - Crude Distillation",
        "actual_consequences": {
            "injuries": 2,
            "fatalities": 0,
            "property_damage_usd": 500000,
            "environmental_release": True
        },
        "regulatory_notification_required": True,
        "standards_applicable": ["OSHA_PSM", "API_RP_754", "NFPA_921"]
    })
    
    # Add evidence
    print("\nAdding evidence...")
    orchestrator.add_evidence(
        case_id=case.id,
        evidence_type="witness_statement",
        file_path="./evidence/operator_001.pdf",
        metadata={"witness_name": "John Smith", "role": "Control Room Operator"}
    )
    
    orchestrator.add_evidence(
        case_id=case.id,
        evidence_type="pid_drawing",
        file_path="./evidence/unit3_pid.pdf",
        metadata={"drawing_number": "P-1234-05"}
    )
    
    # Run investigation
    print("\nRunning investigation workflow...")
    results = orchestrator.investigate(case.id)
    
    # Generate report
    report = orchestrator.generate_report(
        case_id=case.id,
        template="OSHA_PSM",
        format="pdf"
    )
    
    # Generate diagrams
    print("\nGenerating additional diagrams...")
    orchestrator.generate_diagram(case.id, "bowtie")
    orchestrator.generate_diagram(case.id, "fault_tree")
    
    # Create CAPA tracker
    print("\nCreating CAPA tracker...")
    capa = orchestrator.create_capa_tracker(case.id)
    
    # Get status
    print("\nInvestigation Status:")
    status = orchestrator.get_investigation_status(case.id)
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    print("\n✓ Investigation workflow complete!")
