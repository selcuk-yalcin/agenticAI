# Data Visualization Agent - Advanced Testing

## 📊 Test Suite Overview

Comprehensive testing suite for the Data Visualization Agent with 8 advanced test scenarios.

## 🎯 Test Scenarios

### 1. Sales Data Analysis
- **Purpose**: Multi-metric sales dashboard
- **Data**: Monthly revenue, costs, customer counts
- **Charts**: Line charts, bar charts, trend analysis
- **Output**: Comprehensive sales insights

### 2. Customer Segmentation
- **Purpose**: Customer behavior analysis
- **Data**: Age, purchases, frequency, segments
- **Charts**: Scatter plots, bar charts, distribution
- **Output**: Segmentation insights

### 3. Correlation Analysis
- **Purpose**: Relationship discovery
- **Data**: Marketing spend, sales, visits, conversion
- **Charts**: Correlation heatmap, scatter plots
- **Output**: Key relationships and insights

### 4. Time Series Trends
- **Purpose**: Temporal pattern analysis
- **Data**: Stock price, volume, sentiment over time
- **Charts**: Multi-line charts, trend indicators
- **Output**: Trend analysis and patterns

### 5. Distribution Analysis
- **Purpose**: Statistical distribution study
- **Data**: Employee salaries across departments
- **Charts**: Histograms, box plots, comparisons
- **Output**: Statistical insights

### 6. Comparative Analysis
- **Purpose**: Period-over-period comparison
- **Data**: Q1 vs Q2 product performance
- **Charts**: Side-by-side comparisons
- **Output**: Growth and change analysis

### 7. Proportion Analysis
- **Purpose**: Market share and percentages
- **Data**: Company market shares
- **Charts**: Pie charts with percentages
- **Output**: Market concentration insights

### 8. Multi-Metric Dashboard
- **Purpose**: Comprehensive KPI dashboard
- **Data**: 6 business metrics over 4 weeks
- **Charts**: Multiple chart types
- **Output**: Business performance overview

## 🚀 Running Tests

### Advanced Test Suite (All Tests)

```bash
cd /path/to/Agentic-AI
python projects/data_visualization/test_advanced_features.py
```

**Features:**
- 8 comprehensive test scenarios
- Automatic output saving
- Pause between tests for review
- Detailed console output

### Interactive Mode (Custom Tests)

```bash
python projects/data_visualization/test_interactive.py
```

**Features:**
- ⚡ Quick Test: Pre-defined examples
- 🎨 Custom Visualization: Your own data
- 📊 Dashboard Creation: Multi-chart dashboards
- 📖 Example data formats

## 📁 Output Structure

```
outputs/
├── advanced_tests/
│   ├── sales_analysis_20251218_120000.txt
│   ├── customer_segmentation_20251218_120100.txt
│   ├── correlation_analysis_20251218_120200.txt
│   ├── time_series_trends_20251218_120300.txt
│   ├── distribution_analysis_20251218_120400.txt
│   ├── comparison_analysis_20251218_120500.txt
│   ├── pie_chart_analysis_20251218_120600.txt
│   └── multi_metric_dashboard_20251218_120700.txt
└── interactive/
    ├── quick_test_sales_trends_20251218_130000.txt
    ├── custom_bar_chart_20251218_130100.txt
    └── dashboard_business_metrics_20251218_130200.txt
```

## 🎨 Interactive Mode Examples

### Quick Test
```
Select option: 1
Select test: 1 (Sales Trends)
→ Automatically creates visualization with sample data
```

### Custom Visualization
```
Select option: 2

Data: {"month": ["Jan", "Feb", "Mar"], "sales": [100, 120, 115]}

Visualization type: line chart

Instructions: Show trends with annotations
→ Creates custom line chart
```

### Dashboard Creation
```
Select option: 3

Data: {"week": [1,2,3,4], "sales": [100,120,110,130], "costs": [60,70,65,75]}

Title: Weekly Performance

Description: 4-week business metrics
→ Creates multi-chart dashboard
```

## 💡 Usage Tips

### Data Format Guidelines

**Format 1: Dict of Lists (Recommended)**
```json
{
  "category": ["A", "B", "C"],
  "values": [10, 20, 15]
}
```

**Format 2: List of Dicts**
```json
[
  {"category": "A", "value": 10},
  {"category": "B", "value": 20},
  {"category": "C", "value": 15}
]
```

### Chart Type Selection

- **Line Chart**: Time series, trends over time
- **Bar Chart**: Category comparisons, rankings
- **Pie Chart**: Proportions, percentages, market share
- **Scatter Plot**: Correlations, relationships between variables
- **Heatmap**: Correlation matrices, intensity data
- **Dashboard**: Multiple metrics, comprehensive overview

### Best Practices

1. **Clear Data Structure**: Use descriptive column names
2. **Appropriate Sample Size**: 5-50 data points works best
3. **Specific Instructions**: Tell the agent what insights you want
4. **Review Output**: Check generated charts and interpretations
5. **Save Results**: All outputs are automatically timestamped

## 🔧 Configuration

### Environment Variables

```bash
# .env file
OPENAI_API_KEY=your_api_key_here
CHART_MODEL=gpt-4o-mini  # or gpt-4o, gpt-4-turbo
```

### Agent Parameters

```python
agent = create_chart_agent(
    model="gpt-4o-mini",        # Model selection
    temperature=0.0,             # Deterministic output
    output_dir="./outputs/charts"  # Chart save location
)
```

## 📊 Output Examples

### Analysis Output Format
```
ANALYSIS RESULTS
================

Data Overview:
- Shape: 6 rows × 3 columns
- Columns: month, revenue, costs
- Data types: object, int64, int64

Statistical Summary:
- Revenue: mean=$55,167, std=$8,124
- Costs: mean=$34,833, std=$4,070

Key Insights:
1. Revenue shows upward trend (+49% over 6 months)
2. Profit margin averages 36.8%
3. Strong positive correlation between revenue and costs (r=0.98)

Visualizations Created:
✓ Line chart: revenue_trends.png
✓ Bar chart: monthly_comparison.png
✓ Analysis: profit_margin_analysis.png
```

## 🎯 Next Steps

1. **Run Advanced Tests**: Start with full test suite
2. **Try Interactive Mode**: Experiment with your own data
3. **Review Outputs**: Check generated charts and insights
4. **Customize Queries**: Modify test scenarios for your needs
5. **Integrate**: Use insights for production dashboards

## 📈 Performance

- **Processing Time**: 10-30 seconds per visualization
- **Model**: GPT-4o-mini (cost-effective, fast)
- **Cost**: ~$0.001 per chart (very cheap!)
- **Quality**: Production-ready charts and analysis

## 🆘 Troubleshooting

### Issue: "OPENAI_API_KEY not found"
**Solution**: Create .env file with your API key

### Issue: "Invalid JSON format"
**Solution**: Validate JSON at jsonlint.com before pasting

### Issue: "No charts generated"
**Solution**: Check output directory permissions

### Issue: Chart quality low
**Solution**: Use more descriptive column names and provide clear instructions

## 📚 Resources

- [Chart Agent Documentation](../README.md)
- [Data Tools Reference](tools/README.md)
- [Example Datasets](examples/)
- [API Reference](../../docs/api.md)

---

**Happy Visualizing! 📊✨**
