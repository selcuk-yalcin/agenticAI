#!/usr/bin/env python3
"""
Advanced E-commerce Analytics Tests
====================================
Comprehensive testing of Analytics Agent capabilities.
"""

import os
import sys
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from projects.ecommerce_analytics.agents.analytics_agent import create_analytics_agent

# Create outputs directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "advanced_tests")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_result(filename: str, content: str):
    """Save test result to file."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        if isinstance(content, dict):
            f.write(json.dumps(content, indent=2, ensure_ascii=False))
        else:
            f.write(content)
    print(f"💾 Saved to: {filepath}")
    return filepath


def test_sales_trend_analysis():
    """Test 1: Comprehensive sales trend analysis."""
    print("\n" + "=" * 80)
    print("TEST 1: Sales Trend Analysis")
    print("=" * 80)
    
    agent = create_analytics_agent(
        model=os.getenv("ANALYTICS_MODEL", "gpt-4o-mini"),
        temperature=0.2
    )
    
    # Simulated sales data context
    sales_context = """
    Sales Data Summary (Last 30 Days):
    - Total Revenue: $156,750
    - Total Orders: 342
    - Average Order Value: $458.33
    - Growth vs Previous Period: +12.5%
    
    Weekly Breakdown:
    Week 1: $35,200 (78 orders)
    Week 2: $42,100 (91 orders)
    Week 3: $38,450 (82 orders)
    Week 4: $41,000 (91 orders)
    
    Top Categories:
    1. Electronics: $62,700 (40%)
    2. Fashion: $47,025 (30%)
    3. Home & Garden: $31,350 (20%)
    4. Sports: $15,675 (10%)
    """
    
    print("\n📊 Analyzing sales trends...")
    print(f"   Period: Last 30 days")
    print(f"   Total Revenue: $156,750")
    print(f"   Total Orders: 342")
    
    # Create enhanced prompt with data
    prompt = f"""Based on this e-commerce data, provide a comprehensive sales trend analysis:

{sales_context}

Please analyze:
1. Overall trend and growth pattern
2. Weekly performance variations
3. Category performance insights
4. Notable patterns or anomalies
5. Recommendations for optimization
6. Forecast for next 30 days"""
    
    result = agent.run(prompt)
    
    print(f"\n📈 Analysis Result (first 400 chars):\n{result[:400]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"sales_trend_analysis_{timestamp}.txt", result)
    
    print("\n" + "=" * 80)
    return result


def test_product_performance():
    """Test 2: Product performance analysis."""
    print("\n" + "=" * 80)
    print("TEST 2: Product Performance Analysis")
    print("=" * 80)
    
    agent = create_analytics_agent(
        model=os.getenv("ANALYTICS_MODEL", "gpt-4o-mini"),
        temperature=0.2
    )
    
    product_data = """
    Product Performance Metrics (Last Quarter):
    
    Product A - Wireless Headphones:
    - Units Sold: 1,234
    - Revenue: $123,400
    - Avg Price: $100
    - Conversion Rate: 3.2%
    - Return Rate: 2.1%
    - Customer Rating: 4.5/5
    
    Product B - Smart Watch:
    - Units Sold: 856
    - Revenue: $171,200
    - Avg Price: $200
    - Conversion Rate: 2.8%
    - Return Rate: 4.5%
    - Customer Rating: 4.2/5
    
    Product C - Laptop Stand:
    - Units Sold: 2,145
    - Revenue: $85,800
    - Avg Price: $40
    - Conversion Rate: 5.1%
    - Return Rate: 1.8%
    - Customer Rating: 4.7/5
    
    Product D - USB-C Cable:
    - Units Sold: 3,421
    - Revenue: $51,315
    - Avg Price: $15
    - Conversion Rate: 6.2%
    - Return Rate: 3.2%
    - Customer Rating: 4.1/5
    
    Product E - Bluetooth Speaker:
    - Units Sold: 678
    - Revenue: $101,700
    - Avg Price: $150
    - Conversion Rate: 2.3%
    - Return Rate: 5.8%
    - Customer Rating: 3.9/5
    """
    
    print("\n🎯 Analyzing product performance...")
    print(f"   Products: 5 key items")
    print(f"   Metrics: Sales, Revenue, Conversion, Returns, Ratings")
    
    prompt = f"""Analyze these product performance metrics and provide insights:

{product_data}

