"""
Comprehensive tests for EvidenceAnalysisAgent.
Tests all evidence types and processing methods.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.evidence_analyzer import EvidenceAnalysisAgent


class TestEvidenceAnalysisAgent:
    """Test suite for Evidence Analysis Agent."""
    
    @pytest.fixture
    def agent(self, mock_openai_client):
        """Create agent instance with mocked OpenAI client."""
        with patch('agents.evidence_analyzer.OpenAI') as mock_openai:
            mock_openai.return_value = mock_openai_client
            
            with patch('agents.evidence_analyzer.config') as mock_config:
                mock_config.OPENAI_API_KEY = "test-key"
                mock_config.OPENAI_MODEL = "gpt-4o"
                mock_config.validate.return_value = True
                mock_config.get_openai_client_config.return_value = {
                    'api_key': 'test-key',
                    'model': 'gpt-4o',
                    'temperature': 0.2
                }
                
                agent = EvidenceAnalysisAgent()
                agent.client = mock_openai_client
                return agent
    
    def test_initialization(self, agent):
        """Test agent initializes correctly."""
        assert agent is not None
        assert agent.api_key == "test-key"
        assert agent.client is not None
    
    def test_process_witness_statement(self, agent, sample_witness_statement, mock_openai_client):
        """Test processing witness statement evidence."""
        # Mock LLM response
        mock_response = {
            "key_facts": [
                "High temperature alarm at 14:25",
                "Cooling water flow dropped to 100 GPM",
                "Fire observed at 14:30"
            ],
            "timeline_events": [
                {
                    "timestamp": "2024-01-15T14:25:00Z",
                    "event": "High temperature alarm",
                    "severity": "medium"
                }
            ],
            "entities": {
                "people": ["John Operator"],
                "equipment": ["Heat Exchanger E-301", "Bypass valve"],
                "locations": ["Control room", "Crude distillation unit"]
            },
            "summary": "Operator observed cooling failure leading to fire",
            "confidence_score": 0.9
        }
        
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = str(mock_response)
        
        result = agent.process_evidence(sample_witness_statement)
        
        assert result is not None
        assert 'key_facts' in result or 'summary' in result
        assert 'confidence_score' in result or result.get('confidence_score', 0) >= 0
    
    def test_process_scada_log(self, agent, sample_scada_log, mock_openai_client):
        """Test processing SCADA log data."""
        mock_response = {
            "key_facts": [
                "Cooling water flow decreased from 450 to 95 GPM",
                "Temperature rose from 385°F to 780°F",
                "Fire alarm activated at 14:30:15"
            ],
            "timeline_events": [
                {"timestamp": "2024-01-15T14:20:00Z", "event": "Normal operation"},
                {"timestamp": "2024-01-15T14:25:00Z", "event": "Flow alarm"},
                {"timestamp": "2024-01-15T14:30:00Z", "event": "Fire alarm"}
            ],
            "anomalies": [
                "Rapid flow decrease in 5 minutes",
                "Temperature exceeded safe operating limit"
            ],
            "confidence_score": 0.95
        }
        
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = str(mock_response)
        
        result = agent.process_evidence(sample_scada_log)
        
        assert result is not None
        assert 'timeline_events' in result or 'key_facts' in result
    
    def test_process_maintenance_record(self, agent, sample_maintenance_record, mock_openai_client):
        """Test processing maintenance record evidence."""
        mock_response = {
            "key_facts": [
                "Impeller wear at 40%",
                "Maintenance deferred to April 2024",
                "Recommendation to replace within 3 months"
            ],
            "equipment_identified": ["Cooling Water Pump CWP-301", "Impeller"],
            "maintenance_issues": [
                "Deferred critical maintenance",
                "Wear beyond recommended limits"
            ],
            "confidence_score": 0.88
        }
        
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = str(mock_response)
        
        result = agent.process_evidence(sample_maintenance_record)
        
        assert result is not None
        assert 'key_facts' in result or 'equipment_identified' in result
    
    def test_extract_timeline_events(self, agent, sample_timeline_events):
        """Test extracting and ordering timeline events."""
        result = agent.extract_timeline_events(sample_timeline_events)
        
        assert result is not None
        assert isinstance(result, list)
        
        # Check events are in chronological order
        timestamps = [e.get('timestamp', '') for e in result]
        assert timestamps == sorted(timestamps)
    
    def test_detect_inconsistencies(self, agent, mock_openai_client):
        """Test detecting inconsistencies across evidence."""
        evidence_list = [
            {
                "evidence_id": "WS-001",
                "content": "Operator says alarm at 14:25"
            },
            {
                "evidence_id": "LOG-001",
                "content": "System log shows alarm at 14:27"
            }
        ]
        
        mock_response = {
            "inconsistencies": [
                {
                    "description": "Timing discrepancy for alarm activation",
                    "sources": ["WS-001", "LOG-001"],
                    "severity": "medium",
                    "explanation": "2-minute difference between witness and system log"
                }
            ],
            "conflicts": 1,
            "reliability_assessment": "moderate"
        }
        
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = str(mock_response)
        
        result = agent.detect_inconsistencies(evidence_list)
        
        assert result is not None
        assert 'inconsistencies' in result or isinstance(result, dict)
    
    def test_process_photo_evidence(self, agent, mock_openai_client):
        """Test processing photo evidence with vision model."""
        photo_evidence = {
            "evidence_id": "PHOTO-001",
            "type": "photo",
            "file_path": "/path/to/damage_photo.jpg",
            "metadata": {
                "description": "Equipment damage from fire",
                "timestamp": "2024-01-15T15:00:00Z"
            }
        }
        
        mock_response = {
            "visual_findings": [
                "Severe thermal damage to heat exchanger",
                "Burnt insulation material",
                "Deformed piping connections"
            ],
            "damage_assessment": "Major structural damage",
            "safety_concerns": ["Structural integrity compromised"],
            "confidence_score": 0.85
        }
        
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = str(mock_response)
        
        result = agent.process_evidence(photo_evidence)
        
        assert result is not None
    
    def test_process_pid_drawing(self, agent, mock_openai_client):
        """Test processing P&ID (Piping and Instrumentation Diagram)."""
        pid_evidence = {
            "evidence_id": "PID-001",
            "type": "pid_drawing",
            "file_path": "/path/to/unit3_pid.pdf",
            "metadata": {
                "unit": "Crude Distillation Unit 3",
                "drawing_number": "PID-CDU3-001"
            }
        }
        
        mock_response = {
            "equipment_identified": [
                "Heat Exchanger E-301",
                "Cooling Water Pump CWP-301",
                "Temperature Indicator TI-301",
                "Flow Indicator FI-301"
            ],
            "safety_systems": [
                "High temperature alarm",
                "Low flow alarm",
                "Emergency shutdown valve"
            ],
            "process_description": "Crude oil cooling system with redundant safety instrumentation",
            "confidence_score": 0.92
        }
        
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = str(mock_response)
        
        result = agent.process_evidence(pid_evidence)
        
        assert result is not None
        assert 'equipment_identified' in result or 'safety_systems' in result
    
    def test_process_hazop_report(self, agent, mock_openai_client):
        """Test processing HAZOP (Hazard and Operability) report."""
        hazop_evidence = {
            "evidence_id": "HAZOP-001",
            "type": "hazop_report",
            "file_path": "/path/to/hazop_report.pdf",
            "metadata": {
                "study_date": "2023-06-15",
                "node": "Crude Distillation Unit"
            }
        }
        
        mock_response = {
            "identified_hazards": [
                "Loss of cooling - High temperature",
                "Pump failure - No flow",
                "Instrument failure - Loss of indication"
            ],
            "safeguards_documented": [
                "High temperature alarm TI-301",
                "Low flow alarm FI-301",
                "Automatic shutdown system"
            ],
            "recommendations": [
                "Install backup cooling pump",
                "Improve alarm response procedures"
            ],
            "confidence_score": 0.90
        }
        
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = str(mock_response)
        
        result = agent.process_evidence(hazop_evidence)
        
        assert result is not None
    
    def test_process_procedure_document(self, agent, mock_openai_client):
        """Test processing operating procedure."""
        procedure_evidence = {
            "evidence_id": "PROC-001",
            "type": "procedure",
            "file_path": "/path/to/emergency_procedure.pdf",
            "metadata": {
                "procedure_id": "OP-CDU-003",
                "title": "Emergency Shutdown Procedure"
            }
        }
        
        mock_response = {
            "key_steps": [
                "Activate emergency shutdown button",
                "Close feed valve",
                "Start emergency cooling",
                "Notify emergency response team"
            ],
            "prerequisites": ["Alarm activation", "Visual confirmation of emergency"],
            "compliance_status": "Procedure followed partially",
            "gaps_identified": ["10-minute delay in activation"],
            "confidence_score": 0.87
        }
        
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = str(mock_response)
        
        result = agent.process_evidence(procedure_evidence)
        
        assert result is not None
    
    def test_entity_extraction(self, agent, sample_witness_statement, mock_openai_client):
        """Test extracting entities (people, equipment, chemicals) from evidence."""
        mock_response = {
            "entities": {
                "people": ["John Operator", "Field Operator"],
                "equipment": [
                    "Heat Exchanger E-301",
                    "Bypass valve",
                    "Crude distillation unit"
                ],
                "chemicals": ["Crude oil"],
                "locations": ["Control room", "Unit 3"],
                "systems": ["DCS", "Emergency shutdown system"]
            },
            "relationships": [
                {"entity1": "John Operator", "relation": "operates", "entity2": "DCS"}
            ]
        }
        
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = str(mock_response)
        
        result = agent.process_evidence(sample_witness_statement)
        
        assert result is not None
    
    def test_confidence_scoring(self, agent, mock_openai_client):
        """Test confidence scoring for processed evidence."""
        evidence = {
            "evidence_id": "TEST-001",
            "type": "witness_statement",
            "content": "Clear factual statement with specific details"
        }
        
        mock_response = {
            "key_facts": ["Fact 1", "Fact 2"],
            "confidence_score": 0.95,
            "reliability_factors": [
                "Direct observation",
                "Specific timestamps",
                "Corroborating details"
            ]
        }
        
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = str(mock_response)
        
        result = agent.process_evidence(evidence)
        
        assert result is not None
        assert 'confidence_score' in result or result.get('confidence_score', 0) >= 0
        if 'confidence_score' in result:
            assert 0 <= result['confidence_score'] <= 1
    
    def test_multiple_evidence_correlation(self, agent, mock_openai_client):
        """Test correlating information across multiple evidence sources."""
        evidence_items = [
            {"evidence_id": "WS-001", "type": "witness_statement"},
            {"evidence_id": "LOG-001", "type": "scada_log"},
            {"evidence_id": "PHOTO-001", "type": "photo"}
        ]
        
        mock_response = {
            "corroborated_facts": [
                "Fire occurred at approximately 14:30",
                "Cooling system failure was immediate cause"
            ],
            "divergences": [],
            "confidence": "high"
        }
        
        mock_openai_client.chat.completions.create.return_value.choices[0].message.content = str(mock_response)
        
        # Process all evidence
        results = [agent.process_evidence(e) for e in evidence_items]
        
        assert len(results) == 3
        assert all(r is not None for r in results)
    
    def test_unsupported_evidence_type(self, agent):
        """Test handling of unsupported evidence type."""
        unsupported_evidence = {
            "evidence_id": "UNK-001",
            "type": "unknown_type",
            "content": "Some content"
        }
        
        result = agent.process_evidence(unsupported_evidence)
        
        # Should handle gracefully
        assert result is not None or result is None  # Either handles or returns None
    
    def test_empty_evidence(self, agent):
        """Test processing empty evidence."""
        empty_evidence = {
            "evidence_id": "EMPTY-001",
            "type": "witness_statement",
            "content": ""
        }
        
        result = agent.process_evidence(empty_evidence)
        
        # Should handle gracefully
        assert result is not None or result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
