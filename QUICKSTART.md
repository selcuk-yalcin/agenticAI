# Quick Start Guide

Get up and running in 5 minutes.

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your keys
```

## Basic Usage

### Research Agent

```python
from projects.research import ResearchAgent

agent = ResearchAgent()
result = agent.run("What are the latest developments in quantum computing?")
print(result)
```

### Chart Agent

```python
from projects.data_visualization import ChartAgent
import json

agent = ChartAgent()
data = {
    "month": ["Jan", "Feb", "Mar", "Apr", "May"],
    "sales": [12000, 15000, 13500, 18000, 21000]
}

result = agent.run(
    query="Create a line chart showing sales trends",
    data=json.dumps(data)
)
print(result)
```

## Advanced Examples

### Deep Research

```python
from projects.research import ResearchAgent

agent = ResearchAgent()
report = agent.deep_research(
    topic="Impact of AI on healthcare",
    max_turns_per_question=3
)
```

### Dashboard Creation

```python
from projects.data_visualization import ChartAgent
import json

agent = ChartAgent()
data = {"temperature": [20, 25, 30], "sales": [150, 220, 320]}

dashboard = agent.create_dashboard(
    data=json.dumps(data),
    title="Temperature & Sales Analysis"
)
```

## Configuration

### Environment Variables

```bash
# .env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
TAVILY_API_KEY=tvly-...
```

### Config File

```yaml
# config/config.yaml
llm:
  default_model: "gpt-4-turbo-preview"
  temperature: 0.0
```

## Available Projects

### Research
- **Tools:** Tavily, Wikipedia, arXiv
- **Example:** `from projects.research import ResearchAgent`

### Data Visualization
- **Tools:** Data analysis, 5 chart types
- **Example:** `from projects.data_visualization import ChartAgent`

## Common Tasks

### Save Output

```python
from core.utils import save_markdown

save_markdown(content, "report", "./outputs/research")
```

### Multiple Charts

```python
agent.run("""Create THREE charts:
1. Bar chart of sales
2. Scatter plot of correlation
3. Pie chart of distribution
""", data=json.dumps(data))
```

## Troubleshooting

**API Key Error:** Add to `.env` file

**Import Error:** Run from `Agents/` directory  

**No Charts:** Check data format and permissions

## Next Steps

- Read [STRUCTURE.md](STRUCTURE.md)
- Check [CHART_AGENT.md](CHART_AGENT.md)
- Run examples: `python projects/data_visualization/examples/chart_examples.py`
