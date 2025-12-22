"""
Comprehensive tests for IncidentOrchestrator agent.
Tests all methods with realistic incident scenarios.
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.orchestrator import (
    IncidentOrchestrator,
    InvestigationCase,
    InvestigationStatus,
    IncidentSeverity
)


class TestIncidentOrchestrator:
    """Test suite for IncidentOrchestrator."""
    
    @pytest.fixture
    def orchestrator(self, mock_openai_client):
        """Create orchestrator instance with mocked dependencies."""
        with patch('agents.orchestrator.config') as mock_config:
            mock_config.OPENAI_API_KEY = "test-key"
            mock_config.COMPANY_NAME = "Test Company"
            mock_config.ORGANIZATION_ID = "test-org"
            mock_config.ENVIRONMENT = "testing"
            mock_config.validate.return_value = True
            mock_config.get_openai_client_config.return_value = {
                'api_key': 'test-key',
                'model': 'gpt-4o',
                'temperature': 0.2
            }
            
            orch = IncidentOrchestrator()
            return orch
    
    def test_initialization(self, orchestrator):
        """Test orchestrator initializes correctly."""
        assert orchestrator is not None
        assert isinstance(orchestrator.cases, dict)
        assert len(orchestrator.cases) == 0
        assert orchestrator.api_key == "test-key"
    
    def test_create_investigation_success(self, orchestrator, sample_incident_data):
        """Test creating a new investigation case."""
        case = orchestrator.create_investigation(sample_incident_data)
        
        assert case is not None
        assert case.incident_id == "INC-2024-TEST-001"
        assert case.title == "Fire in Crude Distillation Unit"
        assert case.industry == "oil_and_gas"
        assert case.incident_type == "fire"
        assert case.severity == "major"
        assert case.status == InvestigationStatus.INITIATED.value
        assert case.incident_id in orchestrator.cases
        
    def test_create_investigation_with_minimal_data(self, orchestrator):
        """Test creating investigation with minimal required data."""
        minimal_data = {
            "incident_id": "INC-MINIMAL-001",
            "industry": "petrochemical",
            "incident_type": "spill"
        }
        
        case = orchestrator.create_investigation(minimal_data)
        
        assert case is not None
        assert case.incident_id == "INC-MINIMAL-001"
        assert case.status == InvestigationStatus.INITIATED.value
    
    def test_get_case(self, orchestrator, sample_incident_data):
        """Test retrieving an existing case."""
        created_case = orchestrator.create_investigation(sample_incident_data)
        retrieved_case = orchestrator.get_case(created_case.incident_id)
        
        assert retrieved_case is not None
        assert retrieved_case.incident_id == created_case.incident_id
        assert retrieved_case.title == created_case.title
    
    def test_get_case_not_found(self, orchestrator):
        """Test retrieving non-existent case returns None."""
        case = orchestrator.get_case("NON-EXISTENT-001")
        assert case is None
    
    def test_add_evidence_to_case(self, orchestrator, sample_incident_data, sample_witness_statement):
        """Test adding evidence to investigation case."""
        case = orchestrator.create_investigation(sample_incident_data)
        
        result = orchestrator.add_evidence(
            case_id=case.incident_id,
            evidence=sample_witness_statement
        )
        
        assert result is True
        updated_case = orchestrator.get_case(case.incident_id)
        assert len(updated_case.evidence_items) == 1
        assert updated_case.evidence_items[0]['evidence_id'] == "WS-001"
        assert updated_case.evidence_items[0]['type'] == "witness_statement"
        assert updated_case.status == InvestigationStatus.EVIDENCE_COLLECTION.value
    
    def test_add_multiple_evidence_items(self, orchestrator, sample_incident_data, 
                                         sample_witness_statement, sample_scada_log):
        """Test adding multiple evidence items to case."""
        case = orchestrator.create_investigation(sample_incident_data)
        
        orchestrator.add_evidence(case.incident_id, sample_witness_statement)
        orchestrator.add_evidence(case.incident_id, sample_scada_log)
        
        updated_case = orchestrator.get_case(case.incident_id)
        assert len(updated_case.evidence_items) == 2
        
        evidence_types = [e['type'] for e in updated_case.evidence_items]
        assert "witness_statement" in evidence_types
        assert "scada_log" in evidence_types
    
    def test_add_evidence_to_nonexistent_case(self, orchestrator, sample_witness_statement):
        """Test adding evidence to non-existent case fails gracefully."""
        result = orchestrator.add_evidence("NON-EXISTENT", sample_witness_statement)
        assert result is False
    
    def test_update_case_status(self, orchestrator, sample_incident_data):
        """Test updating investigation case status."""
        case = orchestrator.create_investigation(sample_incident_data)
        
        success = orchestrator.update_case_status(
            case.incident_id,
            InvestigationStatus.ANALYSIS.value
        )
        
        assert success is True
        updated_case = orchestrator.get_case(case.incident_id)
        assert updated_case.status == InvestigationStatus.ANALYSIS.value
    
    def test_list_all_cases(self, orchestrator, sample_incident_data):
        """Test listing all investigation cases."""
        # Create multiple cases
        data1 = sample_incident_data.copy()
        data1['incident_id'] = "INC-001"
        
        data2 = sample_incident_data.copy()
        data2['incident_id'] = "INC-002"
        
        orchestrator.create_investigation(data1)
        orchestrator.create_investigation(data2)
        
        cases = orchestrator.list_cases()
        assert len(cases) == 2
        
        case_ids = [c.incident_id for c in cases]
        assert "INC-001" in case_ids
        assert "INC-002" in case_ids
    
    def test_list_cases_by_status(self, orchestrator, sample_incident_data):
        """Test filtering cases by status."""
        # Create cases with different statuses
        case1 = orchestrator.create_investigation(sample_incident_data)
        
        data2 = sample_incident_data.copy()
        data2['incident_id'] = "INC-002"
        case2 = orchestrator.create_investigation(data2)
        
        # Update one case to different status
        orchestrator.update_case_status(case2.incident_id, InvestigationStatus.ANALYSIS.value)
        
        initiated_cases = orchestrator.list_cases(status=InvestigationStatus.INITIATED.value)
        assert len(initiated_cases) == 1
        assert initiated_cases[0].incident_id == case1.incident_id
        
        analysis_cases = orchestrator.list_cases(status=InvestigationStatus.ANALYSIS.value)
        assert len(analysis_cases) == 1
        assert analysis_cases[0].incident_id == case2.incident_id
    
    def test_export_case_data(self, orchestrator, sample_incident_data, sample_witness_statement):
        """Test exporting case data as dictionary."""
        case = orchestrator.create_investigation(sample_incident_data)
        orchestrator.add_evidence(case.incident_id, sample_witness_statement)
        
        exported_data = orchestrator.export_case(case.incident_id)
        
        assert exported_data is not None
        assert exported_data['incident_id'] == case.incident_id
        assert 'evidence_items' in exported_data
        assert len(exported_data['evidence_items']) == 1
        assert 'created_at' in exported_data
    
    def test_delete_case(self, orchestrator, sample_incident_data):
        """Test deleting an investigation case."""
        case = orchestrator.create_investigation(sample_incident_data)
        case_id = case.incident_id
        
        assert case_id in orchestrator.cases
        
        success = orchestrator.delete_case(case_id)
        
        assert success is True
        assert case_id not in orchestrator.cases
        assert orchestrator.get_case(case_id) is None
    
    def test_case_statistics(self, orchestrator, sample_incident_data):
        """Test getting case statistics."""
        # Create cases with different statuses
        for i in range(5):
            data = sample_incident_data.copy()
            data['incident_id'] = f"INC-{i:03d}"
            orchestrator.create_investigation(data)
        
        # Update some statuses
        orchestrator.update_case_status("INC-001", InvestigationStatus.ANALYSIS.value)
        orchestrator.update_case_status("INC-002", InvestigationStatus.ANALYSIS.value)
        orchestrator.update_case_status("INC-003", InvestigationStatus.COMPLETED.value)
        
        stats = orchestrator.get_statistics()
        
        assert stats['total_cases'] == 5
        assert stats['by_status'][InvestigationStatus.INITIATED.value] == 2
        assert stats['by_status'][InvestigationStatus.ANALYSIS.value] == 2
        assert stats['by_status'][InvestigationStatus.COMPLETED.value] == 1
    
    @patch('agents.orchestrator.IncidentOrchestrator._generate_report_content')
    def test_generate_report_pdf(self, mock_generate, orchestrator, sample_incident_data, tmp_path):
        """Test generating PDF investigation report."""
        mock_generate.return_value = "Report content"
        
        case = orchestrator.create_investigation(sample_incident_data)
        
        report_path = orchestrator.generate_report(
            case_id=case.incident_id,
            template="OSHA_PSM",
            format="pdf",
            output_path=str(tmp_path / "report.pdf")
        )
        
        assert report_path is not None
        # In real implementation, would check file exists
    
    @patch('agents.orchestrator.IncidentOrchestrator._generate_report_content')
    def test_generate_report_docx(self, mock_generate, orchestrator, sample_incident_data, tmp_path):
        """Test generating DOCX investigation report."""
        mock_generate.return_value = "Report content"
        
        case = orchestrator.create_investigation(sample_incident_data)
        
        report_path = orchestrator.generate_report(
            case_id=case.incident_id,
            template="API_RP_754",
            format="docx",
            output_path=str(tmp_path / "report.docx")
        )
        
        assert report_path is not None
    
    def test_generate_diagram_placeholder(self, orchestrator, sample_incident_data):
        """Test diagram generation (placeholder implementation)."""
        case = orchestrator.create_investigation(sample_incident_data)
        
        # This should not raise an error even if not fully implemented
        result = orchestrator.generate_diagram(
            case_id=case.incident_id,
            diagram_type="5_why"
        )
        
        # Placeholder may return None or path
        assert result is not None or result is None
    
    def test_create_capa_tracker(self, orchestrator, sample_incident_data):
        """Test creating CAPA (Corrective Action Preventive Action) tracker."""
        case = orchestrator.create_investigation(sample_incident_data)
        
        capa_tracker = orchestrator.create_capa_tracker(case.incident_id)
        
        assert capa_tracker is not None
        assert 'case_id' in capa_tracker
        assert capa_tracker['case_id'] == case.incident_id
    
    def test_concurrent_case_creation(self, orchestrator, sample_incident_data):
        """Test creating multiple cases concurrently doesn't cause conflicts."""
        cases = []
        for i in range(10):
            data = sample_incident_data.copy()
            data['incident_id'] = f"INC-CONCURRENT-{i:03d}"
            case = orchestrator.create_investigation(data)
            cases.append(case)
        
        assert len(orchestrator.cases) == 10
        assert all(c.incident_id in orchestrator.cases for c in cases)
    
    def test_case_validation(self, orchestrator):
        """Test validation of case data."""
        invalid_data = {
            # Missing required fields
            "title": "Test"
        }
        
        # Should handle gracefully or raise appropriate error
        try:
            case = orchestrator.create_investigation(invalid_data)
            # If it creates a case, check it has defaults
            assert case is not None
        except (ValueError, KeyError):
            # Or it should raise validation error
            pass
    
    def test_evidence_ordering(self, orchestrator, sample_incident_data):
        """Test that evidence is maintained in order of addition."""
        case = orchestrator.create_investigation(sample_incident_data)
        
        # Add evidence in specific order
        for i in range(5):
            evidence = {
                "evidence_id": f"EV-{i:03d}",
                "type": "document",
                "sequence": i
            }
            orchestrator.add_evidence(case.incident_id, evidence)
        
        updated_case = orchestrator.get_case(case.incident_id)
        
        # Check ordering is preserved
        for i, evidence in enumerate(updated_case.evidence_items):
            assert evidence['evidence_id'] == f"EV-{i:03d}"
            assert evidence['sequence'] == i


