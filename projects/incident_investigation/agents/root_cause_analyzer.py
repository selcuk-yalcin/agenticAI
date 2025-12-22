"""
Root Cause Analysis Agent for Incident Investigation System.

This agent applies multiple root cause frameworks to identify:
- Immediate causes (direct triggers)
- Contributing factors (enabling conditions)
- Systemic causes (organizational failures)
- Latent conditions (long-standing weaknesses)

Frameworks integrated:
- CCPS Guidelines (AIChE)
- TapRoot® Root Cause Map
- DNV ICAM
- 5M+E (Man, Machine, Material, Method, Measurement, Environment, Management)
- Swiss Cheese Model

Author: AI Development Team
Version: 1.0.0
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from enum import Enum
from openai import OpenAI

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent))
try:
    from config import config
except ImportError:
    config = None


class CauseCategory(Enum):
    """Root cause categories based on CCPS framework."""
    EQUIPMENT_MATERIAL = "Equipment/Material"
    HUMAN_PERSONNEL = "Human/Personnel"
    ORGANIZATIONAL_MANAGEMENT = "Organizational/Management"
    EXTERNAL = "External"


class CauseSeverity(Enum):
    """Severity level of identified causes."""
    CRITICAL = "critical"
    MAJOR = "major"
    MODERATE = "moderate"
    MINOR = "minor"


class RootCauseAnalysisAgent:
    """
    Agent for performing structured root cause analysis.
    
    Applies multiple frameworks systematically:
    1. CCPS Guidelines - Industry standard for process safety
    2. TapRoot® - Systematic cause tree analysis
    3. 5M+E - Categorical breakdown
    4. Causal chain mapping
    
    Example:
        >>> agent = RootCauseAnalysisAgent()
        >>> results = agent.analyze_causes(
        ...     evidence_summary="Fire in vessel V-301 due to cooling failure",
        ...     timeline_events=[...]
        ... )
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Root Cause Analysis Agent.
        
        Args:
            api_key: OpenAI API key (deprecated, use .env instead)
        """
        # Load configuration from .env or use provided api_key (legacy)
        if config:
            config.validate()
            self.api_key = config.OPENAI_API_KEY
            self.openai_config = config.get_openai_client_config()
        else:
            # Fallback to legacy parameter or environment variable
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            self.openai_config = {
                'model': os.getenv('OPENAI_MODEL', 'gpt-4o'),
                'temperature': float(os.getenv('OPENAI_TEMPERATURE', '0.2'))
            }
        
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
        
        # Load taxonomies
        self.ccps_taxonomy = self._load_ccps_taxonomy()
        self.taproot_taxonomy = self._load_taproot_taxonomy()
        
        print("RootCauseAnalysisAgent initialized")
        if config:
            print(f"  - Model: {config.OPENAI_MODEL}")
    
    def _load_ccps_taxonomy(self) -> Dict:
        """Load CCPS root cause taxonomy."""
        return {
            "Equipment/Material": [
                "Equipment failure",
                "Design deficiency",
                "Material defect",
                "Installation error",
                "Maintenance inadequate"
            ],
            "Human/Personnel": [
                "Operator error",
                "Procedural non-compliance",
                "Training inadequate",
                "Lack of awareness",
                "Fatigue",
                "Communication failure"
            ],
            "Organizational/Management": [
                "Management system failure",
                "Procedure deficiency",
                "Safety culture weakness",
                "Resource allocation inadequate",
                "Risk assessment inadequate",
                "Management of Change not followed",
                "Mechanical integrity program gap",
                "Emergency response inadequate"
            ],
            "External": [
                "Natural disaster",
                "Third-party action",
                "Regulatory change",
                "Supply chain failure"
            ]
        }
    
    def _load_taproot_taxonomy(self) -> List:
        """Load TapRoot® cause categories."""
        return [
            "Equipment Problem",
            "Human Performance Problem",
            "Procedure/Training Problem",
            "Work Direction Problem",
            "Quality Control Problem",
            "Management System Problem"
        ]
    
    def analyze_causes(
        self,
        evidence_summary: str,
        timeline_events: List[Dict],
        incident_type: str,
        industry: str
    ) -> Dict[str, Any]:
        """
        Perform comprehensive root cause analysis.
        
        Args:
            evidence_summary: Summary of all evidence
            timeline_events: Chronological event sequence
            incident_type: Type of incident (fire, explosion, etc.)
            industry: Industry sector (oil_and_gas, chemical, etc.)
        
        Returns:
            Root cause analysis results:
                - immediate_causes: Direct triggers
                - contributing_factors: Enabling conditions
                - systemic_causes: Organizational failures
                - causal_chain: Sequence of cause-effect relationships
                - framework_analysis: Results from each framework
        """
        print("Performing root cause analysis...")
        
        results = {
            "immediate_causes": [],
            "contributing_factors": [],
            "systemic_causes": [],
            "causal_chain": [],
            "framework_analysis": {}
        }
        
        # Apply CCPS Framework
        print("  Applying CCPS Guidelines...")
        ccps_results = self._apply_ccps_framework(
            evidence_summary,
            timeline_events,
            incident_type
        )
        results["framework_analysis"]["CCPS"] = ccps_results
        results["immediate_causes"].extend(ccps_results.get("immediate", []))
        results["contributing_factors"].extend(ccps_results.get("contributing", []))
        results["systemic_causes"].extend(ccps_results.get("systemic", []))
        
        # Apply TapRoot® Framework
        print("  Applying TapRoot® methodology...")
        taproot_results = self._apply_taproot_framework(
            evidence_summary,
            timeline_events
        )
        results["framework_analysis"]["TapRoot"] = taproot_results
        
        # Apply 5M+E Analysis
        print("  Applying 5M+E analysis...")
        five_m_e_results = self._apply_5m_e_framework(
            evidence_summary,
            incident_type
        )
        results["framework_analysis"]["5M_E"] = five_m_e_results
        
        # Build causal chain
        print("  Building causal chain...")
        results["causal_chain"] = self._build_causal_chain(
            results["immediate_causes"],
            results["contributing_factors"],
            results["systemic_causes"]
        )
        
        # Deduplicate and prioritize
        results = self._deduplicate_and_prioritize(results)
        
        print(f"✓ Identified {len(results['immediate_causes'])} immediate causes")
        print(f"✓ Identified {len(results['systemic_causes'])} systemic causes")
        
        return results
    
    def _apply_ccps_framework(
        self,
        evidence_summary: str,
        timeline_events: List[Dict],
        incident_type: str
    ) -> Dict:
        """
        Apply CCPS Guidelines framework.
        
        Categories:
        - Equipment/Material failures
        - Human/Personnel factors
        - Organizational/Management issues
        - External factors
        """
        if self.client:
            # Use LLM to analyze causes using CCPS framework
            prompt = f"""
            You are an expert incident investigator using CCPS (Center for Chemical Process Safety) Guidelines.
            
            Analyze this incident and identify root causes in these categories:
            1. Equipment/Material causes (failures, design flaws, maintenance issues)
            2. Human/Personnel causes (errors, training gaps, fatigue)
            3. Organizational/Management causes (system failures, procedure gaps, culture issues)
            4. External causes (if applicable)
            
            For each cause identified:
            - Classify as: Immediate (direct trigger), Contributing (enabling condition), or Systemic (organizational failure)
            - Assign confidence score (0-1)
            - Reference supporting evidence
            
            Incident Type: {incident_type}
            
            Evidence Summary:
            {evidence_summary}
            
            Timeline:
            {json.dumps(timeline_events, indent=2)}
            
            Provide structured JSON output with causes categorized by CCPS framework and classified by level (immediate/contributing/systemic).
            """
            
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are an expert process safety investigator trained in CCPS methodologies."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2
                )
                
                content = response.choices[0].message.content
                analysis = json.loads(content)
                
                return analysis
            
            except Exception as e:
                print(f"Warning: LLM analysis failed: {e}")
        
        # Fallback: Rule-based analysis
        return self._fallback_ccps_analysis(incident_type)
    
    def _fallback_ccps_analysis(self, incident_type: str) -> Dict:
        """Fallback rule-based CCPS analysis."""
        analysis = {
            "immediate": [
                {
                    "cause": f"{incident_type.capitalize()} initiated",
                    "category": "Equipment/Material",
                    "subcategory": "Equipment failure",
                    "confidence": 0.7,
                    "evidence_refs": []
                }
            ],
            "contributing": [
                {
                    "factor": "Inadequate monitoring or alarm system",
                    "category": "Equipment/Material",
                    "confidence": 0.6
                },
                {
                    "factor": "Procedural compliance gap",
                    "category": "Human/Personnel",
                    "confidence": 0.6
                }
            ],
            "systemic": [
                {
                    "cause": "Management of Change (MOC) process not followed",
                    "category": "Organizational/Management",
                    "standard_violated": "OSHA PSM Element 8",
                    "severity": "major",
                    "confidence": 0.5
                },
                {
                    "cause": "Training program inadequate",
                    "category": "Organizational/Management",
                    "standard_violated": "OSHA PSM Element 9",
                    "severity": "moderate",
                    "confidence": 0.5
                }
            ]
        }
        
        return analysis
    
    def _apply_taproot_framework(
        self,
        evidence_summary: str,
        timeline_events: List[Dict]
    ) -> Dict:
        """
        Apply TapRoot® root cause tree methodology.
        
        Uses decision tree approach to drill down systematically.
        """
        # Simplified TapRoot® analysis
        # In production, implement full decision tree logic
        
        return {
            "root_category": "Management System Problem",
            "subcategories": [
                "Procedure/Training Problem",
                "Quality Control Problem"
            ],
            "root_causes": [
                "Procedure not adequate",
                "Training not adequate",
                "No independent verification"
            ]
        }
    
    def _apply_5m_e_framework(
        self,
        evidence_summary: str,
        incident_type: str
    ) -> Dict:
        """
        Apply 5M+E framework for categorical analysis.
        
        Categories:
        - Man (Human factors)
        - Machine (Equipment)
        - Material (Substances)
        - Method (Procedures)
        - Measurement (Monitoring)
        - Environment (Conditions)
        - Management (Systems)
        """
        categories = {
            "Man": [],
            "Machine": [],
            "Material": [],
            "Method": [],
            "Measurement": [],
            "Environment": [],
            "Management": []
        }
        
        # Simplified categorization
        # In production, use LLM or rule-based logic to populate
        
        categories["Machine"].append("Equipment failure or malfunction")
        categories["Method"].append("Procedure not followed or inadequate")
        categories["Measurement"].append("Inadequate monitoring or alarm system")
        categories["Management"].append("Management system weakness")
        
        return categories
    
    def _build_causal_chain(
        self,
        immediate_causes: List[Dict],
        contributing_factors: List[Dict],
        systemic_causes: List[Dict]
    ) -> List[Dict]:
        """
        Build causal chain showing cause-effect relationships.
        
        Example chain:
        Systemic Cause → Contributing Factor → Immediate Cause → Incident
        """
        chain = []
        
        # Simplified chain building
        # In production, use graph analysis to map relationships
        
        if systemic_causes:
            chain.append({
                "level": "systemic",
                "cause": systemic_causes[0].get("cause", "Systemic failure"),
                "leads_to": "contributing_factors"
            })
        
        if contributing_factors:
            chain.append({
                "level": "contributing",
                "cause": contributing_factors[0].get("factor", "Contributing condition"),
                "leads_to": "immediate_causes"
            })
        
        if immediate_causes:
            chain.append({
                "level": "immediate",
                "cause": immediate_causes[0].get("cause", "Direct trigger"),
                "leads_to": "incident"
            })
        
        return chain
    
    def _deduplicate_and_prioritize(self, results: Dict) -> Dict:
        """Remove duplicates and prioritize causes by severity and confidence."""
        # Simplified deduplication
        # In production, implement fuzzy matching and semantic similarity
        
        # Prioritize systemic causes by severity
        if results["systemic_causes"]:
            severity_order = {"critical": 0, "major": 1, "moderate": 2, "minor": 3}
            results["systemic_causes"].sort(
                key=lambda x: severity_order.get(x.get("severity", "minor"), 4)
            )
        
        return results
    
    def generate_five_why_analysis(
        self,
        incident_description: str,
        evidence_summary: str
    ) -> Dict:
        """
        Generate 5 Why analysis.
        
        Iteratively asks "Why?" to drill down to root cause.
        
        Args:
            incident_description: Description of what happened
            evidence_summary: Summary of evidence
        
        Returns:
            5 Why analysis with each level of "why"
        """
        if self.client:
            prompt = f"""
            Perform a 5 Why analysis for this incident.
            
            Start with: {incident_description}
            
            For each level, ask "Why did this happen?" and provide the answer based on evidence.
            Continue for at least 5 levels until you reach the root cause.
            
            Evidence:
            {evidence_summary}
            
            Provide structured output showing each "Why?" level.
            """
            
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are an expert in root cause analysis using 5 Why methodology."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3
                )
                
                content = response.choices[0].message.content
                
                # Parse into structured format
                return {
                    "method": "5_Why",
                    "starting_event": incident_description,
                    "analysis": content,
                    "root_cause_reached": True
                }
            
            except Exception as e:
                print(f"Warning: 5 Why analysis failed: {e}")
        
        # Fallback
        return {
            "method": "5_Why",
            "starting_event": incident_description,
            "levels": [
                {"why": 1, "question": "Why did incident occur?", "answer": "Equipment failed"},
                {"why": 2, "question": "Why did equipment fail?", "answer": "Maintenance inadequate"},
                {"why": 3, "question": "Why was maintenance inadequate?", "answer": "Procedure not followed"},
                {"why": 4, "question": "Why was procedure not followed?", "answer": "Training gap"},
                {"why": 5, "question": "Why was there a training gap?", "answer": "Management system weakness"}
            ],
            "root_cause": "Management system weakness (training program inadequate)"
        }
    
    def map_to_regulatory_standards(self, causes: List[Dict], standards: List[str]) -> Dict:
        """
        Map identified causes to regulatory standard violations.
        
        Args:
            causes: List of identified causes
            standards: Applicable standards (OSHA_PSM, API_RP_754, etc.)
        
        Returns:
            Mapping of causes to standard elements
        """
        mapping = {}
        
        # OSHA PSM mapping
        if "OSHA_PSM" in standards:
            osha_psm_elements = {
                "Process Safety Information": [],
                "Process Hazard Analysis": [],
                "Operating Procedures": [],
                "Training": [],
                "Contractors": [],
                "Pre-Startup Safety Review": [],
                "Mechanical Integrity": [],
                "Management of Change": [],
                "Incident Investigation": [],
                "Emergency Planning and Response": [],
                "Compliance Audits": []
            }
            
            # Map causes to elements
            for cause in causes:
                cause_text = cause.get("cause", "").lower()
                
                if "training" in cause_text:
                    osha_psm_elements["Training"].append(cause)
                elif "procedure" in cause_text:
                    osha_psm_elements["Operating Procedures"].append(cause)
                elif "moc" in cause_text or "management of change" in cause_text:
                    osha_psm_elements["Management of Change"].append(cause)
                elif "maintenance" in cause_text or "mechanical integrity" in cause_text:
                    osha_psm_elements["Mechanical Integrity"].append(cause)
            
            mapping["OSHA_PSM"] = osha_psm_elements
        
        return mapping


if __name__ == "__main__":
    # Example usage
    print("Root Cause Analysis Agent - Test Run")
    print("======================================\n")
    
    agent = RootCauseAnalysisAgent()
    
    # Perform root cause analysis
    results = agent.analyze_causes(
        evidence_summary="Fire in vessel V-301. Cooling water flow stopped. Valve HV-305 found closed. Operator did not verify valve position during maintenance.",
        timeline_events=[
            {"time": "14:18", "event": "Maintenance started on cooling system"},
            {"time": "14:28", "event": "High temperature alarm activated"},
            {"time": "14:30", "event": "Fire initiated in V-301"}
        ],
        incident_type="fire",
        industry="oil_and_gas"
    )
    
    print("\nRoot Cause Analysis Results:")
    print("="*50)
    print(f"\nImmediate Causes ({len(results['immediate_causes'])}):")
    for cause in results['immediate_causes']:
        print(f"  - {cause.get('cause')}")
    
    print(f"\nSystemic Causes ({len(results['systemic_causes'])}):")
    for cause in results['systemic_causes']:
        print(f"  - {cause.get('cause')} (Severity: {cause.get('severity', 'unknown')})")
    
    # Generate 5 Why analysis
    print("\n" + "="*50)
    five_why = agent.generate_five_why_analysis(
        incident_description="Fire occurred in vessel V-301",
        evidence_summary="Cooling failure led to overheating"
    )
    
    print("\n5 Why Analysis:")
    if "levels" in five_why:
        for level in five_why["levels"]:
            print(f"  Why {level['why']}: {level['answer']}")
    
    print(f"\n✓ Root cause identified: {five_why.get('root_cause', 'See analysis')}")
