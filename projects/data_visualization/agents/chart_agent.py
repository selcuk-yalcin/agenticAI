"""
Chart Agent
===========
Agent specialized in data analysis and visualization.
"""

from typing import Optional, Tuple, List, Dict, Any
from core.agents.base_agent import BaseAgent
from projects.data_visualization.tools.data_tools import (
    data_analysis_tool,
    chart_generation_tool,
    get_data_tool_definitions
)


class ChartAgent(BaseAgent):
    """
    Chart generation agent for data visualization.
    
    Capabilities:
    - Data analysis (statistics, correlation, distribution)
    - Chart generation (line, bar, scatter, pie, heatmap)
    - Automatic chart type selection
    - Multi-chart reports
    """
    
    SYSTEM_PROMPT = """You are a data visualization expert specializing in creating insightful charts and graphs.

Your capabilities:
1. Analyze data to understand structure and patterns
2. Generate various types of charts (line, bar, scatter, pie, heatmap)
3. Select appropriate chart types based on data characteristics
4. Create clear, informative visualizations

Your process:
1. First, analyze the data using data_analysis tool to understand:
   - Data structure (columns, types, shape)
   - Statistical properties (mean, median, distribution)
   - Relationships (correlation)
2. Based on analysis, select appropriate chart type:
   - Line charts: for trends over time
   - Bar charts: for categorical comparisons
   - Scatter plots: for relationships between variables
   - Pie charts: for proportions/percentages
   - Heatmaps: for correlation matrices
3. Generate charts with clear titles and labels
4. Provide insights about the visualizations

Guidelines:
- Always analyze data before generating charts
- Choose chart types that best represent the data
- Use descriptive titles and labels
- Provide interpretation of the visualizations
- Generate multiple charts if needed for comprehensive analysis
- Save charts with meaningful filenames

Data format:
- Input data should be in JSON format
- List of dicts: [{"col1": val1, "col2": val2}, ...]
- Or dict of lists: {"col1": [val1, val2, ...], "col2": [...]}
"""
    
    def __init__(
        self,
        model: Optional[str] = None,
        temperature: float = 0.0,
        output_dir: str = "./outputs/charts"
    ):
        """
        Initialize chart agent.
        
        Args:
            model: LLM model to use
            temperature: Sampling temperature
            output_dir: Directory for saving charts
        """
        super().__init__(
            name="ChartAgent",
            system_prompt=self.SYSTEM_PROMPT,
            model=model,
            temperature=temperature
        )
        
        self.output_dir = output_dir
        
        # Add data tools
        data_tools = get_data_tool_definitions()
        self.add_tools(data_tools, {
            "data_analysis": data_analysis_tool,
            "generate_chart": chart_generation_tool
        })
    
    def run(
        self,
        query: str,
        data: Optional[str] = None,
        max_turns: Optional[int] = None,
        return_tool_log: bool = False
    ):
        """
        Generate charts based on query and data.
        
        Args:
            query: User's visualization request
            data: JSON string containing data (optional, can be in query)
            max_turns: Maximum tool calling iterations
            return_tool_log: If True, return (response, tool_log) tuple
            
        Returns:
            Visualization report (or tuple with tool log if return_tool_log=True)
        """
        # Append data to query if provided
        if data:
            full_query = f"{query}\n\nData:\n{data}"
        else:
            full_query = query
        
        response, tool_log = self._execute_with_tools(full_query, max_turns)
        
        if return_tool_log:
            return response, tool_log
        return response
    
    def create_dashboard(
        self,
        data: str,
        title: str = "Data Dashboard",
        description: Optional[str] = None
    ) -> str:
        """
        Create a comprehensive dashboard with multiple visualizations.
        
        Args:
            data: JSON string containing data
            title: Dashboard title
            description: Optional description of the data
            
        Returns:
            Dashboard report with multiple charts
        """
        self.reset()
        
        prompt = f"""Create a comprehensive data dashboard with the title: "{title}"
{f'Description: {description}' if description else ''}

Please:
1. First analyze the data thoroughly
2. Generate multiple appropriate charts to show different aspects:
   - Overview/summary statistics
   - Trends (if time series data)
   - Comparisons (if categorical data)
   - Relationships/correlations (if multiple numeric variables)
   - Distribution (if relevant)
3. Provide insights for each visualization
4. Suggest what the data reveals

Data:
{data}"""
        
        return self.run(prompt)
    
    def analyze_and_visualize(
        self,
        data: str,
        focus: Optional[str] = None
    ) -> str:
        """
        Analyze data and create focused visualizations.
        
        Args:
            data: JSON string containing data
            focus: Optional focus area (e.g., "trends", "correlation", "distribution")
            
        Returns:
            Analysis report with visualizations
        """
        self.reset()
        
        focus_text = f" with focus on {focus}" if focus else ""
        prompt = f"""Analyze this data{focus_text} and create appropriate visualizations.

Steps:
1. Analyze the data structure and statistics
2. Identify key patterns and insights
3. Generate relevant charts
4. Provide interpretation

Data:
{data}"""
        
        return self.run(prompt)
    
    def compare_datasets(
        self,
        dataset1: str,
        dataset2: str,
        label1: str = "Dataset 1",
        label2: str = "Dataset 2"
    ) -> str:
        """
        Compare two datasets with visualizations.
        
        Args:
            dataset1: First dataset (JSON string)
            dataset2: Second dataset (JSON string)
            label1: Label for first dataset
            label2: Label for second dataset
            
        Returns:
            Comparison report with charts
        """
        self.reset()
        
        prompt = f"""Compare these two datasets and create comparison visualizations.

{label1}:
{dataset1}

{label2}:
{dataset2}

Please:
1. Analyze both datasets separately
2. Identify similarities and differences
3. Create comparative visualizations
4. Provide insights on the comparison"""
        
        return self.run(prompt)


# Convenience function
def create_chart_agent(
    model: Optional[str] = None,
    **kwargs
) -> ChartAgent:
    """
    Create a chart agent with default settings.
    
    Args:
        model: LLM model to use
        **kwargs: Additional arguments for ChartAgent
        
    Returns:
        Configured ChartAgent instance
    """
    return ChartAgent(model=model, **kwargs)
