#!/usr/bin/env python3
"""
Interactive Chart Generator
===========================
Interactive tool for creating custom visualizations.
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
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "interactive")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_result(filename: str, content: str):
    """Save result to file."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"\n💾 Saved to: {filepath}")
    return filepath


def show_examples():
    """Show example data formats."""
    print("\n" + "=" * 80)
    print("📊 EXAMPLE DATA FORMATS")
    print("=" * 80)
    
    examples = {
        "1. Simple Bar Chart": {
            "categories": ["A", "B", "C", "D"],
            "values": [25, 40, 35, 50]
        },
        "2. Time Series": {
            "dates": ["2025-01-01", "2025-01-02", "2025-01-03"],
            "values": [100, 120, 115]
        },
        "3. Multi-Variable": {
            "x": [1, 2, 3, 4, 5],
            "y": [2, 4, 3, 5, 6],
            "z": [10, 20, 15, 25, 30]
        },
        "4. Categorical": {
            "category": ["Sales", "IT", "HR"],
            "count": [45, 32, 28],
            "budget": [500000, 350000, 280000]
        }
    }
    
    for name, data in examples.items():
        print(f"\n{name}:")
        print(json.dumps(data, indent=2))
    
    print("\n" + "=" * 80)


def quick_test_mode():
    """Run pre-defined quick tests."""
    print("\n" + "=" * 80)
    print("⚡ QUICK TEST MODE")
    print("=" * 80)
    
    tests = {
        "1": {
            "name": "Sales Trends",
            "data": {
                "month": ["Jan", "Feb", "Mar", "Apr", "May"],
                "sales": [45000, 52000, 48000, 61000, 58000]
            },
            "query": "Create a line chart showing sales trends over time"
        },
        "2": {
            "name": "Product Comparison",
            "data": {
                "product": ["Product A", "Product B", "Product C"],
                "revenue": [120000, 95000, 145000],
                "units_sold": [2400, 1900, 2900]
            },
            "query": "Create bar charts comparing product performance"
        },
        "3": {
            "name": "Market Share",
            "data": {
                "company": ["Us", "Competitor A", "Competitor B", "Others"],
                "share": [35, 28, 22, 15]
            },
            "query": "Create a pie chart showing market share distribution"
        },
        "4": {
            "name": "Correlation Analysis",
            "data": {
                "advertising": [5000, 7000, 6000, 8000, 9000],
                "sales": [45000, 58000, 52000, 63000, 71000],
                "website_visits": [2000, 2800, 2400, 3100, 3500]
            },
            "query": "Analyze correlations and create a heatmap and scatter plots"
        },
        "5": {
            "name": "Distribution Analysis",
            "data": {
                "employee_id": list(range(1, 31)),
                "salary": [45000, 52000, 48000, 61000, 58000, 67000, 55000, 49000, 71000, 63000,
                          46000, 53000, 59000, 65000, 72000, 56000, 50000, 68000, 74000, 62000,
                          47000, 54000, 60000, 66000, 73000, 57000, 51000, 69000, 75000, 64000]
            },
            "query": "Analyze salary distribution and show statistics"
        }
    }
    
    print("\nAvailable Quick Tests:")
    for key, test in tests.items():
        print(f"  {key}. {test['name']}")
    
    choice = input("\nSelect test (1-5) or 'q' to go back: ").strip()
    
    if choice == 'q':
        return
    
    if choice not in tests:
        print("❌ Invalid choice!")
        return
    
    test = tests[choice]
    print(f"\n🚀 Running: {test['name']}")
    print(f"📊 Data: {json.dumps(test['data'], indent=2)[:200]}...")
    print(f"❓ Query: {test['query']}")
    
    agent = create_chart_agent(model=os.getenv("CHART_MODEL", "gpt-4o-mini"))
    
    print("\n⏳ Processing...")
    result = agent.run(
        query=test['query'],
        data=json.dumps(test['data'])
    )
    
    print("\n" + "=" * 80)
    print("📈 RESULT")
    print("=" * 80)
    print(result)
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"quick_test_{test['name'].replace(' ', '_').lower()}_{timestamp}.txt"
    save_result(filename, result)


