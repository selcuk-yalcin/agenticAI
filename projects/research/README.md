# Research Project

## Overview
AI-powered research agents that can gather information from multiple sources and synthesize findings.

## Agents
- **ResearchAgent**: Conducts research using web search and academic tools

## Tools
- **tavily_search_tool**: Web search via Tavily API
- **wikipedia_search_tool**: Wikipedia encyclopedia search
- **arxiv_search_tool**: Academic paper search

## Usage
```python
from projects.research import ResearchAgent

agent = ResearchAgent()
result = agent.run("What are the latest AI trends?")
print(result)
```

## Examples
See `examples/` directory for detailed usage examples.
