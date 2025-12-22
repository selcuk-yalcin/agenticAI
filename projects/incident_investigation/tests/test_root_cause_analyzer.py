"""
Comprehensive tests for RootCauseAnalysisAgent.
Tests all RCA frameworks and methods.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.root_cause_analyzer import (
    RootCauseAnalysisAgent,
    CauseCategory,
    CauseSeverity
)


class TestRootCauseAnalysisAgent:
    """Test suite for Root Cause Analysis Agent."""
    
    @pytest.fixture
    def agent(self, mock_openai_client):
        """Create agent instance with mocked OpenAI client."""
        with patch('agents.root_cause_analyzer.OpenAI') as mock_openai:
            mock_openai.return_value = mock_openai_client
            
            with patch('agents.root_cause_analyzer.config') as mock_config:
                mock_config.OPENAI_API_KEY = "test-key"
                mock_config.OPENAI_MODEL = "gpt-4o"
                mock_config.validate.return_value = True
                mock_config.get_openai_client_config.return_value = {
                    'api_key': 'test-key',
                    'model': 'gpt-4o',
                    'temperature': 0.2
                }
                
                agent = RootCauseAnalysisAgent()
                agent.client = mock_openai_client
                return agent
    
    def test_initialization(self, agent):
        """Test agent initializes with frameworks."""
        assert agent is not None
        assert agent.api_key == "test-key"
        assert agent.ccps_taxonomy is not None
        assert agent.taproot_taxonomy is not None
    
    def test_analyze_causes_complete(self, agent, sample_timeline_events, mock_openai_client):
        """Test complete root cause analysis."""
        evidence_summary = """
        Fire in crude distillation unit caused by cooling water pump failure.
        Pump impeller had 40% wear. Maintenance was deferred despite recommendations.
        Operator response delayed due to unclear procedures.
        """
        
        mock_response = {
            "immediate_causes": [
                {
                    "cause": "Cooling water pump impeller failure",
                    "category": "Equipment/Material",
                    "confidence": 0.95,
                    "evidence": ["Impeller 40% worn", "Flow dropped to 100 GPM"]
                }
            ],
            "contributing_factors": [
                {
                    "cause": "Deferred preventive maintenance",
                    "category": "Organizational/Management",
                    "confidence": 0.85,
                    "evidence": ["Maintenance delayed from December to April"]
                },
                {
                    "cause": "Inadequate alarm response procedures",
                    "category": "Human/Personnel",
                    "confidence": 0.75,
                    "evidence": ["10-minute delay in emergency shutdown"]
                }
            ],
            "systemic_causes": [
                {
                    "cause": "Weak mechanical integrity program",
                    "category": "Organizational/Management",
                    "confidence": 0.80,
                    "evidence": ["Pattern of deferred maintenance", "Budget constraints"]
                }
            ],
            "causal_chain": [
                "Budget constraints → Deferred maintenance",
                "Impeller wear → Pump failure",
                "Pump failure → Loss of cooling",
                "Loss of cooling → Overheat → Fire"
            ]
        }
        
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = str(mock_response)
        
        result = agent.analyze_causes(evidence_summary, sample_timeline_events)
        
        assert result is not None
        assert 'immediate_causes' in result or 'contributing_factors' in result
    
    def test_apply_ccps_framework(self, agent, mock_openai_client):
        """Test CCPS framework application."""
        evidence_summary = "Pump failure due to worn impeller"
        
        mock_response = {
            "Equipment/Material": [
                {
                    "cause": "Impeller wear beyond limits",
                    "subcategory": "Equipment failure",
                    "confidence": 0.9
                }
            ],
            "Organizational/Management": [
                {
                    "cause": "Inadequate maintenance program",
                    "subcategory": "Management system deficiency",
                    "confidence": 0.85
                }
            ]
        }
        
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = str(mock_response)
        
        result = agent._apply_ccps_framework(evidence_summary)
        
        assert result is not None
    
    def test_apply_taproot_framework(self, agent, mock_openai_client):
        """Test TapRoot® framework application."""
        evidence_summary = "Operator delayed emergency shutdown"
        
        mock_response = {
            "root_causes": [
                {
                    "category": "Training Deficiency",
                    "cause": "Inadequate emergency response training",
                    "path": "Human Error → Training → Inadequate Practice"
                }
            ],
            "decision_tree_path": ["Human Error", "Training", "Inadequate Practice"]
        }
        
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = str(mock_response)
        
        result = agent._apply_taproot_framework(evidence_summary)
        
        assert result is not None
    
    def test_apply_5m_e_framework(self, agent, mock_openai_client):
        """Test 5M+E framework application."""
        evidence_summary = "Multiple failures leading to incident"
        
        mock_response = {
            "Man": ["Operator response delay", "Inadequate training"],
            "Machine": ["Pump impeller failure", "Worn equipment"],
            "Material": ["Coolant system degradation"],
            "Method": ["Unclear emergency procedures"],
            "Measurement": ["Delayed alarm recognition"],
            "Environment": ["High ambient temperature stress"],
            "Management": ["Deferred maintenance decisions", "Budget constraints"]
        }
        
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = str(mock_response)
        
        result = agent._apply_5m_e_framework(evidence_summary)
        
        assert result is not None
        assert any(key in result for key in ["Man", "Machine", "Material", "Method"])
    
    def test_generate_five_why_analysis(self, agent, mock_openai_client):
        """Test 5 Why iterative analysis."""
        incident_description = "Fire in distillation unit"
        
        mock_response = {
            "why_1": {
                "question": "Why did fire occur?",
                "answer": "High temperature in vessel exceeded ignition point"
            },
            "why_2": {
                "question": "Why was temperature high?",
                "answer": "Cooling water flow stopped"
            },
            "why_3": {
                "question": "Why did cooling flow stop?",
                "answer": "Pump impeller failed"
            },
            "why_4": {
                "question": "Why did impeller fail?",
                "answer": "Excessive wear (40%) not addressed"
            },
            "why_5": {
                "question": "Why was wear not addressed?",
                "answer": "Maintenance deferred due to budget constraints"
            },
            "root_cause": "Inadequate maintenance funding and prioritization"
        }
        
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = str(mock_response)
        
        result = agent.generate_five_why_analysis(incident_description)
        
        assert result is not None
        assert 'why_1' in result or 'root_cause' in result
    
    def test_map_to_regulatory_standards(self, agent):
        """Test mapping causes to regulatory standards."""
        causes = [
            {
                "cause": "Inadequate mechanical integrity program",
                "category": "Organizational/Management"
            },
            {
                "cause": "Inadequate operator training",
                "category": "Human/Personnel"
            }
        ]
        
        result = agent.map_to_regulatory_standards(causes, ["OSHA_PSM"])
        
        assert result is not None
        assert isinstance(result, dict) or isinstance(result, list)
    
    def test_identify_barrier_failures(self, agent, mock_openai_client):
        """Test identifying failed safety barriers (Swiss Cheese Model)."""
        incident_data = {
            "description": "Fire incident",
            "safety_systems": ["Alarm", "Emergency shutdown", "Fire suppression"],
            "timeline": []
        }
        
        mock_response = {
            "barriers": [
                {
                    "barrier": "High temperature alarm",
                    "status": "Activated but response delayed",
                    "failure_mode": "Human response inadequate"
                },
                {
                    "barrier": "Preventive maintenance",
                    "status": "Failed - maintenance deferred",
                    "failure_mode": "Management decision"
                },
                {
                    "barrier": "Emergency shutdown",
                    "status": "Activated late (10 min delay)",
                    "failure_mode": "Procedural confusion"
                }
            ],
            "holes_aligned": True,
            "incident_severity": "major"
        }
        
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = str(mock_response)
        
        result = agent.identify_barrier_failures(incident_data)
        
        assert result is not None
    
    def test_cause_categorization(self, agent):
        """Test categorizing causes by severity and type."""
        causes = [
            {"cause": "Equipment failure", "category": "Equipment/Material"},
            {"cause": "Training gap", "category": "Human/Personnel"},
            {"cause": "Management system weakness", "category": "Organizational/Management"}
        ]
        
        categorized = agent._categorize_causes(causes)
        
        assert categorized is not None
        assert isinstance(categorized, dict)
    
    def test_causal_chain_construction(self, agent, mock_openai_client):
        """Test constructing causal chain from root to incident."""
        causes = {
            "immediate_causes": ["Pump failure"],
            "contributing_factors": ["Deferred maintenance"],
            "systemic_causes": ["Budget constraints"]
        }
        
        mock_response = {
            "causal_chain": [
                "Budget constraints (systemic)",
                "→ Deferred maintenance (contributing)",
                "→ Impeller wear",
                "→ Pump failure (immediate)",
                "→ Loss of cooling",
                "→ Overheating",
                "→ Fire (incident)"
            ],
            "chain_confidence": 0.88
        }
        
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = str(mock_response)
        
        result = agent.construct_causal_chain(causes)
        
        assert result is not None
    
    def test_confidence_weighting(self, agent):
        """Test confidence scoring for identified causes."""
        cause = {
            "cause": "Equipment failure",
            "evidence": ["Direct observation", "Maintenance log", "Expert analysis"],
            "corroboration": 3
        }
        
        confidence = agent._calculate_confidence(cause)
        
        assert confidence is not None
        assert 0 <= confidence <= 1
    
    def test_multiple_framework_integration(self, agent, mock_openai_client):
        """Test integrating results from multiple frameworks."""
        evidence_summary = "Complex incident with multiple causes"
        
        # Mock responses for different frameworks
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = str({
            "integrated_causes": [
                {
                    "cause": "Equipment failure",
                    "frameworks": ["CCPS", "5M+E"],
                    "confidence": 0.92
                }
            ]
        })
        
        result = agent.analyze_causes(evidence_summary, [])
        
        assert result is not None
    
    def test_osha_psm_element_mapping(self, agent):
        """Test mapping causes to OSHA PSM elements."""
        causes = [
            {"cause": "Inadequate mechanical integrity", "category": "Organizational/Management"},
            {"cause": "Missing process safety information", "category": "Organizational/Management"},
            {"cause": "Operator error", "category": "Human/Personnel"}
        ]
        
        mapping = agent._map_to_osha_psm(causes)
        
        assert mapping is not None
        # Should map to PSM elements like:
        # - Mechanical Integrity
        # - Process Safety Information
        # - Training
    
    def test_api_rp_754_tier_mapping(self, agent):
        """Test mapping to API RP 754 performance indicators."""
        incident_data = {
            "type": "fire",
            "severity": "major",
            "consequences": ["equipment_damage", "production_loss"]
        }
        
        mapping = agent._map_to_api_rp_754(incident_data)
        
        assert mapping is not None
        # Should map to Tier 1 (Loss of Primary Containment) or Tier 2 indicators
    
    def test_human_factors_analysis(self, agent, mock_openai_client):
        """Test analyzing human factors contributions."""
        incident_data = {
            "operator_actions": ["Delayed response", "Incorrect valve operation"],
            "procedures": ["Emergency response SOP"],
            "training_records": ["Last training 2 years ago"]
        }
        
        mock_response = {
            "human_factors": [
                {
                    "factor": "Cognitive overload",
                    "evidence": "Multiple simultaneous alarms"
                },
                {
                    "factor": "Skill decay",
                    "evidence": "Infrequent emergency drills"
                },
                {
                    "factor": "Procedural ambiguity",
                    "evidence": "Unclear shutdown sequence"
                }
            ],
            "classification": "Human error as symptom, not root cause"
        }
        
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = str(mock_response)
        
        result = agent.analyze_human_factors(incident_data)
        
        assert result is not None
    
    def test_organizational_factors_analysis(self, agent, mock_openai_client):
        """Test analyzing organizational/management factors."""
        incident_data = {
            "management_decisions": ["Deferred maintenance", "Reduced staffing"],
            "safety_culture_indicators": ["Budget cuts", "Production pressure"],
            "audit_findings": ["Overdue inspections", "Training gaps"]
        }
        
        mock_response = {
            "organizational_factors": [
                {
                    "factor": "Resource allocation prioritizing production over safety",
                    "severity": "critical"
                },
                {
                    "factor": "Weak safety culture",
                    "indicators": ["Normalized deviance", "Budget constraints"]
                }
            ]
        }
        
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = str(mock_response)
        
        result = agent.analyze_organizational_factors(incident_data)
        
        assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
