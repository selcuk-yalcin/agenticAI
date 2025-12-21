"""Tests for E-commerce Analytics Agent.

This module tests:
- Sales KPI calculations (revenue, AOV, conversion rate)
- Customer segmentation and analytics
- Product performance metrics
- Trend analysis and forecasting
"""

import pytest
from unittest.mock import Mock, patch


class TestEcommerceAnalytics:
    """Test suite for e-commerce analytics functionality."""

    @pytest.fixture
    def sample_sales_data(self):
        """Fixture providing sample sales transaction data.
        
        Returns:
            list: Sales transactions with order details.
        """
        return [
            {"order_id": "ORD001", "customer_id": "C001", "amount": 150.00, "items": 3, "date": "2024-01-01"},
            {"order_id": "ORD002", "customer_id": "C002", "amount": 89.99, "items": 2, "date": "2024-01-01"},
            {"order_id": "ORD003", "customer_id": "C001", "amount": 200.00, "items": 5, "date": "2024-01-02"},
            {"order_id": "ORD004", "customer_id": "C003", "amount": 45.50, "items": 1, "date": "2024-01-02"},
            {"order_id": "ORD005", "customer_id": "C002", "amount": 120.00, "items": 2, "date": "2024-01-03"},
        ]

    @pytest.fixture
    def sample_product_data(self):
        """Fixture providing sample product catalog data.
        
        Returns:
            list: Products with sales and inventory info.
        """
        return [
            {"product_id": "P001", "name": "Laptop", "category": "Electronics", "price": 999.99, "units_sold": 50, "stock": 20},
            {"product_id": "P002", "name": "Mouse", "category": "Electronics", "price": 29.99, "units_sold": 200, "stock": 150},
            {"product_id": "P003", "name": "Desk Chair", "category": "Furniture", "price": 199.99, "units_sold": 30, "stock": 10},
            {"product_id": "P004", "name": "Monitor", "category": "Electronics", "price": 299.99, "units_sold": 75, "stock": 25},
        ]

    def test_calculate_total_revenue(self, sample_sales_data):
        """Test calculation of total revenue.
        
        Total revenue = sum of all order amounts.
        """
        def calculate_total_revenue(sales_data):
            """Calculate total revenue from sales."""
            return sum(order["amount"] for order in sales_data)
        
        revenue = calculate_total_revenue(sample_sales_data)
        
        assert revenue == 605.49
        assert isinstance(revenue, float)

    def test_calculate_average_order_value(self, sample_sales_data):
        """Test calculation of Average Order Value (AOV).
        
        AOV = Total Revenue / Number of Orders
        """
        def calculate_aov(sales_data):
            """Calculate average order value."""
            if not sales_data:
                return 0
            
            total_revenue = sum(order["amount"] for order in sales_data)
            num_orders = len(sales_data)
            
            return total_revenue / num_orders
        
        aov = calculate_aov(sample_sales_data)
        
        assert aov == 605.49 / 5
        assert aov > 0

    def test_calculate_conversion_rate(self):
        """Test calculation of conversion rate.
        
        Conversion Rate = (Orders / Visitors) * 100
        """
        def calculate_conversion_rate(num_orders, num_visitors):
            """Calculate conversion rate percentage."""
            if num_visitors == 0:
                return 0
            
            return (num_orders / num_visitors) * 100
        
        rate = calculate_conversion_rate(50, 1000)
        
        assert rate == 5.0
        assert 0 <= rate <= 100

    def test_customer_segmentation_rfm(self, sample_sales_data):
        """Test RFM (Recency, Frequency, Monetary) customer segmentation.
        
        RFM segments:
        - Champions: High F, high M, low R
        - At Risk: High F, high M, high R
        - New Customers: Low F, low/medium M, low R
        """
        def calculate_rfm_score(customer_id, sales_data, current_date="2024-01-04"):
            """Calculate RFM scores for a customer."""
            from datetime import datetime
            
            customer_orders = [o for o in sales_data if o["customer_id"] == customer_id]
            
            if not customer_orders:
                return None
            
            # Recency: days since last purchase (lower is better)
            last_order_date = max(datetime.strptime(o["date"], "%Y-%m-%d") for o in customer_orders)
            current = datetime.strptime(current_date, "%Y-%m-%d")
            recency = (current - last_order_date).days
            
            # Frequency: number of orders (higher is better)
            frequency = len(customer_orders)
            
            # Monetary: total spent (higher is better)
            monetary = sum(o["amount"] for o in customer_orders)
            
            return {
                "recency": recency,
                "frequency": frequency,
                "monetary": monetary
            }
        
        rfm_c001 = calculate_rfm_score("C001", sample_sales_data)
        rfm_c002 = calculate_rfm_score("C002", sample_sales_data)
        
        assert rfm_c001 is not None
        assert rfm_c001["frequency"] == 2  # C001 has 2 orders
        assert rfm_c001["monetary"] == 350.00  # 150 + 200

    def test_product_performance_ranking(self, sample_product_data):
        """Test ranking products by performance metrics.
        
        Metrics:
        - Total revenue
        - Units sold
        - Revenue per unit
        """
        def rank_products_by_revenue(products):
            """Rank products by total revenue."""
            for product in products:
                product["total_revenue"] = product["price"] * product["units_sold"]
            
            # Sort by revenue descending
            ranked = sorted(products, key=lambda p: p["total_revenue"], reverse=True)
            
            return ranked
        
        ranked = rank_products_by_revenue(sample_product_data)
        
        assert len(ranked) == 4
        assert ranked[0]["product_id"] == "P001"  # Laptop: 999.99 * 50 = 49,999.50
        assert ranked[0]["total_revenue"] > ranked[1]["total_revenue"]

    def test_inventory_turnover_rate(self, sample_product_data):
        """Test calculation of inventory turnover rate.
        
        Turnover Rate = Units Sold / Average Inventory
        High turnover = fast-moving products
        """
        def calculate_inventory_turnover(product):
            """Calculate inventory turnover rate."""
            units_sold = product["units_sold"]
            current_stock = product["stock"]
            
            # Simplified: assume average inventory = (sold + current) / 2
            avg_inventory = (units_sold + current_stock) / 2
            
            if avg_inventory == 0:
                return 0
            
            turnover_rate = units_sold / avg_inventory
            
            return {
                "turnover_rate": turnover_rate,
                "velocity": "fast" if turnover_rate > 2 else "slow"
            }
        
        laptop_turnover = calculate_inventory_turnover(sample_product_data[0])
        mouse_turnover = calculate_inventory_turnover(sample_product_data[1])
        
        assert "turnover_rate" in laptop_turnover
        assert laptop_turnover["turnover_rate"] > 0

    def test_sales_trend_analysis(self):
        """Test analysis of sales trends over time.
        
        Trend analysis:
        - Growth rate (week-over-week, month-over-month)
        - Trend direction (increasing, decreasing, stable)
        - Seasonality detection
        """
        def analyze_sales_trend(daily_sales):
            """Analyze sales trend from daily data."""
            if len(daily_sales) < 2:
                return {"trend": "insufficient_data"}
            
            # Calculate simple growth rate
            first_half = sum(daily_sales[:len(daily_sales)//2])
            second_half = sum(daily_sales[len(daily_sales)//2:])
            
            if first_half == 0:
                growth_rate = 0
            else:
                growth_rate = ((second_half - first_half) / first_half) * 100
            
            # Determine trend direction
            if growth_rate > 5:
                trend = "increasing"
            elif growth_rate < -5:
                trend = "decreasing"
            else:
                trend = "stable"
            
            return {
                "trend": trend,
                "growth_rate": growth_rate,
                "first_half_total": first_half,
                "second_half_total": second_half
            }
        
        increasing_sales = [100, 110, 120, 130, 140, 150]
        decreasing_sales = [150, 140, 130, 120, 110, 100]
        
        inc_trend = analyze_sales_trend(increasing_sales)
        dec_trend = analyze_sales_trend(decreasing_sales)
        
        assert inc_trend["trend"] == "increasing"
        assert dec_trend["trend"] == "decreasing"

    def test_customer_lifetime_value(self, sample_sales_data):
        """Test calculation of Customer Lifetime Value (CLV).
        
        CLV = Average Order Value × Purchase Frequency × Customer Lifespan
        """
        def calculate_clv(customer_id, sales_data, avg_lifespan_months=12):
            """Calculate customer lifetime value."""
            customer_orders = [o for o in sales_data if o["customer_id"] == customer_id]
            
            if not customer_orders:
                return 0
            
            # Average order value for this customer
            total_spent = sum(o["amount"] for o in customer_orders)
            num_orders = len(customer_orders)
            avg_order_value = total_spent / num_orders
            
            # Purchase frequency (orders per month)
            # Simplified: assume data spans 1 month
            purchase_frequency = num_orders
            
            # CLV = AOV × Frequency × Lifespan
            clv = avg_order_value * purchase_frequency * avg_lifespan_months
            
            return {
                "clv": clv,
                "avg_order_value": avg_order_value,
                "purchase_frequency": purchase_frequency
            }
        
        clv_c001 = calculate_clv("C001", sample_sales_data)
        
        assert clv_c001["clv"] > 0
        assert clv_c001["avg_order_value"] == 175.00  # (150 + 200) / 2

    def test_cart_abandonment_rate(self):
        """Test calculation of cart abandonment rate.
        
        Abandonment Rate = (Carts Created - Orders) / Carts Created × 100
        """
        def calculate_abandonment_rate(carts_created, orders_completed):
            """Calculate cart abandonment rate."""
            if carts_created == 0:
                return 0
            
            abandoned = carts_created - orders_completed
            rate = (abandoned / carts_created) * 100
            
            return {
                "abandonment_rate": rate,
                "abandoned_carts": abandoned,
                "conversion_rate": (orders_completed / carts_created) * 100
            }
        
        result = calculate_abandonment_rate(carts_created=100, orders_completed=65)
        
        assert result["abandonment_rate"] == 35.0
        assert result["abandoned_carts"] == 35

    def test_product_category_analysis(self, sample_product_data):
        """Test analysis of product categories.
        
        Category metrics:
        - Total revenue per category
        - Best-selling category
        - Average price per category
        """
        def analyze_categories(products):
            """Analyze product categories."""
            categories = {}
            
            for product in products:
                cat = product["category"]
                if cat not in categories:
                    categories[cat] = {
                        "revenue": 0,
                        "units_sold": 0,
                        "products": []
                    }
                
                revenue = product["price"] * product["units_sold"]
                categories[cat]["revenue"] += revenue
                categories[cat]["units_sold"] += product["units_sold"]
                categories[cat]["products"].append(product["name"])
            
            # Find best-selling category
            best_category = max(categories.items(), key=lambda x: x[1]["revenue"])
            
            return {
                "categories": categories,
                "best_category": best_category[0],
                "best_category_revenue": best_category[1]["revenue"]
            }
        
        analysis = analyze_categories(sample_product_data)
        
        assert "Electronics" in analysis["categories"]
        assert analysis["best_category"] in ["Electronics", "Furniture"]

    @patch('openai.ChatCompletion.create')
    def test_sales_forecast_with_llm(self, mock_openai):
        """Test sales forecasting using LLM.
        
        Forecasting considers:
        - Historical trends
        - Seasonality
        - External factors
        """
        mock_openai.return_value = Mock(
            choices=[Mock(message=Mock(content="Based on trends, forecasted sales: $50,000"))]
        )
        
        def forecast_sales(historical_data, periods=7):
            """Forecast future sales using LLM."""
            data_summary = f"Historical sales: {historical_data}"
            
            response = mock_openai(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user",
                    "content": f"Forecast sales for next {periods} days based on: {data_summary}"
                }]
            )
            
            return response.choices[0].message.content
        
        forecast = forecast_sales([100, 120, 115, 130, 140])
        
        assert isinstance(forecast, str)
        assert len(forecast) > 0

    def test_cohort_analysis(self):
        """Test cohort analysis for customer retention.
        
        Cohort analysis tracks:
        - Customer groups by acquisition date
        - Retention rates over time
        - Revenue per cohort
        """
        def analyze_cohort(cohort_data):
            """Analyze customer cohort."""
            # cohort_data: {month: {customers: [...], revenue: ...}}
            
            cohorts = {}
            
            for month, data in cohort_data.items():
                cohorts[month] = {
                    "initial_customers": len(data["customers"]),
                    "revenue": data["revenue"],
                    "avg_revenue_per_customer": data["revenue"] / len(data["customers"]) if data["customers"] else 0
                }
            
            return cohorts
        
        cohort_data = {
            "2024-01": {"customers": ["C001", "C002", "C003"], "revenue": 1500},
            "2024-02": {"customers": ["C004", "C005"], "revenue": 800}
        }
        
        analysis = analyze_cohort(cohort_data)
        
        assert "2024-01" in analysis
        assert analysis["2024-01"]["initial_customers"] == 3