Please provide:
1. Top 3 performers and why they excel
2. Products needing improvement and specific actions
3. Pricing optimization opportunities
4. Inventory recommendations
5. Marketing strategy suggestions for each product
6. Cross-selling opportunities"""
    
    result = agent.run(prompt)
    
    print(f"\n📊 Performance Analysis (first 400 chars):\n{result[:400]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"product_performance_{timestamp}.txt", result)
    
    print("\n" + "=" * 80)
    return result


def test_customer_behavior():
    """Test 3: Customer behavior and segmentation."""
    print("\n" + "=" * 80)
    print("TEST 3: Customer Behavior Analysis")
    print("=" * 80)
    
    agent = create_analytics_agent(
        model=os.getenv("ANALYTICS_MODEL", "gpt-4o-mini"),
        temperature=0.2
    )
    
    customer_data = """
    Customer Segmentation Analysis:
    
    Segment 1: VIP Customers (Top 10%)
    - Count: 145 customers
    - Avg Order Value: $850
    - Purchase Frequency: 8.5 times/year
    - Lifetime Value: $7,225
    - Churn Rate: 5%
    - Preferred Categories: Electronics, Fashion
    
    Segment 2: Regular Customers (20%)
    - Count: 290 customers
    - Avg Order Value: $420
    - Purchase Frequency: 4.2 times/year
    - Lifetime Value: $1,764
    - Churn Rate: 12%
    - Preferred Categories: Electronics, Home
    
    Segment 3: Occasional Buyers (30%)
    - Count: 435 customers
    - Avg Order Value: $280
    - Purchase Frequency: 2.1 times/year
    - Lifetime Value: $588
    - Churn Rate: 25%
    - Preferred Categories: Fashion, Sports
    
    Segment 4: New Customers (40%)
    - Count: 580 customers
    - Avg Order Value: $220
    - Purchase Frequency: 1.2 times/year
    - Lifetime Value: $264
    - Churn Rate: 45%
    - Preferred Categories: Various
    
    Overall Metrics:
    - Total Active Customers: 1,450
    - Average Customer Lifetime: 2.3 years
    - Customer Acquisition Cost: $45
    - Retention Rate: 68%
    """
    
    print("\n👥 Analyzing customer behavior...")
    print(f"   Total Customers: 1,450")
    print(f"   Segments: 4 (VIP, Regular, Occasional, New)")
    
    prompt = f"""Analyze this customer behavior data and provide strategic insights:

{customer_data}

Please analyze:
1. Key characteristics of each segment
2. Opportunities to move customers up segments
3. Churn risk mitigation strategies
4. Personalization recommendations for each segment
5. Customer lifetime value optimization tactics
6. Retention campaign ideas
7. New customer onboarding improvements"""
    
    result = agent.run(prompt)
    
    print(f"\n🎯 Behavior Analysis (first 400 chars):\n{result[:400]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"customer_behavior_{timestamp}.txt", result)
    
    print("\n" + "=" * 80)
    return result


def test_cart_abandonment():
    """Test 4: Cart abandonment analysis."""
    print("\n" + "=" * 80)
    print("TEST 4: Cart Abandonment Analysis")
    print("=" * 80)
    
    agent = create_analytics_agent(
        model=os.getenv("ANALYTICS_MODEL", "gpt-4o-mini"),
        temperature=0.2
    )
    
    abandonment_data = """
    Cart Abandonment Data (Last 30 Days):
    
    Overall Statistics:
    - Carts Created: 2,456
    - Completed Purchases: 1,623
    - Abandoned Carts: 833
    - Abandonment Rate: 33.9%
    - Potential Lost Revenue: $187,425
    
    Abandonment by Stage:
    - Cart Page: 45% (375 carts)
    - Shipping Info: 30% (250 carts)
    - Payment Page: 25% (208 carts)
    
    Abandonment by Category:
    - Electronics: 38% (highest)
    - Fashion: 32%
    - Home & Garden: 28%
    - Sports: 25% (lowest)
    
    Common Factors (from exit surveys):
    - High shipping costs: 35%
    - Just browsing/comparing: 28%
    - Unexpected fees: 18%
    - Complex checkout: 12%
    - Payment security concerns: 7%
    
    Cart Value Analysis:
    - Avg Abandoned Cart Value: $225
    - Carts >$500: 15% abandonment
    - Carts $200-$500: 32% abandonment
    - Carts <$200: 42% abandonment
    
    Recovery Campaign Results:
    - Email recovery rate: 18%
    - SMS recovery rate: 12%
    - Push notification recovery rate: 8%
    """
    
    print("\n🛒 Analyzing cart abandonment...")
    print(f"   Abandonment Rate: 33.9%")
    print(f"   Abandoned Carts: 833")
    print(f"   Lost Revenue: $187,425")
    
    prompt = f"""Analyze this cart abandonment data and provide actionable strategies:

