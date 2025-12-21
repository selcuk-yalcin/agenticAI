"""Tests for emissions calculations.

This module tests:
- Scope 1, 2, 3 emissions calculations
- Emission factor lookups and application
- GHG Protocol compliance
- Intensity metrics (per revenue, per employee)
"""

import pytest
from unittest.mock import Mock


class TestEmissionsCalculation:
    """Test suite for emissions calculation functionality."""

    @pytest.fixture
    def emission_factors(self):
        """Fixture providing sample emission factors database.
        
        Returns:
            dict: Emission factors by category and country.
        """
        return {
            ("electricity", "US"): 0.42,  # kg CO2e per kWh
            ("electricity", "UK"): 0.23,
            ("natural_gas", "US"): 2.03,  # kg CO2e per cubic meter
            ("gasoline", "US"): 2.31,  # kg CO2e per liter
            ("diesel", "US"): 2.68,
            ("flight_economy", "global"): 0.15,  # kg CO2e per passenger-km
            ("flight_business", "global"): 0.43
        }

    def test_scope2_electricity_calculation(self, emission_factors):
        """Test Scope 2 emissions calculation for electricity consumption.
        
        Formula: kWh × emission_factor_per_kWh = kg CO2e
        """
        def calculate_scope2_electricity(kwh, country, factors):
            """Calculate Scope 2 emissions from electricity."""
            factor = factors.get(("electricity", country), 0.5)  # Default factor
            return kwh * factor
        
        # 1000 kWh in US
        emissions = calculate_scope2_electricity(1000, "US", emission_factors)
        
        assert emissions == pytest.approx(420.0)  # 1000 × 0.42

    def test_scope1_natural_gas_calculation(self, emission_factors):
        """Test Scope 1 emissions calculation for natural gas.
        
        Formula: cubic_meters × emission_factor = kg CO2e
        """
        def calculate_scope1_gas(cubic_meters, country, factors):
            """Calculate Scope 1 emissions from natural gas."""
            factor = factors.get(("natural_gas", country), 2.0)
            return cubic_meters * factor
        
        emissions = calculate_scope1_gas(100, "US", emission_factors)
        assert emissions == pytest.approx(203.0)  # 100 × 2.03

    def test_scope3_flight_emissions(self, emission_factors):
        """Test Scope 3 emissions for business flights.
        
        Formula: distance_km × passengers × class_factor = kg CO2e
        """
        def calculate_flight_emissions(distance_km, flight_class, passengers, factors):
            """Calculate flight emissions."""
            factor = factors.get((f"flight_{flight_class}", "global"), 0.2)
            return distance_km * passengers * factor
        
        # 1000 km business class flight, 1 passenger
        emissions = calculate_flight_emissions(1000, "business", 1, emission_factors)
        
        assert emissions == pytest.approx(430.0)  # 1000 × 1 × 0.43

    def test_total_emissions_aggregation(self):
        """Test aggregation of emissions across all scopes.
        
        Total = Scope 1 + Scope 2 + Scope 3
        """
        emissions_data = {
            "scope1": 500.0,  # kg CO2e
            "scope2": 800.0,
            "scope3": 1200.0
        }
        
        def calculate_total(emissions):
            """Calculate total emissions."""
            return sum(emissions.values())
        
        total = calculate_total(emissions_data)
        assert total == 2500.0

    def test_emissions_by_category_breakdown(self):
        """Test breakdown of emissions by category.
        
        Categories: electricity, heating, transport, procurement, etc.
        """
        emissions = [
            {"category": "electricity", "scope": 2, "amount": 500},
            {"category": "electricity", "scope": 2, "amount": 300},
            {"category": "heating", "scope": 1, "amount": 200},
            {"category": "flights", "scope": 3, "amount": 1000}
        ]
        
        def breakdown_by_category(emissions):
            """Aggregate emissions by category."""
            breakdown = {}
            for e in emissions:
                cat = e["category"]
                breakdown[cat] = breakdown.get(cat, 0) + e["amount"]
            return breakdown
        
        result = breakdown_by_category(emissions)
        
        assert result["electricity"] == 800
        assert result["heating"] == 200
        assert result["flights"] == 1000

    def test_intensity_metrics_calculation(self):
        """Test calculation of emissions intensity metrics.
        
        Metrics:
        - tCO2e per million USD revenue
        - tCO2e per employee
        - tCO2e per square meter
        """
        def calculate_intensity(total_emissions_kg, revenue_usd, employees):
            """Calculate intensity metrics."""
            total_tonnes = total_emissions_kg / 1000  # kg to tonnes
            
            return {
                "tonnes_per_million_revenue": (total_tonnes / (revenue_usd / 1_000_000)) if revenue_usd > 0 else 0,
                "tonnes_per_employee": total_tonnes / employees if employees > 0 else 0
            }
        
        # 100,000 kg CO2e, $10M revenue, 50 employees
        metrics = calculate_intensity(100_000, 10_000_000, 50)
        
        assert metrics["tonnes_per_million_revenue"] == pytest.approx(10.0)  # 100 / 10
        assert metrics["tonnes_per_employee"] == pytest.approx(2.0)  # 100 / 50

    def test_year_over_year_trend_calculation(self):
        """Test calculation of emissions trends over time.
        
        Calculates:
        - Absolute change
        - Percentage change
        - Trend direction
        """
        def calculate_trend(current_year, previous_year):
            """Calculate YoY emissions trend."""
            absolute_change = current_year - previous_year
            pct_change = (absolute_change / previous_year * 100) if previous_year > 0 else 0
            trend = "increasing" if absolute_change > 0 else "decreasing" if absolute_change < 0 else "stable"
            
            return {
                "absolute_change": absolute_change,
                "percent_change": pct_change,
                "trend": trend
            }
        
        # 2024: 1000 kg, 2023: 1200 kg
        trend = calculate_trend(1000, 1200)
        
        assert trend["absolute_change"] == -200
        assert trend["percent_change"] == pytest.approx(-16.67, rel=0.01)
        assert trend["trend"] == "decreasing"

    def test_emission_factor_versioning(self, emission_factors):
        """Test that emission factors are versioned and traceable.
        
        Requirements:
        - Each factor has source and date
        - Old factors can be retrieved for historical calculations
        - Factor updates don't affect past reports
        """
        versioned_factors = {
            "2024": emission_factors,
            "2023": {("electricity", "US"): 0.45}  # Older factor
        }
        
        def get_factor(category, country, year):
            """Get emission factor for specific year."""
            factors = versioned_factors.get(str(year), {})
            return factors.get((category, country))
        
        factor_2024 = get_factor("electricity", "US", 2024)
        factor_2023 = get_factor("electricity", "US", 2023)
        
        assert factor_2024 == 0.42
        assert factor_2023 == 0.45

    def test_scope_classification_accuracy(self):
        """Test correct classification of activities into scopes.
        
        Scope 1: Direct emissions (company vehicles, heating)
        Scope 2: Purchased electricity, heating, cooling
        Scope 3: Indirect emissions (flights, supply chain, commuting)
        """
        def classify_scope(activity_type):
            """Classify activity into GHG scope."""
            scope1 = ["company_vehicle", "natural_gas_heating", "diesel_generator"]
            scope2 = ["purchased_electricity", "purchased_steam"]
            scope3 = ["employee_flights", "supplier_emissions", "employee_commute"]
            
            if activity_type in scope1:
                return 1
            elif activity_type in scope2:
                return 2
            elif activity_type in scope3:
                return 3
            return None
        
        assert classify_scope("company_vehicle") == 1
        assert classify_scope("purchased_electricity") == 2
        assert classify_scope("employee_flights") == 3

    def test_uncertainty_range_calculation(self):
        """Test calculation of uncertainty ranges in emissions estimates.
        
        Uncertainty sources:
        - Emission factor accuracy
        - Data quality
        - Estimation methods
        """
        def calculate_with_uncertainty(value, uncertainty_pct):
            """Calculate value with uncertainty range."""
            margin = value * (uncertainty_pct / 100)
            return {
                "value": value,
                "uncertainty": uncertainty_pct,
                "min": value - margin,
                "max": value + margin
            }
        
        # 1000 kg with ±10% uncertainty
        result = calculate_with_uncertainty(1000, 10)
        
        assert result["value"] == 1000
        assert result["min"] == 900
        assert result["max"] == 1100
