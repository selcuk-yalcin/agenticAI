# Data Visualization Project

## Overview
AI-powered data analysis and chart generation.

## Agents
- **ChartAgent**: Analyzes data and creates visualizations

## Tools
- **data_analysis_tool**: Statistical analysis and data profiling
- **chart_generation_tool**: Generate charts (line, bar, scatter, pie, heatmap)

## Usage
```python
from projects.data_visualization import ChartAgent
import json

agent = ChartAgent()
data = {"month": ["Jan", "Feb"], "sales": [100, 150]}
result = agent.run("Create a line chart", data=json.dumps(data))
```

## Examples
See `examples/chart_examples.py` for detailed usage examples.
