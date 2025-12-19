#!/usr/bin/env python3
"""
Advanced Data Visualization Tests
==================================
Comprehensive testing of Chart Agent capabilities.
"""

import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from projects.data_visualization.agents.chart_agent import create_chart_agent

# Create outputs directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "advanced_tests")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_result(filename: str, content: str):
    """Save test result to file."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"💾 Saved to: {filepath}")
    return filepath


def test_sales_data_analysis():
    """Test 1: Sales data analysis with multiple charts."""
    print("\n" + "=" * 80)
    print("TEST 1: Sales Data Analysis")
    print("=" * 80)
    
    agent = create_chart_agent(model=os.getenv("CHART_MODEL", "gpt-4o-mini"))
    
    # Sample sales data
    sales_data = {
        "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "revenue": [45000, 52000, 48000, 61000, 58000, 67000],
        "costs": [30000, 33000, 31000, 38000, 36000, 41000],
        "customers": [120, 145, 138, 167, 162, 189]
    }
    
    print("\n📊 Analyzing sales data...")
    print(f"   Months: {len(sales_data['month'])}")
    print(f"   Metrics: revenue, costs, customers")
    
    result = agent.create_dashboard(
        data=json.dumps(sales_data),
        title="Q1-Q2 Sales Dashboard",
        description="Sales performance for the first half of the year"
    )
    
    print(f"\n📈 Analysis Result (first 300 chars):\n{result[:300]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"sales_analysis_{timestamp}.txt", result)
    
    print("\n" + "=" * 80)
    return result


def test_customer_segmentation():
    """Test 2: Customer segmentation analysis."""
    print("\n" + "=" * 80)
    print("TEST 2: Customer Segmentation Analysis")
    print("=" * 80)
    
    agent = create_chart_agent(model=os.getenv("CHART_MODEL", "gpt-4o-mini"))
    
    # Customer data
    customer_data = {
        "customer_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "age": [25, 34, 45, 23, 56, 38, 42, 29, 51, 33],
        "total_purchases": [1200, 3400, 2100, 800, 4500, 2800, 3100, 1500, 3800, 2200],
        "frequency": [5, 12, 8, 3, 18, 10, 11, 6, 15, 9],
        "category": ["Bronze", "Gold", "Silver", "Bronze", "Platinum", "Gold", "Gold", "Silver", "Platinum", "Silver"]
    }
    
    print("\n👥 Analyzing customer segments...")
    print(f"   Customers: {len(customer_data['customer_id'])}")
    print(f"   Segments: Bronze, Silver, Gold, Platinum")
    
    result = agent.analyze_and_visualize(
        data=json.dumps(customer_data),
        focus="customer segmentation and purchasing patterns"
    )
    
    print(f"\n📊 Segmentation Result (first 300 chars):\n{result[:300]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"customer_segmentation_{timestamp}.txt", result)
    
    print("\n" + "=" * 80)
    return result


def test_correlation_analysis():
    """Test 3: Correlation and relationship analysis."""
    print("\n" + "=" * 80)
    print("TEST 3: Correlation Analysis")
    print("=" * 80)
    
    agent = create_chart_agent(model=os.getenv("CHART_MODEL", "gpt-4o-mini"))
    
    # Multi-variable data
    correlation_data = {
        "marketing_spend": [5000, 7000, 6000, 8000, 9000, 7500, 10000, 8500],
        "sales": [45000, 58000, 52000, 63000, 71000, 61000, 78000, 68000],
        "website_visits": [2000, 2800, 2400, 3100, 3500, 2900, 3800, 3300],
        "conversion_rate": [2.5, 3.1, 2.8, 3.4, 3.8, 3.2, 4.1, 3.6]
    }
    
    print("\n🔗 Analyzing correlations...")
    print(f"   Variables: marketing_spend, sales, website_visits, conversion_rate")
    
    result = agent.run(
        query="Analyze the correlations between these marketing metrics and create visualizations showing relationships. Include a correlation heatmap and scatter plots for key relationships.",
        data=json.dumps(correlation_data)
    )
    
    print(f"\n📈 Correlation Result (first 300 chars):\n{result[:300]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"correlation_analysis_{timestamp}.txt", result)
    
    print("\n" + "=" * 80)
    return result


def test_time_series_trends():
    """Test 4: Time series trend analysis."""
    print("\n" + "=" * 80)
    print("TEST 4: Time Series Trend Analysis")
    print("=" * 80)
    
    agent = create_chart_agent(model=os.getenv("CHART_MODEL", "gpt-4o-mini"))
    
    # Time series data
    time_series_data = {
        "date": ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", "2025-01-05", 
                 "2025-01-06", "2025-01-07", "2025-01-08", "2025-01-09", "2025-01-10"],
        "stock_price": [150.5, 152.3, 151.8, 154.2, 156.1, 155.7, 158.3, 157.9, 160.2, 159.8],
        "volume": [1000000, 1200000, 950000, 1350000, 1450000, 1300000, 1600000, 1500000, 1700000, 1550000],
        "sentiment_score": [0.6, 0.65, 0.55, 0.7, 0.75, 0.72, 0.8, 0.78, 0.85, 0.82]
    }
    
    print("\n📈 Analyzing time series trends...")
    print(f"   Data points: {len(time_series_data['date'])}")
    print(f"   Metrics: stock_price, volume, sentiment_score")
    
    result = agent.run(
        query="Analyze these time series trends and create line charts showing how stock price, volume, and sentiment evolved over time. Identify any patterns or correlations.",
        data=json.dumps(time_series_data)
    )
    
    print(f"\n📊 Trend Result (first 300 chars):\n{result[:300]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"time_series_trends_{timestamp}.txt", result)
    
    print("\n" + "=" * 80)
    return result


def test_distribution_analysis():
    """Test 5: Distribution and statistical analysis."""
    print("\n" + "=" * 80)
    print("TEST 5: Distribution Analysis")
    print("=" * 80)
    
    agent = create_chart_agent(model=os.getenv("CHART_MODEL", "gpt-4o-mini"))
    
    # Distribution data
    distribution_data = {
        "employee_id": list(range(1, 51)),
        "salary": [45000, 52000, 48000, 61000, 58000, 67000, 55000, 49000, 71000, 63000,
                   46000, 53000, 59000, 65000, 72000, 56000, 50000, 68000, 74000, 62000,
                   47000, 54000, 60000, 66000, 73000, 57000, 51000, 69000, 75000, 64000,
                   48000, 55000, 61000, 67000, 74000, 58000, 52000, 70000, 76000, 65000,
                   49000, 56000, 62000, 68000, 75000, 59000, 53000, 71000, 77000, 66000],
        "years_experience": [1, 3, 2, 5, 4, 7, 3, 2, 8, 6,
                            1, 3, 4, 6, 9, 3, 2, 7, 10, 5,
                            1, 3, 5, 6, 9, 4, 2, 7, 11, 6,
                            2, 3, 5, 7, 10, 4, 3, 8, 12, 6,
                            2, 4, 5, 7, 11, 4, 3, 8, 13, 7],
        "department": ["Sales", "IT", "Sales", "IT", "Sales", "IT", "HR", "Sales", "IT", "Sales",
                      "IT", "HR", "Sales", "IT", "Sales", "IT", "HR", "Sales", "IT", "Sales",
                      "IT", "HR", "Sales", "IT", "Sales", "IT", "HR", "Sales", "IT", "Sales",
                      "IT", "HR", "Sales", "IT", "Sales", "IT", "HR", "Sales", "IT", "Sales",
                      "IT", "HR", "Sales", "IT", "Sales", "IT", "HR", "Sales", "IT", "Sales"]
    }
    
    print("\n📊 Analyzing salary distribution...")
    print(f"   Employees: {len(distribution_data['employee_id'])}")
    print(f"   Departments: Sales, IT, HR")
    
    result = agent.run(
        query="Analyze the salary distribution across departments. Create visualizations showing: 1) Overall salary distribution, 2) Salary by department comparison, 3) Relationship between experience and salary. Provide statistical insights.",
        data=json.dumps(distribution_data)
    )
    
    print(f"\n📈 Distribution Result (first 300 chars):\n{result[:300]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"distribution_analysis_{timestamp}.txt", result)
    
    print("\n" + "=" * 80)
    return result


def test_comparison_analysis():
    """Test 6: Comparative analysis between datasets."""
    print("\n" + "=" * 80)
    print("TEST 6: Comparative Analysis")
    print("=" * 80)
    
    agent = create_chart_agent(model=os.getenv("CHART_MODEL", "gpt-4o-mini"))
    
    # Q1 data
    q1_data = {
        "product": ["Product A", "Product B", "Product C", "Product D"],
        "sales": [25000, 18000, 32000, 21000],
        "returns": [1200, 900, 1500, 1100]
    }
    
    # Q2 data
    q2_data = {
        "product": ["Product A", "Product B", "Product C", "Product D"],
        "sales": [28000, 22000, 35000, 24000],
        "returns": [1000, 1100, 1300, 950]
    }
    
    print("\n⚖️  Comparing Q1 vs Q2 performance...")
    print(f"   Products: {len(q1_data['product'])}")
    
    result = agent.compare_datasets(
        dataset1=json.dumps(q1_data),
        dataset2=json.dumps(q2_data),
        label1="Q1 2025",
        label2="Q2 2025"
    )
    
    print(f"\n📊 Comparison Result (first 300 chars):\n{result[:300]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"comparison_analysis_{timestamp}.txt", result)
    
    print("\n" + "=" * 80)
    return result


def test_pie_chart_proportions():
    """Test 7: Pie chart for proportions and percentages."""
    print("\n" + "=" * 80)
    print("TEST 7: Proportion Analysis (Pie Charts)")
    print("=" * 80)
    
    agent = create_chart_agent(model=os.getenv("CHART_MODEL", "gpt-4o-mini"))
    
    # Market share data
    market_data = {
        "company": ["Company A", "Company B", "Company C", "Company D", "Others"],
        "market_share": [35.2, 28.7, 18.5, 12.3, 5.3],
        "revenue_millions": [352, 287, 185, 123, 53]
    }
    
    print("\n🥧 Analyzing market share proportions...")
    print(f"   Companies: {len(market_data['company'])}")
    
    result = agent.run(
        query="Create pie charts showing market share distribution and revenue proportions. Include percentage labels and provide insights about market concentration.",
        data=json.dumps(market_data)
    )
    
    print(f"\n📊 Proportion Result (first 300 chars):\n{result[:300]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"pie_chart_analysis_{timestamp}.txt", result)
    
    print("\n" + "=" * 80)
    return result


def test_multi_metric_dashboard():
    """Test 8: Complex dashboard with multiple metrics."""
    print("\n" + "=" * 80)
    print("TEST 8: Multi-Metric Dashboard")
    print("=" * 80)
    
    agent = create_chart_agent(model=os.getenv("CHART_MODEL", "gpt-4o-mini"))
    
    # Complex business data
    business_data = {
        "week": ["Week 1", "Week 2", "Week 3", "Week 4"],
        "website_visitors": [15000, 18000, 16500, 21000],
        "signups": [450, 540, 495, 630],
        "conversions": [45, 59, 52, 71],
        "revenue": [22500, 29500, 26000, 35500],
        "avg_order_value": [500, 500, 500, 500],
        "customer_satisfaction": [4.2, 4.3, 4.1, 4.5]
    }
    
    print("\n📊 Creating comprehensive business dashboard...")
    print(f"   Time period: {len(business_data['week'])} weeks")
    print(f"   Metrics: 6 key performance indicators")
    
    result = agent.create_dashboard(
        data=json.dumps(business_data),
        title="Weekly Business Performance Dashboard",
        description="Key metrics tracking for 4-week period"
    )
    
    print(f"\n📈 Dashboard Result (first 300 chars):\n{result[:300]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"multi_metric_dashboard_{timestamp}.txt", result)
    
    print("\n" + "=" * 80)
    return result


def main():
    """Run all advanced visualization tests."""
    print("\n" + "=" * 80)
    print("🚀 ADVANCED DATA VISUALIZATION TESTS")
    print("=" * 80)
    print(f"\n📁 Outputs: {OUTPUT_DIR}")
    print(f"🤖 Model: {os.getenv('CHART_MODEL', 'gpt-4o-mini')}\n")
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OPENAI_API_KEY not found!")
        sys.exit(1)
    
    try:
        # Run all tests
        print("\n▶️  Starting Test Suite...\n")
        
        test_sales_data_analysis()
        input("\nPress Enter to continue...")
        
        test_customer_segmentation()
        input("\nPress Enter to continue...")
        
        test_correlation_analysis()
        input("\nPress Enter to continue...")
        
        test_time_series_trends()
        input("\nPress Enter to continue...")
        
        test_distribution_analysis()
        input("\nPress Enter to continue...")
        
        test_comparison_analysis()
        input("\nPress Enter to continue...")
        
        test_pie_chart_proportions()
        input("\nPress Enter to continue...")
        
        test_multi_metric_dashboard()
        
        print("\n" + "=" * 80)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print(f"📁 All results saved to: {OUTPUT_DIR}")
        print("=" * 80 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