def custom_mode():
    """Interactive custom visualization mode."""
    print("\n" + "=" * 80)
    print("🎨 CUSTOM VISUALIZATION MODE")
    print("=" * 80)
    
    print("\n1️⃣  Enter your data (JSON format):")
    print("   Tip: Use {} for dict or [] for list format")
    print("   Type 'examples' to see example formats")
    
    data_input = input("\nData: ").strip()
    
    if data_input.lower() == 'examples':
        show_examples()
        return
    
    try:
        # Try to parse JSON
        data = json.loads(data_input)
    except json.JSONDecodeError:
        print("❌ Invalid JSON format! Please check your input.")
        return
    
    print("\n2️⃣  What kind of visualization do you want?")
    print("   Options: line chart, bar chart, pie chart, scatter plot, heatmap, dashboard")
    
    viz_type = input("\nVisualization type: ").strip()
    
    print("\n3️⃣  Any specific instructions? (optional)")
    print("   Example: 'Show trends over time', 'Include correlation analysis'")
    
    instructions = input("\nInstructions (press Enter to skip): ").strip()
    
    # Build query
    if instructions:
        query = f"Create a {viz_type}. {instructions}"
    else:
        query = f"Create a {viz_type} for this data"
    
    print(f"\n🚀 Creating visualization...")
    print(f"📊 Data size: {len(str(data))} chars")
    print(f"❓ Query: {query}")
    
    agent = create_chart_agent(model=os.getenv("CHART_MODEL", "gpt-4o-mini"))
    
    print("\n⏳ Processing...")
    result = agent.run(
        query=query,
        data=json.dumps(data)
    )
    
    print("\n" + "=" * 80)
    print("📈 RESULT")
    print("=" * 80)
    print(result)
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"custom_{viz_type.replace(' ', '_')}_{timestamp}.txt"
    save_result(filename, result)


def dashboard_mode():
    """Create a comprehensive dashboard."""
    print("\n" + "=" * 80)
    print("📊 DASHBOARD CREATION MODE")
    print("=" * 80)
    
    print("\n1️⃣  Enter your data (JSON format):")
    data_input = input("\nData: ").strip()
    
    if data_input.lower() == 'examples':
        show_examples()
        return
    
    try:
        data = json.loads(data_input)
    except json.JSONDecodeError:
        print("❌ Invalid JSON format!")
        return
    
    print("\n2️⃣  Dashboard title:")
    title = input("\nTitle: ").strip() or "Data Dashboard"
    
    print("\n3️⃣  Description (optional):")
    description = input("\nDescription: ").strip() or None
    
    print(f"\n🚀 Creating dashboard: {title}")
    
    agent = create_chart_agent(model=os.getenv("CHART_MODEL", "gpt-4o-mini"))
    
    print("\n⏳ Processing...")
    result = agent.create_dashboard(
        data=json.dumps(data),
        title=title,
        description=description
    )
    
    print("\n" + "=" * 80)
    print("📈 DASHBOARD")
    print("=" * 80)
    print(result)
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"dashboard_{title.replace(' ', '_').lower()}_{timestamp}.txt"
    save_result(filename, result)


def main():
    """Main interactive menu."""
    print("\n" + "=" * 80)
    print("🎨 INTERACTIVE CHART GENERATOR")
    print("=" * 80)
    print(f"\n📁 Outputs: {OUTPUT_DIR}")
    print(f"🤖 Model: {os.getenv('CHART_MODEL', 'gpt-4o-mini')}")
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ ERROR: OPENAI_API_KEY not found!")
        sys.exit(1)
    
    while True:
        print("\n" + "=" * 80)
        print("MENU")
        print("=" * 80)
        print("\n1. ⚡ Quick Test (Pre-defined examples)")
        print("2. 🎨 Custom Visualization (Your data)")
        print("3. 📊 Create Dashboard (Multi-chart)")
        print("4. 📖 Show Example Data Formats")
        print("5. 🚪 Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        try:
            if choice == '1':
                quick_test_mode()
            elif choice == '2':
                custom_mode()
            elif choice == '3':
                dashboard_mode()
            elif choice == '4':
                show_examples()
            elif choice == '5':
                print("\n👋 Goodbye!")
                break
            else:
                print("\n❌ Invalid choice! Please select 1-5.")
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user.")
            continue
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
