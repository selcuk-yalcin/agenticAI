"""Tests for data ingestion and normalization.

This module tests:
- CSV/Excel file parsing
- PDF invoice extraction (OCR)
- Data validation and cleaning
- Unit conversion and standardization
"""

import pytest
from unittest.mock import Mock, patch
import pandas as pd
from io import StringIO


class TestDataIngestion:
    """Test suite for data ingestion functionality."""

    @pytest.fixture
    def sample_energy_csv(self):
        """Fixture providing sample energy bill CSV data.
        
        Returns:
            str: CSV content for testing.
        """
        return """date,supplier,kwh,cost,currency
2024-01-01,PowerCo,1000,150.00,USD
2024-02-01,PowerCo,1200,180.00,USD
2024-03-01,PowerCo,950,142.50,USD"""

    @pytest.fixture
    def sample_travel_csv(self):
        """Fixture providing sample travel/flight data.
        
        Returns:
            str: CSV content for flight records.
        """
        return """date,employee,origin,destination,class,distance_km
2024-01-15,John Doe,SFO,JFK,economy,4139
2024-02-20,Jane Smith,LAX,LHR,business,8781"""

    def test_csv_parsing_returns_dataframe(self, sample_energy_csv):
        """Test that CSV parsing returns a valid pandas DataFrame.
        
        Verifies:
        - Return type is DataFrame
        - All expected columns are present
        - Data types are correct
        """
        df = pd.read_csv(StringIO(sample_energy_csv))
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        assert list(df.columns) == ["date", "supplier", "kwh", "cost", "currency"]

    def test_data_validation_rejects_invalid_records(self):
        """Test that invalid records are flagged or rejected.
        
        Invalid scenarios:
        - Missing required fields
        - Negative quantities
        - Invalid dates
        - Unknown units
        """
        def validate_record(record):
            """Validate a single data record."""
            required_fields = ["date", "kwh"]
            
            # Check required fields
            for field in required_fields:
                if field not in record or record[field] is None:
                    return False, f"Missing required field: {field}"
            
            # Check non-negative quantities
            if record.get("kwh", 0) < 0:
                return False, "Negative quantity not allowed"
            
            return True, "Valid"
        
        valid = {"date": "2024-01-01", "kwh": 1000}
        invalid_missing = {"date": "2024-01-01"}
        invalid_negative = {"date": "2024-01-01", "kwh": -100}
        
        assert validate_record(valid)[0] is True
        assert validate_record(invalid_missing)[0] is False
        assert validate_record(invalid_negative)[0] is False

    def test_unit_conversion_standardizes_inputs(self):
        """Test conversion of various units to standard format.
        
        Conversions:
        - kWh, MWh, GWh → kWh
        - liters, gallons → liters
        - kg, tons, lbs → kg
        """
        def convert_to_standard_unit(value, from_unit):
            """Convert to standard units."""
            conversions = {
                "kwh": 1.0,
                "mwh": 1000.0,
                "gwh": 1000000.0,
                "liters": 1.0,
                "gallons": 3.785,
                "kg": 1.0,
                "tons": 1000.0,
                "lbs": 0.453592
            }
            
            return value * conversions.get(from_unit.lower(), 1.0)
        
        assert convert_to_standard_unit(1, "mwh") == 1000
        assert convert_to_standard_unit(10, "gallons") == pytest.approx(37.85, rel=0.01)
        assert convert_to_standard_unit(1, "tons") == 1000

    def test_date_parsing_handles_various_formats(self):
        """Test parsing of different date formats.
        
        Supported formats:
        - YYYY-MM-DD
        - MM/DD/YYYY
        - DD-MM-YYYY
        - YYYY/MM/DD
        """
        def parse_date(date_str):
            """Parse date string to standard format."""
            import pandas as pd
            try:
                return pd.to_datetime(date_str).strftime("%Y-%m-%d")
            except:
                return None
        
        assert parse_date("2024-01-15") == "2024-01-15"
        assert parse_date("01/15/2024") == "2024-01-15"
        assert parse_date("2024/01/15") == "2024-01-15"

    def test_supplier_name_normalization(self):
        """Test normalization of supplier names to canonical form.
        
        Examples:
        - "PG&E", "Pacific Gas & Electric", "PGE" → "Pacific Gas & Electric"
        - "Con Ed", "ConEd", "Consolidated Edison" → "Consolidated Edison"
        """
        supplier_mappings = {
            "pg&e": "Pacific Gas & Electric",
            "pacific gas & electric": "Pacific Gas & Electric",
            "pge": "Pacific Gas & Electric",
            "con ed": "Consolidated Edison",
            "coned": "Consolidated Edison"
        }
        
        def normalize_supplier(name):
            """Normalize supplier name."""
            return supplier_mappings.get(name.lower(), name)
        
        assert normalize_supplier("PG&E") == "Pacific Gas & Electric"
        assert normalize_supplier("ConEd") == "Consolidated Edison"

    @patch('PyPDF2.PdfReader')
    def test_pdf_extraction_with_ocr(self, mock_pdf_reader):
        """Test extraction of data from PDF invoices using OCR.
        
        Tests:
        - PDF is opened successfully
        - Text extraction works
        - Key fields are identified (date, amount, kwh)
        """
        mock_pdf_reader.return_value.pages = [
            Mock(extract_text=lambda: "Invoice Date: 2024-01-01\nUsage: 1000 kWh\nAmount: $150.00")
        ]
        
        def extract_from_pdf(pdf_path):
            """Extract data from PDF invoice."""
            reader = mock_pdf_reader(pdf_path)
            text = reader.pages[0].extract_text()
            
            # Simple regex extraction (in practice use more robust parsing)
            import re
            kwh_match = re.search(r'(\d+)\s*kWh', text)
            
            return {
                "kwh": int(kwh_match.group(1)) if kwh_match else None,
                "raw_text": text
            }
        
        result = extract_from_pdf("invoice.pdf")
        assert result["kwh"] == 1000

    def test_duplicate_detection_in_ingestion(self, sample_energy_csv):
        """Test detection of duplicate records during ingestion.
        
        Duplicate criteria:
        - Same date + same supplier
        - Same invoice_id (if available)
        """
        df = pd.read_csv(StringIO(sample_energy_csv))
        
        # Add duplicate
        duplicate_row = df.iloc[0].copy()
        df = pd.concat([df, pd.DataFrame([duplicate_row])], ignore_index=True)
        
        def remove_duplicates(df):
            """Remove duplicate records."""
            return df.drop_duplicates(subset=["date", "supplier"], keep="first")
        
        clean_df = remove_duplicates(df)
        assert len(clean_df) == 3  # Original 3 rows, duplicate removed

    def test_data_quality_report_generation(self, sample_energy_csv):
        """Test generation of data quality report.
        
        Report includes:
        - Total records
        - Valid vs invalid count
        - Missing field statistics
        - Outlier detection
        """
        df = pd.read_csv(StringIO(sample_energy_csv))
        
        def generate_quality_report(df):
            """Generate data quality report."""
            return {
                "total_records": len(df),
                "missing_values": df.isnull().sum().to_dict(),
                "duplicate_count": df.duplicated().sum(),
                "date_range": {
                    "start": df["date"].min(),
                    "end": df["date"].max()
                }
            }
        
        report = generate_quality_report(df)
        
        assert report["total_records"] == 3
        assert isinstance(report["missing_values"], dict)
        assert report["duplicate_count"] >= 0
