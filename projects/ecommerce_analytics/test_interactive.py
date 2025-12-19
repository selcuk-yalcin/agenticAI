#!/usr/bin/env python3
"""
Interactive E-commerce Analytics
=================================
Interactive tool for analyzing e-commerce metrics.
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
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "interactive")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_result(filename: str, content: str):
    """Save result to file."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"\n💾 Saved to: {filepath}")
    return filepath


def quick_analysis_menu():
    """Show quick analysis options."""
    print("\n" + "=" * 80)
    print("⚡ QUICK ANALYSIS")
    print("=" * 80)
    print("\n1. 📊 Sales Performance Summary")
    print("2. 🎯 Product Portfolio Review")
    print("3. 👥 Customer Insights")
    print("4. 🛒 Conversion Funnel Analysis")
    print("5. 💰 Revenue Opportunities")
    print("6. 📦 Inventory Health Check")
    print("7. 📢 Marketing Effectiveness")
    print("8. 🔮 Quick Forecast")
    print("9. 🔙 Back to Main Menu")
    
    choice = input("\nSelect analysis (1-9): ").strip()
    return choice


def run_quick_analysis(choice: str, agent):
    """Run selected quick analysis."""
    analyses = {
        "1": {
            "name": "Sales Performance Summary",
            "prompt": """Provide a comprehensive sales performance summary including:
            - Overall revenue trends
            - Key growth drivers
            - Top performing categories
            - Sales velocity metrics
            - Recommendations for improvement"""
        },
        "2": {
            "name": "Product Portfolio Review",
            "prompt": """Analyze the product portfolio:
            - Star products (high sales, high margin)
            - Cash cows (steady sellers)
            - Problem products (low performance)
            - Opportunities (potential winners)
            - Portfolio optimization recommendations"""
        },
        "3": {
            "name": "Customer Insights",
            "prompt": """Provide customer behavior insights:
            - Customer segmentation overview
            - Purchase patterns and trends
            - Retention and churn analysis
            - Lifetime value opportunities
            - Personalization strategies"""
        },
        "4": {
            "name": "Conversion Funnel Analysis",
            "prompt": """Analyze the conversion funnel:
            - Traffic sources and quality
            - Conversion rate by stage
            - Drop-off points and causes
            - Optimization opportunities
            - Expected impact of improvements"""
        },
        "5": {
            "name": "Revenue Opportunities",
            "prompt": """Identify revenue growth opportunities:
            - Upsell and cross-sell potential
            - Pricing optimization opportunities
            - New customer acquisition strategies
            - Retention improvement tactics
            - Quick wins for revenue boost"""
        },
        "6": {
            "name": "Inventory Health Check",
            "prompt": """Assess inventory health:
            - Stock level status by category
            - Overstock and understock items
            - Turnover rate analysis
            - Cost optimization opportunities
            - Reorder recommendations"""
        },
        "7": {
            "name": "Marketing Effectiveness",
            "prompt": """Evaluate marketing performance:
            - Channel ROI comparison
            - Customer acquisition efficiency
            - Campaign performance insights
            - Budget allocation recommendations
            - Quick optimization wins"""
        },
        "8": {
            "name": "Quick Forecast",
            "prompt": """Provide a quick revenue forecast:
            - Next month projection
            - Key assumptions
            - Risk factors
            - Opportunities to exceed forecast
            - Actions to maximize results"""
        }
    }
    
    if choice not in analyses:
        return None
    
    analysis = analyses[choice]
    print(f"\n🚀 Running: {analysis['name']}")
    print("\n⏳ Processing...")
    
    result = agent.run(analysis['prompt'])
    
    print("\n" + "=" * 80)
    print(f"📈 {analysis['name'].upper()}")
    print("=" * 80)
    print(result)
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{analysis['name'].replace(' ', '_').lower()}_{timestamp}.txt"
    save_result(filename, result)
    
    return result


def custom_analysis():
    """Run custom analysis with user-provided data and question."""
    print("\n" + "=" * 80)
    print("🎨 CUSTOM ANALYSIS")
    print("=" * 80)
    
    print("\n1️⃣  What type of analysis do you need?")
    print("   Examples:")
    print("   - 'Analyze why sales dropped last month'")
    print("   - 'Identify best products to promote'")
    print("   - 'Find customer churn patterns'")
    print("   - 'Optimize pricing strategy'")
    
    question = input("\nYour question: ").strip()
    
    if not question:
        print("❌ Question cannot be empty!")
        return
    
    print("\n2️⃣  Provide relevant data or context (optional):")
    print("   Press Enter to skip, or paste your data:")
    
    context = input("\nContext/Data: ").strip()
    
    # Build prompt
    if context:
        prompt = f"{question}\n\nContext:\n{context}"
    else:
        prompt = question
    
    print(f"\n🚀 Analyzing...")
    
    agent = create_analytics_agent(
        model=os.getenv("ANALYTICS_MODEL", "gpt-4o-mini"),
        temperature=0.2
    )
    
    print("\n⏳ Processing...")
    result = agent.run(prompt)
    
    print("\n" + "=" * 80)
    print("📊 ANALYSIS RESULT")
    print("=" * 80)
    print(result)
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"custom_analysis_{timestamp}.txt"
    save_result(filename, result)