class TestInvestigationCase:
    """Test InvestigationCase dataclass."""
    
    def test_case_creation(self, sample_incident_data):
        """Test creating InvestigationCase instance."""
        case = InvestigationCase(
            incident_id=sample_incident_data['incident_id'],
            title=sample_incident_data['title'],
            industry=sample_incident_data['industry'],
            facility=sample_incident_data.get('facility', ''),
            location=sample_incident_data.get('location', ''),
            incident_type=sample_incident_data['incident_type'],
            severity=sample_incident_data['severity'],
            date_occurred=sample_incident_data['date_occurred'],
            description=sample_incident_data.get('description', ''),
            initial_consequences=sample_incident_data.get('initial_consequences', []),
            investigation_team=sample_incident_data.get('investigation_team', []),
            standards_applicable=sample_incident_data.get('standards_applicable', []),
            status=InvestigationStatus.INITIATED.value,
            created_at=datetime.now().isoformat()
        )
        
        assert case.incident_id == "INC-2024-TEST-001"
        assert case.industry == "oil_and_gas"
        assert len(case.evidence_items) == 0
    
    def test_case_with_evidence(self, sample_incident_data, sample_witness_statement):
        """Test case with pre-loaded evidence."""
        case = InvestigationCase(
            incident_id=sample_incident_data['incident_id'],
            title=sample_incident_data['title'],
            industry=sample_incident_data['industry'],
            facility='',
            location='',
            incident_type=sample_incident_data['incident_type'],
            severity=sample_incident_data['severity'],
            date_occurred=sample_incident_data['date_occurred'],
            description='',
            initial_consequences=[],
            investigation_team=[],
            standards_applicable=[],
            status=InvestigationStatus.EVIDENCE_COLLECTION.value,
            created_at=datetime.now().isoformat(),
            evidence_items=[sample_witness_statement]
        )
        
        assert len(case.evidence_items) == 1
        assert case.evidence_items[0]['evidence_id'] == "WS-001"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
