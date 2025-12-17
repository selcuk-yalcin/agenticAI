# Chart Agent - Data Visualization Agent

## Overview

ChartAgent is an AI-powered data visualization agent that can analyze data and automatically generate appropriate charts and visualizations.

## Features

✅ **Automatic Data Analysis**
- Statistical analysis (mean, median, std, quartiles)
- Correlation analysis
- Distribution analysis
- Data profiling

✅ **Multiple Chart Types**
- Line charts (trends over time)
- Bar charts (categorical comparisons)
- Scatter plots (relationships)
- Pie charts (proportions)
- Heatmaps (correlations)

✅ **Smart Chart Selection**
- Agent analyzes data structure
- Automatically chooses appropriate chart types
- Provides insights and interpretations

✅ **Comprehensive Dashboards**
- Multi-chart reports
- Comparative analysis
- Dataset comparisons

## Installation

The ChartAgent requires additional dependencies:

```bash
pip install pandas matplotlib seaborn
```

## Quick Start

### Basic Usage

```python
from agents import ChartAgent
import json

# Create agent
agent = ChartAgent(model="gpt-4-turbo-preview")

# Prepare data
data = {
    "month": ["Jan", "Feb", "Mar", "Apr", "May"],
    "sales": [12000, 15000, 13500, 18000, 21000]
}

# Generate chart
result = agent.run(
    query="Create a line chart showing sales trends",
    data=json.dumps(data)
)

print(result)
```

### Automatic Analysis

Let the agent analyze and choose the best visualizations:

```python
result = agent.analyze_and_visualize(
    data=json.dumps(data),
    focus="trends"  # Optional: "correlation", "distribution"
)
```

### Create Dashboard

Generate comprehensive multi-chart reports:

```python
result = agent.create_dashboard(
    data=json.dumps(data),
    title="Sales Analysis Dashboard",
    description="Monthly sales performance"
)
```

### Compare Datasets

Compare two datasets with visualizations:

```python
result = agent.compare_datasets(
    dataset1=json.dumps(q1_data),
    dataset2=json.dumps(q2_data),
    label1="Q1 2024",
    label2="Q2 2024"
)
```

## Data Format

ChartAgent accepts data in JSON format:

### Option 1: List of Dictionaries
```json
[
    {"product": "A", "sales": 100, "profit": 20},
    {"product": "B", "sales": 150, "profit": 35},
    {"product": "C", "sales": 120, "profit": 25}
]
```

### Option 2: Dictionary of Lists
```json
{
    "product": ["A", "B", "C"],
    "sales": [100, 150, 120],
    "profit": [20, 35, 25]
}
```

## Chart Types

### 1. Line Chart
Best for: Time series, trends

```python
agent.run(
    query="Create a line chart showing monthly revenue",
    data=json.dumps({"month": [...], "revenue": [...]})
)
```

### 2. Bar Chart
Best for: Categorical comparisons

```python
agent.run(
    query="Create a bar chart comparing product sales",
    data=json.dumps({"product": [...], "sales": [...]})
)
```

### 3. Scatter Plot
Best for: Relationships between variables

```python
agent.run(
    query="Create a scatter plot showing correlation between price and sales",
    data=json.dumps({"price": [...], "sales": [...]})
)
```

### 4. Pie Chart
Best for: Proportions, percentages

```python
agent.run(
    query="Create a pie chart showing market share by category",
    data=json.dumps({"category": [...], "share": [...]})
)
```

### 5. Heatmap
Best for: Correlation matrices

```python
agent.run(
    query="Create a heatmap showing correlations between all variables",
    data=json.dumps(data_with_multiple_numeric_columns)
)
```

## Advanced Examples

### Multiple Charts in One Request

```python
result = agent.run(
    query="""
    Create THREE visualizations:
    1. Bar chart of sales by product
    2. Scatter plot of units vs revenue
    3. Pie chart of revenue distribution
    """,
    data=json.dumps(product_data)
)
```

### Custom Styling

```python
result = agent.run(
    query="""
    Create a bar chart with:
    - Blue bars for sales
    - Red bars for expenses
    - Title: "Monthly Financial Performance"
    - Highlight the best month
    """,
    data=json.dumps(financial_data)
)
```

## Tools Used by ChartAgent

### 1. data_analysis
Analyzes data structure and statistics:
- Summary statistics
- Correlation matrix
- Distribution analysis

### 2. generate_chart
Creates and saves visualizations:
- Multiple chart types
- Custom titles and labels
- High-resolution output (300 DPI)

## Output

Charts are saved to `./outputs/charts/` by default.

You can customize the output directory:

```python
agent = ChartAgent(
    model="gpt-4-turbo-preview",
    output_dir="./my_charts"
)
```

## Configuration

### Environment Variables

Set in `.env` file:

```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

### Agent Configuration

```python
agent = ChartAgent(
    model="gpt-4-turbo-preview",  # LLM model
    temperature=0.0,               # Sampling temperature
    output_dir="./outputs/charts"  # Chart output directory
)
```

## Examples

Run the examples:

```bash
cd examples
python chart_examples.py
```

Available examples:
1. Basic line chart
2. Automatic analysis
3. Comprehensive dashboard
4. Multiple charts
5. Correlation heatmap
6. Time series analysis
7. Custom visualization
8. Dataset comparison

## Best Practices

1. **Data Quality**
   - Ensure data is clean and properly formatted
   - Handle missing values before visualization
   - Use appropriate data types

2. **Chart Selection**
   - Let the agent analyze data first
   - Provide context about what you want to show
   - Be specific about insights you're looking for

3. **Queries**
   - Be clear and specific
   - Mention chart type if you have preference
   - Request specific styling if needed

4. **Performance**
   - For large datasets, consider aggregating first
   - Generate one chart at a time for complex visualizations
   - Use appropriate max_turns for tool calling

## Troubleshooting

### Charts not generating?
- Check data format (must be valid JSON)
- Verify column names exist in data
- Ensure numeric data for numeric charts

### Agent not choosing right chart?
- Be more specific in your query
- Mention the chart type explicitly
- Provide context about the data

### Low quality output?
- Charts are saved at 300 DPI by default
- Check output directory permissions
- Verify matplotlib backend

## API Reference

### ChartAgent

```python
ChartAgent(
    model: Optional[str] = None,
    temperature: float = 0.0,
    output_dir: str = "./outputs/charts"
)
```

#### Methods

**run(query, data, max_turns, return_tool_log)**
- Generate charts based on query and data

**analyze_and_visualize(data, focus)**
- Analyze and create focused visualizations

**create_dashboard(data, title, description)**
- Create comprehensive multi-chart dashboard

**compare_datasets(dataset1, dataset2, label1, label2)**
- Compare two datasets with visualizations

## Contributing

To add new chart types:

1. Add method to `ChartGenerationTool` in `tools/data_tools.py`
2. Update chart_type enum in tool definition
3. Update ChartAgent system prompt with new capabilities

## License

Same as main project.

## Support

For issues or questions:
- Check examples in `examples/chart_examples.py`
- Review QUICKSTART.md
- See main README.md