{abandonment_data}

Please provide:
1. Root cause analysis for high abandonment rate
2. Stage-specific optimization recommendations
3. Category-specific strategies
4. Checkout process improvements
5. Recovery campaign optimization
6. Pricing and shipping strategy suggestions
7. Technical improvements needed
8. A/B testing recommendations
9. Expected impact of implementing changes"""
    
    result = agent.run(prompt)
    
    print(f"\n💡 Abandonment Analysis (first 400 chars):\n{result[:400]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"cart_abandonment_{timestamp}.txt", result)
    
    print("\n" + "=" * 80)
    return result


def test_revenue_forecast():
    """Test 5: Revenue forecasting."""
    print("\n" + "=" * 80)
    print("TEST 5: Revenue Forecasting")
    print("=" * 80)
    
    agent = create_analytics_agent(
        model=os.getenv("ANALYTICS_MODEL", "gpt-4o-mini"),
        temperature=0.2,
        enable_forecasting=True
    )
    
    historical_data = """
    Historical Revenue Data:
    
    Q4 2024: $420,000
    Q1 2025: $465,000 (+10.7%)
    Q2 2025: $512,000 (+10.1%)
    Q3 2025: $548,000 (+7.0%)
    
    Seasonal Patterns:
    - Q4: +25% (holiday season)
    - Q1: -8% (post-holiday)
    - Q2: +12% (spring)
    - Q3: +5% (summer)
    
    Current Trends (Q3 2025):
    - Average Monthly Revenue: $182,667
    - Month-over-Month Growth: 2.3%
    - New Customer Acquisition: +15%
    - Customer Retention: 68%
    - Average Order Value: +5%
    
    Market Factors:
    - Industry Growth Rate: 8% annually
    - Competitive Landscape: Moderate
    - Economic Indicators: Stable
    - Planned Initiatives: New product line launch (Oct), Marketing campaign (Nov)
    
    Risks & Opportunities:
    - Supply chain stability: Good
    - Competitor actions: Moderate risk
    - Marketing ROI: Improving (+20% efficiency)
    - Customer satisfaction: 4.3/5 (stable)
    """
    
    print("\n📈 Forecasting revenue for Q4 2025...")
    print(f"   Current Quarter (Q3): $548,000")
    print(f"   Growth Trend: +7.0%")
    
    prompt = f"""Based on this historical data and trends, forecast Q4 2025 revenue:

{historical_data}

