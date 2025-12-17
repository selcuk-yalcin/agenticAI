"""
Chart Agent Examples
===================
Examples for using the ChartAgent for data visualization.
"""

import json
from agents import ChartAgent

# Sample data
sample_sales_data = {
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "sales": [12000, 15000, 13500, 18000, 21000, 19500],
    "expenses": [8000, 9500, 9000, 11000, 13000, 12500]
}

sample_product_data = [
    {"product": "Laptop", "revenue": 45000, "units": 150},
    {"product": "Phone", "revenue": 38000, "units": 250},
    {"product": "Tablet", "revenue": 28000, "units": 180},
    {"product": "Monitor", "revenue": 22000, "units": 200},
    {"product": "Keyboard", "revenue": 12000, "units": 400}
]

sample_correlation_data = {
    "temperature": [20, 22, 25, 27, 30, 32, 35, 28, 26, 24],
    "ice_cream_sales": [150, 180, 220, 250, 320, 380, 450, 280, 240, 200],
    "sunscreen_sales": [80, 95, 120, 140, 180, 210, 260, 150, 130, 110]
}


def example_1_basic_chart():
    """Example 1: Generate a basic line chart."""
    print("=== Example 1: Basic Line Chart ===\n")
    
    agent = ChartAgent(model="gpt-4-turbo-preview")
    
    data_json = json.dumps(sample_sales_data)
    
    result = agent.run(
        query="Create a line chart showing sales and expenses over months. Use different colors for each line.",
        data=data_json
    )
    
    print(result)
    print("\n" + "="*50 + "\n")


def example_2_automatic_analysis():
    """Example 2: Let agent analyze and choose chart type."""
    print("=== Example 2: Automatic Analysis ===\n")
    
    agent = ChartAgent(model="gpt-4-turbo-preview")
    
    data_json = json.dumps(sample_product_data)
    
    result = agent.analyze_and_visualize(
        data=data_json,
        focus="revenue comparison"
    )
    
    print(result)
    print("\n" + "="*50 + "\n")


def example_3_dashboard():
    """Example 3: Create a comprehensive dashboard."""
    print("=== Example 3: Comprehensive Dashboard ===\n")
    
    agent = ChartAgent(model="gpt-4-turbo-preview")
    
    data_json = json.dumps(sample_correlation_data)
    
    result = agent.create_dashboard(
        data=data_json,
        title="Temperature & Sales Analysis",
        description="Relationship between temperature and product sales"
    )
    
    print(result)
    print("\n" + "="*50 + "\n")


def example_4_multiple_charts():
    """Example 4: Generate multiple charts in one request."""
    print("=== Example 4: Multiple Charts ===\n")
    
    agent = ChartAgent(model="gpt-4-turbo-preview")
    
    data_json = json.dumps(sample_product_data)
    
    result = agent.run(
        query="""Analyze this product data and create THREE different charts:
        1. Bar chart comparing revenue by product
        2. Scatter plot showing relationship between units and revenue
        3. Pie chart showing revenue distribution
        
        Use descriptive titles for each chart.""",
        data=data_json
    )
    
    print(result)
    print("\n" + "="*50 + "\n")


def example_5_correlation_heatmap():
    """Example 5: Generate correlation heatmap."""
    print("=== Example 5: Correlation Heatmap ===\n")
    
    agent = ChartAgent(model="gpt-4-turbo-preview")
    
    data_json = json.dumps(sample_correlation_data)
    
    result = agent.run(
        query="Analyze correlations between variables and create a heatmap visualization.",
        data=data_json
    )
    
    print(result)
    print("\n" + "="*50 + "\n")


def example_6_time_series():
    """Example 6: Time series analysis with trends."""
    print("=== Example 6: Time Series Analysis ===\n")
    
    agent = ChartAgent(model="gpt-4-turbo-preview")
    
    # Generate more data for time series
    monthly_data = {
        "date": [f"2024-{i:02d}" for i in range(1, 13)],
        "visitors": [1200, 1350, 1500, 1800, 2100, 2400, 2200, 2600, 2800, 2500, 2900, 3100],
        "conversions": [120, 135, 165, 198, 231, 264, 242, 286, 308, 275, 319, 341]
    }
    
    data_json = json.dumps(monthly_data)
    
    result = agent.run(
        query="""Analyze this monthly website data and create visualizations showing:
        1. Visitor trends over time
        2. Conversion trends
        3. Relationship between visitors and conversions
        
        Identify any patterns or insights.""",
        data=data_json
    )
    
    print(result)
    print("\n" + "="*50 + "\n")


def example_7_custom_visualization():
    """Example 7: Custom visualization with specific requirements."""
    print("=== Example 7: Custom Visualization ===\n")
    
    agent = ChartAgent(model="gpt-4-turbo-preview")
    
    data_json = json.dumps(sample_sales_data)
    
    result = agent.run(
        query="""Create a visualization that shows:
        - Sales as blue bars
        - Expenses as red bars
        - Calculate and mention profit (sales - expenses) for each month
        - Add title "Monthly Financial Overview"
        - Highlight the best performing month""",
        data=data_json
    )
    
    print(result)
    print("\n" + "="*50 + "\n")


def example_8_compare_datasets():
    """Example 8: Compare two datasets."""
    print("=== Example 8: Dataset Comparison ===\n")
    
    agent = ChartAgent(model="gpt-4-turbo-preview")
    
    q1_data = {
        "category": ["Electronics", "Clothing", "Food", "Home"],
        "sales": [45000, 32000, 28000, 19000]
    }
    
    q2_data = {
        "category": ["Electronics", "Clothing", "Food", "Home"],
        "sales": [52000, 29000, 31000, 22000]
    }
    
    result = agent.compare_datasets(
        dataset1=json.dumps(q1_data),
        dataset2=json.dumps(q2_data),
        label1="Q1 2024",
        label2="Q2 2024"
    )
    
    print(result)
    print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("CHART AGENT EXAMPLES")
    print("="*70 + "\n")
    
    # Run examples
    # Uncomment the ones you want to run
    
    example_1_basic_chart()
    # example_2_automatic_analysis()
    # example_3_dashboard()
    # example_4_multiple_charts()
    # example_5_correlation_heatmap()
    # example_6_time_series()
    # example_7_custom_visualization()
    # example_8_compare_datasets()
    
    print("\n" + "="*70)
    print("Examples completed! Check ./outputs/charts/ for generated charts.")
    print("="*70 + "\n")
