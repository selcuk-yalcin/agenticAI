"""
Pytest configuration and shared fixtures for incident investigation tests.
"""

import pytest
import sys
import os
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, MagicMock

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing without API calls."""
    mock_client = MagicMock()
    
    # Mock chat completion response
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = '{"key": "value"}'
    mock_client.chat.completions.create.return_value = mock_response
    
    return mock_client


@pytest.fixture
def sample_incident_data():
    """Sample incident data for testing."""
    return {
        "incident_id": "INC-2024-TEST-001",
        "title": "Fire in Crude Distillation Unit",
        "industry": "oil_and_gas",
        "facility": "Test Refinery",
        "location": "Houston, TX",
        "incident_type": "fire",
        "severity": "major",
        "date_occurred": "2024-01-15T14:30:00Z",
        "description": "Fire broke out in crude distillation unit due to cooling system failure",
        "initial_consequences": ["Equipment damage", "Production shutdown", "Minor injuries"],
        "investigation_team": ["Lead Investigator", "Process Engineer", "Safety Manager"],
        "standards_applicable": ["OSHA_PSM", "API_RP_754"]
    }


@pytest.fixture
def sample_witness_statement():
    """Sample witness statement evidence."""
    return {
        "evidence_id": "WS-001",
        "type": "witness_statement",
        "file_path": "/path/to/witness_statement.pdf",
        "metadata": {
            "witness_name": "John Operator",
            "position": "Senior Board Operator",
            "date_recorded": "2024-01-15T16:00:00Z"
        },
        "content": """
        I was on duty in the control room when the high-temperature alarm for the crude 
        distillation unit sounded at approximately 14:25. The cooling water flow to heat 
        exchanger E-301 had dropped from normal 450 GPM to less than 100 GPM. I immediately 
        notified the field operator and attempted to open the bypass valve, but the 
        temperature continued rising. At 14:30, I observed flames from the unit through 
        the control room window and initiated emergency shutdown procedures.
        """
    }


@pytest.fixture
def sample_scada_log():
    """Sample SCADA log evidence."""
    return {
        "evidence_id": "SCADA-001",
        "type": "scada_log",
        "file_path": "/path/to/scada_log.csv",
        "metadata": {
            "system": "DCS-Main",
            "time_range": "2024-01-15 14:00 to 14:45"
        },
        "content": """timestamp,tag,value,unit,status
2024-01-15 14:20:00,FI-301-CW,450,GPM,Normal
2024-01-15 14:23:00,FI-301-CW,380,GPM,Warning
2024-01-15 14:25:00,FI-301-CW,95,GPM,Alarm
2024-01-15 14:25:00,TI-301-Outlet,385,°F,Normal
2024-01-15 14:27:00,TI-301-Outlet,520,°F,Warning
2024-01-15 14:29:00,TI-301-Outlet,650,°F,HighAlarm
2024-01-15 14:30:00,TI-301-Outlet,780,°F,Critical
2024-01-15 14:30:15,FIRE-ALARM-ZONE3,1,Boolean,Activated
"""
    }


@pytest.fixture
def sample_maintenance_record():
    """Sample maintenance record evidence."""
    return {
        "evidence_id": "MAINT-001",
        "type": "maintenance_record",
        "file_path": "/path/to/maintenance.pdf",
        "metadata": {
            "equipment": "Cooling Water Pump CWP-301",
            "work_order": "WO-2024-0234"
        },
        "content": """
        Work Order: WO-2024-0234
        Equipment: Cooling Water Pump CWP-301
        Date: 2023-12-20
        
        Work Performed:
        - Replaced mechanical seal
        - Checked bearing clearances
        - Vibration analysis performed
        
        Findings:
        - Impeller wear noted (estimated 40% wear)
        - Recommendation: Replace impeller within 3 months
        
        Status: Deferred to next turnaround (April 2024)
        """
    }


@pytest.fixture
def sample_timeline_events():
    """Sample timeline events."""
    return [
        {
            "timestamp": "2024-01-15T14:20:00Z",
            "event": "Cooling water flow begins decreasing",
            "source": "SCADA log",
            "severity": "low"
        },
        {
            "timestamp": "2024-01-15T14:25:00Z",
            "event": "High temperature alarm activates",
            "source": "Control system",
            "severity": "medium"
        },
        {
            "timestamp": "2024-01-15T14:27:00Z",
            "event": "Operator attempts to open bypass valve",
            "source": "Witness statement",
            "severity": "medium"
        },
        {
            "timestamp": "2024-01-15T14:30:00Z",
            "event": "Fire ignition in distillation unit",
            "source": "Fire alarm system",
            "severity": "critical"
        },
        {
            "timestamp": "2024-01-15T14:30:15Z",
            "event": "Emergency shutdown initiated",
            "source": "Control system log",
            "severity": "critical"
        }
    ]


@pytest.fixture
def sample_root_causes():
    """Sample root cause analysis results."""
    return {
        "immediate_causes": [
            {
                "cause": "Cooling water pump impeller failure",
                "category": "Equipment/Material",
                "confidence": 0.95,
                "evidence": ["Maintenance records show 40% impeller wear", "Flow dropped to 100 GPM"]
            }
        ],
        "contributing_factors": [
            {
                "cause": "Deferred maintenance on critical equipment",
                "category": "Organizational/Management",
                "confidence": 0.85,
                "evidence": ["Impeller replacement deferred despite recommendation"]
            },
            {
                "cause": "Inadequate alarm response procedures",
                "category": "Human/Personnel",
                "confidence": 0.75,
                "evidence": ["10-minute delay between alarm and emergency shutdown"]
            }
        ],
        "systemic_causes": [
            {
                "cause": "Weak mechanical integrity program",
                "category": "Organizational/Management",
                "confidence": 0.80,
                "evidence": ["Pattern of deferred maintenance", "Budget constraints prioritized over safety"]
            }
        ]
    }


@pytest.fixture
def temp_evidence_dir(tmp_path):
    """Create temporary directory for evidence files."""
    evidence_dir = tmp_path / "evidence"
    evidence_dir.mkdir()
    
    # Create sample PDF placeholder
    pdf_file = evidence_dir / "witness_statement.pdf"
    pdf_file.write_text("Sample witness statement content")
    
    # Create sample CSV
    csv_file = evidence_dir / "scada_log.csv"
    csv_file.write_text("timestamp,tag,value\n2024-01-15 14:30:00,TEMP,500")
    
    return evidence_dir


@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch, tmp_path):
    """Setup test environment variables."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key-12345")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4o")
    monkeypatch.setenv("ENVIRONMENT", "testing")
    
    # Set paths to temp directory
    outputs_dir = tmp_path / "outputs"
    outputs_dir.mkdir()
    monkeypatch.setenv("OUTPUTS_DIR", str(outputs_dir))
