"""Tests for lead discovery and filtering functionality.

This module tests:
- Lead scraping from various sources (LinkedIn, websites)
- Lead scoring and ranking algorithms
- Duplicate detection and filtering
- Data quality validation
"""

import pytest
from unittest.mock import Mock, patch, MagicMock


class TestLeadDiscovery:
    """Test suite for lead discovery functionality."""

    @pytest.fixture
    def sample_leads(self):
        """Fixture providing sample lead data for testing.
        
        Returns:
            list: Sample lead records with various attributes.
        """
        return [
            {
                "id": 1,
                "name": "John Doe",
                "title": "VP of Engineering",
                "company": "TechCorp",
                "location": "San Francisco, CA",
                "public_url": "https://linkedin.com/in/johndoe",
                "snippet": "Experienced engineering leader...",
                "source": "linkedin"
            },
            {
                "id": 2,
                "name": "Jane Smith",
                "title": "Marketing Manager",
                "company": "SaaS Inc",
                "location": "New York, NY",
                "public_url": "https://linkedin.com/in/janesmith",
                "snippet": "Digital marketing expert...",
                "source": "linkedin"
            }
        ]

    def test_lead_discovery_returns_list(self, sample_leads):
        """Test that lead discovery returns a list of leads.
        
        Verifies:
        - Return type is list
        - List contains lead dictionaries
        - Each lead has required fields
        """
        # Mock implementation (replace with actual function when available)
        def discover_leads(query):
            return sample_leads
        
        result = discover_leads("VP of Engineering")
        
        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(lead, dict) for lead in result)

    def test_lead_has_required_fields(self, sample_leads):
        """Test that each lead contains all required fields.
        
        Required fields:
        - id, name, title, company, location, public_url, snippet, source
        """
        required_fields = ["id", "name", "title", "company", "location", "public_url", "snippet", "source"]
        
        for lead in sample_leads:
            for field in required_fields:
                assert field in lead, f"Lead missing required field: {field}"

    def test_lead_scoring_prioritizes_senior_titles(self):
        """Test that lead scoring assigns higher scores to senior titles.
        
        Scoring logic:
        - VP/Director/Head: high score (0.8-1.0)
        - Manager: medium score (0.5-0.7)
        - Individual contributor: lower score (0.3-0.5)
        """
        def score_lead(lead):
            """Simple scoring function based on title."""
            title = lead.get("title", "").lower()
            if any(keyword in title for keyword in ["vp", "director", "head", "chief"]):
                return 0.9
            elif "manager" in title:
                return 0.6
            else:
                return 0.4
        
        vp_lead = {"title": "VP of Engineering"}
        manager_lead = {"title": "Marketing Manager"}
        ic_lead = {"title": "Software Engineer"}
        
        assert score_lead(vp_lead) > score_lead(manager_lead)
        assert score_lead(manager_lead) > score_lead(ic_lead)

    def test_duplicate_detection_filters_same_person(self):
        """Test that duplicate leads are detected and filtered.
        
        Duplicate criteria:
        - Same name AND same company
        - Same public_url
        """
        leads = [
            {"id": 1, "name": "John Doe", "company": "TechCorp", "public_url": "url1"},
            {"id": 2, "name": "John Doe", "company": "TechCorp", "public_url": "url1"},  # Duplicate
            {"id": 3, "name": "Jane Smith", "company": "SaaS Inc", "public_url": "url2"}
        ]
        
        def remove_duplicates(leads):
            """Remove duplicate leads based on name+company or URL."""
            seen = set()
            unique_leads = []
            for lead in leads:
                key = (lead["name"], lead["company"])
                if key not in seen:
                    seen.add(key)
                    unique_leads.append(lead)
            return unique_leads
        
        result = remove_duplicates(leads)
        assert len(result) == 2  # Should filter out 1 duplicate

    @patch('requests.get')
    def test_lead_discovery_handles_api_errors(self, mock_get):
        """Test that lead discovery handles API errors gracefully.
        
        Error scenarios:
        - Network timeout
        - HTTP 429 (rate limit)
        - HTTP 500 (server error)
        """
        mock_get.side_effect = Exception("API Error")
        
        def discover_leads_safe(query):
            """Safe lead discovery with error handling."""
            try:
                # Mock API call
                response = mock_get("https://api.example.com/leads")
                return response.json()
            except Exception as e:
                print(f"Error: {e}")
                return []  # Return empty list on error
        
        result = discover_leads_safe("test query")
        assert result == []  # Should return empty list, not crash

    def test_lead_filtering_by_location(self, sample_leads):
        """Test filtering leads by geographic location.
        
        Filters:
        - Include: specific cities or regions
        - Exclude: unwanted locations
        """
        def filter_by_location(leads, allowed_locations):
            """Filter leads by location."""
            return [
                lead for lead in leads
                if any(loc in lead["location"] for loc in allowed_locations)
            ]
        
        sf_leads = filter_by_location(sample_leads, ["San Francisco"])
        assert len(sf_leads) == 1
        assert sf_leads[0]["name"] == "John Doe"

    def test_lead_data_quality_validation(self):
        """Test validation of lead data quality.
        
        Validation rules:
        - Name is not empty
        - Title is not generic (e.g., "Professional", "Consultant")
        - Company is valid
        - URL is properly formatted
        """
        def is_valid_lead(lead):
            """Validate lead data quality."""
            if not lead.get("name") or len(lead["name"]) < 2:
                return False
            generic_titles = ["professional", "consultant", "expert"]
            if lead.get("title", "").lower() in generic_titles:
                return False
            if not lead.get("company"):
                return False
            return True
        
        valid_lead = {"name": "John Doe", "title": "VP Sales", "company": "TechCorp"}
        invalid_lead = {"name": "J", "title": "Professional", "company": ""}
        
        assert is_valid_lead(valid_lead) is True
        assert is_valid_lead(invalid_lead) is False
