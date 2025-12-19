#!/usr/bin/env python3
"""
Analytics Agent Test Script
===========================
Test the Analytics Agent's capabilities for ecommerce data analysis.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from projects.ecommerce_analytics.agents.analytics_agent import create_analytics_agent

# Create outputs directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_output(filename: str, content: str):
    """Save output to file."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"💾 Saved to: {filepath}")
    return filepath


def test_sales_analysis():
    """Test sales data analysis."""
    print("=" * 80)
    print("TEST 1: Sales Analysis")
    print("=" * 80)
    
    agent = create_analytics_agent(model=os.getenv("ANALYTICS_MODEL", "gpt-4o-mini"))
    
    sales_data = {
        "January": {"revenue": 50000, "orders": 120},
        "February": {"revenue": 55000, "orders": 135},
        "March": {"revenue": 62000, "orders": 150},
        "April": {"revenue": 58000, "orders": 140}
    }
    
    result = agent.run(
        task="analyze_sales",
        data=sales_data,
        metrics=["revenue_trend", "order_growth", "average_order_value"]
    )
    
    print("\n📊 Sales Analysis:\n")
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_output(f"sales_analysis_{timestamp}.md", result)
    
    print("\n" + "=" * 80 + "\n")
    
    return result


def test_customer_segmentation():
    """Test customer segmentation analysis."""
    print("=" * 80)
    print("TEST 2: Customer Segmentation")
    print("=" * 80)
    
    agent = create_analytics_agent(model=os.getenv("ANALYTICS_MODEL", "gpt-4o-mini"))
    
    customer_data = {
        "high_value": {"count": 50, "avg_spend": 5000},
        "medium_value": {"count": 200, "avg_spend": 1500},
        "low_value": {"count": 500, "avg_spend": 300}
    }
    
    result = agent.run(
        task="customer_segmentation",
        data=customer_data,
        include_recommendations=True
    )
    
    print("\n👥 Customer Segmentation:\n")
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_output(f"customer_segmentation_{timestamp}.md", result)
    
    print("\n" + "=" * 80 + "\n")
    
    return result


def test_product_performance():
    """Test product performance analysis."""
    print("=" * 80)
    print("TEST 3: Product Performance")
    print("=" * 80)
    
    agent = create_analytics_agent(model=os.getenv("ANALYTICS_MODEL", "gpt-4o-mini"))
    
    product_data = {
        "Product A": {"sales": 1500, "revenue": 75000, "returns": 50},
        "Product B": {"sales": 2000, "revenue": 60000, "returns": 100},
        "Product C": {"sales": 800, "revenue": 40000, "returns": 20}
    }
    
    result = agent.run(
        task="product_performance",
        data=product_data,
        metrics=["revenue", "return_rate", "profit_margin"]
    )
    
    print("\n📦 Product Performance:\n")
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_output(f"product_performance_{timestamp}.md", result)
    
    print("\n" + "=" * 80 + "\n")
    
    return result


def test_comprehensive_report():
    """Test comprehensive analytics report."""
    print("=" * 80)
    print("TEST 4: Comprehensive Analytics Report")
    print("=" * 80)
    
    agent = create_analytics_agent(model=os.getenv("ANALYTICS_MODEL", "gpt-4o-mini"))
    
    result = agent.run(
        task="comprehensive_report",
        period="Q1 2024",
        include_visualizations=True,
        include_recommendations=True
    )
    
    print("\n📈 Comprehensive Report:\n")
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_output(f"comprehensive_report_{timestamp}.md", result)
    
    print("\n" + "=" * 80 + "\n")
    
    return result


def main():
    """Run all tests."""
    print("\n🚀 Starting Analytics Agent Tests\n")
    print(f"📁 Outputs will be saved to: {OUTPUT_DIR}\n")
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OPENAI_API_KEY not found in .env file!")
        print("Please set your OpenAI API key in .env file.")
        sys.exit(1)
    
    print(f"✅ Using model: {os.getenv('ANALYTICS_MODEL', 'gpt-4o-mini')}\n")
    
    try:
        # Run tests
        test_sales_analysis()
        input("Press Enter to continue to next test...")
        
        test_customer_segmentation()
        input("Press Enter to continue to next test...")
        
        test_product_performance()
        input("Press Enter to continue to next test...")
        
        test_comprehensive_report()
        
        print("\n" + "=" * 80)
        print("✅ All tests completed successfully!")
        print(f"📁 All outputs saved to: {OUTPUT_DIR}")
        print("=" * 80)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