Please provide:
1. Base case forecast (most likely)
2. Optimistic scenario
3. Conservative scenario
4. Confidence level and reasoning
5. Key assumptions made
6. Risk factors that could impact forecast
7. Opportunities to exceed forecast
8. Recommended actions to maximize revenue
9. KPIs to monitor closely
10. Contingency plans for different scenarios"""
    
    result = agent.run(prompt)
    
    print(f"\n🔮 Forecast Analysis (first 400 chars):\n{result[:400]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"revenue_forecast_{timestamp}.txt", result)
    
    print("\n" + "=" * 80)
    return result


def test_product_recommendations():
    """Test 6: Product recommendation engine analysis."""
    print("\n" + "=" * 80)
    print("TEST 6: Product Recommendation Analysis")
    print("=" * 80)
    
    agent = create_analytics_agent(
        model=os.getenv("ANALYTICS_MODEL", "gpt-4o-mini"),
        temperature=0.2
    )
    
    recommendation_data = """
    Recommendation Engine Performance:
    
    Customer: C-12345 (VIP Segment)
    Purchase History:
    - Wireless Headphones ($100) - 3 months ago
    - Laptop Stand ($40) - 2 months ago
    - USB-C Cable ($15) - 1 month ago
    - Total Spent: $1,850 (last year)
    
    Browsing History (Last 7 Days):
    - Smart Watch (viewed 3 times)
    - Fitness Tracker (viewed 2 times)
    - Wireless Earbuds (viewed 2 times)
    - Portable Charger (viewed 1 time)
    
    Similar Customers Bought:
    1. Smart Watch ($200) - 45% of similar customers
    2. Wireless Earbuds ($80) - 38% of similar customers
    3. Fitness Tracker ($120) - 32% of similar customers
    4. Portable Charger ($35) - 28% of similar customers
    5. Screen Protector ($25) - 25% of similar customers
    
    Frequently Bought Together (with customer's previous purchases):
    - Headphones + Carrying Case: 67% bundle rate
    - Laptop Stand + Monitor Arm: 45% bundle rate
    - USB-C Cable + Wall Adapter: 78% bundle rate
    
    Trending in Customer's Category:
    - Smart Home Hub ($150)
    - Noise Cancelling Headphones ($180)
    - Wireless Keyboard ($90)
    
    Seasonal Opportunities:
    - Holiday Gift Sets (approaching)
    - Winter Sports Equipment
    - Year-end Tech Deals
    """
    
    print("\n🎁 Generating product recommendations...")
    print(f"   Customer: VIP Segment")
    print(f"   Previous Purchases: 3 items")
    print(f"   Recent Browsing: 4 categories")
    
    prompt = f"""Analyze this customer data and generate personalized product recommendations:

{recommendation_data}

Please provide:
1. Top 5 product recommendations with reasoning
2. Cross-sell opportunities based on purchase history
3. Upsell strategies for higher-value items
4. Bundle suggestions
5. Timing recommendations (when to present each offer)
6. Personalized messaging for each recommendation
7. Expected conversion rates
8. Incremental revenue potential
9. Long-term customer value strategy"""
    
    result = agent.run(prompt)
    
    print(f"\n🎯 Recommendation Analysis (first 400 chars):\n{result[:400]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"product_recommendations_{timestamp}.txt", result)
    
    print("\n" + "=" * 80)
    return result


def test_inventory_optimization():
    """Test 7: Inventory optimization analysis."""
    print("\n" + "=" * 80)
    print("TEST 7: Inventory Optimization")
    print("=" * 80)
    
    agent = create_analytics_agent(
        model=os.getenv("ANALYTICS_MODEL", "gpt-4o-mini"),
        temperature=0.2
    )
    
    inventory_data = """
    Inventory Status Report:
    
    Product A - Wireless Headphones:
    - Current Stock: 450 units
    - Weekly Sales: 95 units
    - Stock Coverage: 4.7 weeks
    - Reorder Point: 200 units
    - Lead Time: 3 weeks
    - Storage Cost: $2/unit/month
    - Status: Adequate
    
    Product B - Smart Watch:
    - Current Stock: 85 units
    - Weekly Sales: 65 units
    - Stock Coverage: 1.3 weeks
    - Reorder Point: 150 units
    - Lead Time: 4 weeks
    - Storage Cost: $5/unit/month
    - Status: CRITICAL - Below reorder point
    
    Product C - Laptop Stand:
    - Current Stock: 1,200 units
    - Weekly Sales: 165 units
    - Stock Coverage: 7.3 weeks
    - Reorder Point: 400 units
    - Lead Time: 2 weeks
    - Storage Cost: $1/unit/month
    - Status: Overstocked
    
    Product D - USB-C Cable:
    - Current Stock: 2,800 units
    - Weekly Sales: 265 units
    - Stock Coverage: 10.6 weeks
    - Reorder Point: 600 units
    - Lead Time: 1 week
    - Storage Cost: $0.25/unit/month
    - Status: Overstocked
    
    Product E - Bluetooth Speaker:
    - Current Stock: 180 units
    - Weekly Sales: 52 units
    - Stock Coverage: 3.5 weeks
    - Reorder Point: 120 units
    - Lead Time: 3 weeks
    - Storage Cost: $3/unit/month
    - Status: Adequate
    
    Overall Metrics:
    - Total Inventory Value: $487,500
    - Monthly Storage Cost: $8,450
    - Stockout Events (Last Month): 3
    - Excess Inventory Cost: $12,300/month
    - Inventory Turnover Rate: 6.2x/year
    """
    
    print("\n📦 Analyzing inventory levels...")
    print(f"   Products: 5 items")
    print(f"   Total Value: $487,500")
    print(f"   Storage Cost: $8,450/month")
    
    prompt = f"""Analyze this inventory data and provide optimization recommendations:

{inventory_data}

Please provide:
1. Immediate action items for critical stock levels
2. Overstocked products and clearance strategies
3. Optimal reorder points and quantities
4. Cost reduction opportunities
5. Demand forecasting improvements
6. Supplier relationship optimization
7. Just-in-time inventory possibilities
8. Risk mitigation for supply chain disruptions
9. Expected cost savings from optimization
10. Implementation timeline and priorities"""
    
    result = agent.run(prompt)
    
    print(f"\n📊 Inventory Analysis (first 400 chars):\n{result[:400]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"inventory_optimization_{timestamp}.txt", result)
    
    print("\n" + "=" * 80)
    return result


def test_marketing_roi():
    """Test 8: Marketing ROI analysis."""
    print("\n" + "=" * 80)
    print("TEST 8: Marketing ROI Analysis")
    print("=" * 80)
    
    agent = create_analytics_agent(
        model=os.getenv("ANALYTICS_MODEL", "gpt-4o-mini"),
        temperature=0.2
    )
    
    marketing_data = """
    Marketing Campaign Performance (Last Quarter):
    
    Campaign 1: Google Ads - Electronics
    - Budget: $15,000
    - Impressions: 850,000
    - Clicks: 12,750 (CTR: 1.5%)
    - Conversions: 383 (Conv Rate: 3.0%)
    - Revenue: $57,450
    - ROI: 283%
    - CPA: $39.16
    - ROAS: 3.83
    
    Campaign 2: Facebook Ads - Fashion
    - Budget: $12,000
    - Impressions: 1,200,000
    - Clicks: 18,000 (CTR: 1.5%)
    - Conversions: 468 (Conv Rate: 2.6%)
    - Revenue: $51,480
    - ROI: 329%
    - CPA: $25.64
    - ROAS: 4.29
    
    Campaign 3: Email Marketing - All Categories
    - Budget: $3,500
    - Emails Sent: 45,000
    - Open Rate: 24%
    - Click Rate: 5.2%
    - Conversions: 234
    - Revenue: $28,080
    - ROI: 702%
    - CPA: $14.96
    - ROAS: 8.02
    
    Campaign 4: Instagram Influencer - Lifestyle
    - Budget: $8,000
    - Reach: 450,000
    - Engagement: 13,500 (3.0%)
    - Clicks: 3,600
    - Conversions: 144
    - Revenue: $21,600
    - ROI: 170%
    - CPA: $55.56
    - ROAS: 2.70
    
    Campaign 5: SEO/Content Marketing
    - Budget: $5,000
    - Organic Visits: 28,500
    - Conversions: 285
    - Revenue: $42,750
    - ROI: 755%
    - CPA: $17.54
    - ROAS: 8.55
    
    Overall Marketing Performance:
    - Total Budget: $43,500
    - Total Revenue: $201,360
    - Overall ROI: 363%
    - Overall ROAS: 4.63
    - Customer Acquisition Cost: $30.12
    - Customer Lifetime Value: $264
    - LTV:CAC Ratio: 8.77
    """
    
    print("\n📢 Analyzing marketing ROI...")
    print(f"   Total Budget: $43,500")
    print(f"   Total Revenue: $201,360")
    print(f"   Overall ROI: 363%")
    
    prompt = f"""Analyze this marketing performance data and provide strategic recommendations:

{marketing_data}

Please provide:
1. Channel performance ranking and insights
2. Budget reallocation recommendations
3. Underperforming channels and improvement strategies
4. Best practices from top-performing campaigns
5. Customer acquisition efficiency analysis
6. Scaling opportunities for high-ROI channels
7. Testing recommendations for optimization
8. Attribution model suggestions
9. Short-term tactical adjustments
10. Long-term strategic marketing plan
11. Expected impact of recommended changes"""
    
    result = agent.run(prompt)
    
    print(f"\n💰 Marketing Analysis (first 400 chars):\n{result[:400]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"marketing_roi_{timestamp}.txt", result)
    
    print("\n" + "=" * 80)
    return result


def main():
    """Run all advanced e-commerce analytics tests."""
    print("\n" + "=" * 80)
    print("🚀 ADVANCED E-COMMERCE ANALYTICS TESTS")
    print("=" * 80)
    print(f"\n📁 Outputs: {OUTPUT_DIR}")
    print(f"🤖 Model: {os.getenv('ANALYTICS_MODEL', 'gpt-4o-mini')}\n")
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OPENAI_API_KEY not found!")
        sys.exit(1)
    
    try:
        # Run all tests
        print("\n▶️  Starting Test Suite...\n")
        
        test_sales_trend_analysis()
        input("\nPress Enter to continue...")
        
        test_product_performance()
        input("\nPress Enter to continue...")
        
        test_customer_behavior()
        input("\nPress Enter to continue...")
        
        test_cart_abandonment()
        input("\nPress Enter to continue...")
        
        test_revenue_forecast()
        input("\nPress Enter to continue...")
        
        test_product_recommendations()
        input("\nPress Enter to continue...")
        
        test_inventory_optimization()
        input("\nPress Enter to continue...")
        
        test_marketing_roi()
        
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
