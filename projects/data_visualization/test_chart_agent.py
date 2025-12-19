#!/usr/bin/env python3
"""
Chart Agent Test Script
=======================
Test the Chart Agent's capabilities for data visualization.
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

from projects.data_visualization.agents.chart_agent import create_chart_agent

# Create outputs directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def test_bar_chart():
    """Test bar chart generation."""
    print("=" * 80)
    print("TEST 1: Bar Chart Generation")
    print("=" * 80)
    
    agent = create_chart_agent(model=os.getenv("CHART_MODEL", "gpt-4o-mini"))
    
    data = {
        "categories": ["Jan", "Feb", "Mar", "Apr", "May"],
        "values": [120, 150, 180, 140, 200]
    }
    
    result = agent.run(
        chart_type="bar",
        data=data,
        title="Monthly Sales",
        xlabel="Month",
        ylabel="Sales ($)",
        output_dir=OUTPUT_DIR
    )
    
    print(f"\n📊 Bar Chart Created: {result}\n")
    print("=" * 80 + "\n")
    
    return result


def test_line_chart():
    """Test line chart generation."""
    print("=" * 80)
    print("TEST 2: Line Chart Generation")
    print("=" * 80)
    
    agent = create_chart_agent(model=os.getenv("CHART_MODEL", "gpt-4o-mini"))
    
    data = {
        "x": list(range(1, 13)),
        "y": [30, 35, 40, 38, 42, 45, 48, 52, 55, 58, 60, 65]
    }
    
    result = agent.run(
        chart_type="line",
        data=data,
        title="Revenue Growth Trend",
        xlabel="Month",
        ylabel="Revenue ($1000)",
        output_dir=OUTPUT_DIR
    )
    
    print(f"\n📈 Line Chart Created: {result}\n")
    print("=" * 80 + "\n")
    
    return result


def test_pie_chart():
    """Test pie chart generation."""
    print("=" * 80)
    print("TEST 3: Pie Chart Generation")
    print("=" * 80)
    
    agent = create_chart_agent(model=os.getenv("CHART_MODEL", "gpt-4o-mini"))
    
    data = {
        "labels": ["Product A", "Product B", "Product C", "Product D"],
        "values": [35, 25, 20, 20]
    }
    
    result = agent.run(
        chart_type="pie",
        data=data,
        title="Market Share Distribution",
        output_dir=OUTPUT_DIR
    )
    
    print(f"\n🥧 Pie Chart Created: {result}\n")
    print("=" * 80 + "\n")
    
    return result


def test_scatter_plot():
    """Test scatter plot generation."""
    print("=" * 80)
    print("TEST 4: Scatter Plot Generation")
    print("=" * 80)
    
    agent = create_chart_agent(model=os.getenv("CHART_MODEL", "gpt-4o-mini"))
    
    data = {
        "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "y": [2, 4, 5, 7, 8, 10, 11, 13, 14, 16]
    }
    
    result = agent.run(
        chart_type="scatter",
        data=data,
        title="Correlation Analysis",
        xlabel="Variable X",
        ylabel="Variable Y",
        output_dir=OUTPUT_DIR
    )
    
    print(f"\n📍 Scatter Plot Created: {result}\n")
    print("=" * 80 + "\n")
    
    return result


def main():
    """Run all tests."""
    print("\n🚀 Starting Chart Agent Tests\n")
    print(f"📁 Outputs will be saved to: {OUTPUT_DIR}\n")
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OPENAI_API_KEY not found in .env file!")
        print("Please set your OpenAI API key in .env file.")
        sys.exit(1)
    
    print(f"✅ Using model: {os.getenv('CHART_MODEL', 'gpt-4o-mini')}\n")
    
    try:
        # Run tests
        test_bar_chart()
        input("Press Enter to continue to next test...")
        
        test_line_chart()
        input("Press Enter to continue to next test...")
        
        test_pie_chart()
        input("Press Enter to continue to next test...")
        
        test_scatter_plot()
        
        print("\n" + "=" * 80)
        print("✅ All tests completed successfully!")
        print(f"📁 All charts saved to: {OUTPUT_DIR}")
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