def scenario_planning():
    """Interactive scenario planning and what-if analysis."""
    print("\n" + "=" * 80)
    print("🔮 SCENARIO PLANNING")
    print("=" * 80)
    
    print("\nSelect scenario type:")
    print("1. 📈 Growth Scenario (What if sales increase X%?)")
    print("2. 📉 Risk Scenario (What if we lose key customers?)")
    print("3. 💰 Pricing Change (What if we adjust prices?)")
    print("4. 🎯 Marketing Investment (What if we increase budget?)")
    print("5. 🆕 New Product Launch (Impact analysis)")
    print("6. 🎨 Custom Scenario")
    
    choice = input("\nSelect (1-6): ").strip()
    
    scenarios = {
        "1": "Analyze the impact of a 20% increase in monthly sales on revenue, costs, inventory, and cash flow",
        "2": "Analyze the risk and mitigation strategies if we lose our top 10% customers",
        "3": "Analyze the impact of increasing product prices by 15% on sales volume, revenue, and customer behavior",
        "4": "Analyze the potential ROI of doubling our marketing budget across different channels",
        "5": "Analyze the launch strategy and expected impact of introducing 3 new products in Q1"
    }
    
    if choice == "6":
        scenario = input("\nDescribe your scenario: ").strip()
    elif choice in scenarios:
        scenario = scenarios[choice]
        print(f"\n📋 Scenario: {scenario}")
    else:
        print("❌ Invalid choice!")
        return
    
    agent = create_analytics_agent(
        model=os.getenv("ANALYTICS_MODEL", "gpt-4o-mini"),
        temperature=0.2
    )
    
    print("\n⏳ Processing scenario...")
    result = agent.run(f"Scenario Analysis: {scenario}\n\nProvide: Best case, base case, worst case analysis with specific impacts and recommendations.")
    
    print("\n" + "=" * 80)
    print("🔮 SCENARIO ANALYSIS")
    print("=" * 80)
    print(result)
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"scenario_planning_{timestamp}.txt"
    save_result(filename, result)


def competitive_analysis():
    """Competitive analysis and benchmarking."""
    print("\n" + "=" * 80)
    print("🏆 COMPETITIVE ANALYSIS")
    print("=" * 80)
    
    print("\n1️⃣  Describe your competitive landscape:")
    print("   Example: 'We compete with 3 major players in electronics'")
    
    landscape = input("\nCompetitive landscape: ").strip()
    
    print("\n2️⃣  What metrics do you want to compare?")
    print("   Example: 'pricing, product range, customer service'")
    
    metrics = input("\nMetrics (or press Enter for default): ").strip()
    if not metrics:
        metrics = "pricing, product range, customer service, shipping, user experience"
    
    print("\n3️⃣  Any specific concerns or questions?")
    print("   Example: 'How can we differentiate from competitors?'")
    
    concerns = input("\nConcerns (or press Enter to skip): ").strip()
    
    # Build prompt
    prompt = f"""Competitive Analysis:

Landscape: {landscape}
Metrics to Compare: {metrics}
{f'Specific Concerns: {concerns}' if concerns else ''}

Please provide:
1. Competitive positioning analysis
2. Strengths and weaknesses vs competitors
3. Market gaps and opportunities
4. Differentiation strategies
5. Competitive advantages to leverage
6. Threats to watch
7. Action plan for competitive advantage"""
    
    agent = create_analytics_agent(
        model=os.getenv("ANALYTICS_MODEL", "gpt-4o-mini"),
        temperature=0.2
    )
    
    print("\n⏳ Analyzing competition...")
    result = agent.run(prompt)
    
    print("\n" + "=" * 80)
    print("🏆 COMPETITIVE ANALYSIS")
    print("=" * 80)
    print(result)
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"competitive_analysis_{timestamp}.txt"
    save_result(filename, result)


def main():
    """Main interactive menu."""
    print("\n" + "=" * 80)
    print("💼 INTERACTIVE E-COMMERCE ANALYTICS")
    print("=" * 80)
    print(f"\n📁 Outputs: {OUTPUT_DIR}")
    print(f"🤖 Model: {os.getenv('ANALYTICS_MODEL', 'gpt-4o-mini')}")
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ ERROR: OPENAI_API_KEY not found!")
        sys.exit(1)
    
    agent = create_analytics_agent(
        model=os.getenv("ANALYTICS_MODEL", "gpt-4o-mini"),
        temperature=0.2
    )
    
    while True:
        print("\n" + "=" * 80)
        print("MAIN MENU")
        print("=" * 80)
        print("\n1. ⚡ Quick Analysis (Pre-defined)")
        print("2. 🎨 Custom Analysis (Your question)")
        print("3. 🔮 Scenario Planning (What-if analysis)")
        print("4. 🏆 Competitive Analysis")
        print("5. 📊 Business Health Dashboard")
        print("6. 🚪 Exit")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        try:
            if choice == '1':
                analysis_choice = quick_analysis_menu()
                if analysis_choice == '9':
                    continue
                run_quick_analysis(analysis_choice, agent)
            
            elif choice == '2':
                custom_analysis()
            
            elif choice == '3':
                scenario_planning()
            
            elif choice == '4':
                competitive_analysis()
            
            elif choice == '5':
                print("\n🚀 Generating Business Health Dashboard...")
                print("\n⏳ Processing...")
                result = agent.run("""Create a comprehensive business health dashboard covering:
                1. Revenue and growth metrics
                2. Customer acquisition and retention
                3. Product performance
                4. Operational efficiency
                5. Financial health
                6. Key risks and opportunities
                7. Top 3 priorities for next quarter""")
                print("\n" + "=" * 80)
                print("📊 BUSINESS HEALTH DASHBOARD")
                print("=" * 80)
                print(result)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_result(f"business_health_dashboard_{timestamp}.txt", result)
            
            elif choice == '6':
                print("\n👋 Goodbye!")
                break
            
            else:
                print("\n❌ Invalid choice! Please select 1-6.")
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user.")
            continue
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
