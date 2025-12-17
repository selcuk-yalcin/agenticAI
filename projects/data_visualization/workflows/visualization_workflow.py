"""
Data Visualization Workflow
Multi-step data analysis and visualization pipeline
"""

from typing import Dict, Any, List, Optional
import json
from ..agents.chart_agent import ChartAgent


class VisualizationWorkflow:
    """Orchestrates data analysis and visualization tasks."""
    
    def __init__(self):
        self.agent = ChartAgent()
        self.visualizations = []
    
    def analyze_and_visualize(
        self,
        data: Dict[str, Any],
        description: str = "Analyze and visualize this data"
    ) -> Dict[str, Any]:
        """
        Complete workflow: analyze data and create appropriate visualizations.
        
        Args:
            data: Data to analyze and visualize
            description: What to analyze
        
        Returns:
            Analysis results and visualization paths
        """
        print("Step 1: Analyzing data...")
        analysis = self.agent.analyze_data(data)
        
        print("Step 2: Creating visualization...")
        chart_type = self._suggest_chart_type(data, analysis)
        
        visualization = self.agent.run(
            f"Create a {chart_type} chart: {description}",
            data=json.dumps(data)
        )
        
        result = {
            "analysis": analysis,
            "visualization": visualization,
            "chart_type": chart_type
        }
        
        self.visualizations.append(result)
        return result
    
    def multi_chart_dashboard(
        self,
        datasets: List[Dict[str, Any]],
        chart_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create multiple visualizations from different datasets.
        
        Args:
            datasets: List of datasets to visualize
            chart_types: Specific chart types (or auto-suggest)
        
        Returns:
            Dictionary of all created charts
        """
        print(f"Creating dashboard with {len(datasets)} visualizations...")
        
        charts = []
        for i, dataset in enumerate(datasets):
            chart_type = (
                chart_types[i] if chart_types and i < len(chart_types)
                else self._suggest_chart_type(dataset)
            )
            
            print(f"Chart {i+1}: Creating {chart_type}...")
            result = self.agent.run(
                f"Create {chart_type} chart",
                data=json.dumps(dataset)
            )
            
            charts.append({
                "index": i + 1,
                "chart_type": chart_type,
                "data": dataset,
                "output": result
            })
        
        return {
            "total_charts": len(charts),
            "charts": charts
        }
    
    def comparative_visualization(
        self,
        datasets: Dict[str, Dict[str, Any]],
        comparison_type: str = "side_by_side"
    ) -> Dict[str, Any]:
        """
        Create comparative visualizations.
        
        Args:
            datasets: Dictionary of named datasets
            comparison_type: How to compare (side_by_side, overlaid)
        
        Returns:
            Comparative visualization results
        """
        print(f"Creating comparative visualization for {len(datasets)} datasets...")
        
        visualizations = {}
        for name, data in datasets.items():
            print(f"Visualizing: {name}")
            result = self.agent.run(
                f"Create chart for {name}",
                data=json.dumps(data)
            )
            visualizations[name] = result
        
        # Create comparison summary
        comparison_prompt = f"""Compare these {len(datasets)} datasets:
        
Datasets: {', '.join(datasets.keys())}
Comparison Type: {comparison_type}

Provide insights on differences, similarities, and patterns."""
        
        comparison_analysis = self.agent.run(comparison_prompt)
        
        return {
            "datasets": list(datasets.keys()),
            "comparison_type": comparison_type,
            "visualizations": visualizations,
            "comparison_analysis": comparison_analysis
        }
    
    def time_series_analysis(
        self,
        data: Dict[str, Any],
        time_column: str = "date",
        value_columns: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Analyze and visualize time series data.
        
        Args:
            data: Time series data
            time_column: Name of time column
            value_columns: Columns to plot
        
        Returns:
            Time series analysis and visualization
        """
        print("Analyzing time series data...")
        
        # Analyze trends
        analysis = self.agent.analyze_data(data)
        
        # Create time series chart
        chart = self.agent.run(
            f"Create line chart showing trends over {time_column}",
            data=json.dumps(data)
        )
        
        # Statistical analysis
        stats_prompt = f"""Analyze time series patterns:

Data has {len(data.get(time_column, []))} time points
Value columns: {value_columns or 'all numeric columns'}

Identify:
1. Overall trend (increasing, decreasing, stable)
2. Seasonality patterns
3. Anomalies or outliers
4. Growth rate
5. Forecast direction"""
        
        stats_analysis = self.agent.run(stats_prompt)
        
        return {
            "time_column": time_column,
            "analysis": analysis,
            "chart": chart,
            "statistical_analysis": stats_analysis
        }
    
    def distribution_analysis(
        self,
        data: Dict[str, Any],
        column: str
    ) -> Dict[str, Any]:
        """
        Analyze distribution of values in a column.
        
        Args:
            data: Dataset
            column: Column to analyze
        
        Returns:
            Distribution analysis and visualization
        """
        print(f"Analyzing distribution of {column}...")
        
        # Create histogram/distribution chart
        chart = self.agent.run(
            f"Create bar chart showing distribution of {column}",
            data=json.dumps(data)
        )
        
        # Statistical analysis
        values = data.get(column, [])
        stats_prompt = f"""Analyze distribution of {column}:

Sample size: {len(values)}
Values: {values[:10]}... (showing first 10)

Provide:
1. Central tendency (mean, median)
2. Spread (range, variance)
3. Shape (normal, skewed, bimodal)
4. Outliers
5. Key insights"""
        
        stats = self.agent.run(stats_prompt)
        
        return {
            "column": column,
            "chart": chart,
            "statistics": stats
        }
    
    def correlation_analysis(
        self,
        data: Dict[str, Any],
        variables: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Analyze correlations between variables.
        
        Args:
            data: Dataset
            variables: Variables to correlate (or all numeric)
        
        Returns:
            Correlation analysis and heatmap
        """
        print("Analyzing correlations...")
        
        # Create correlation heatmap
        chart = self.agent.run(
            "Create heatmap showing correlations between variables",
            data=json.dumps(data)
        )
        
        # Correlation insights
        corr_prompt = f"""Analyze correlations in the data:

Variables: {variables or 'all numeric columns'}

Identify:
1. Strong positive correlations
2. Strong negative correlations
3. Weak or no correlations
4. Potential causation vs correlation
5. Actionable insights"""
        
        insights = self.agent.run(corr_prompt)
        
        return {
            "variables": variables,
            "heatmap": chart,
            "insights": insights
        }
    
    def _suggest_chart_type(
        self,
        data: Dict[str, Any],
        analysis: Optional[str] = None
    ) -> str:
        """Suggest appropriate chart type based on data."""
        keys = list(data.keys())
        
        # Check for time series
        time_keywords = ['date', 'time', 'month', 'year', 'day']
        if any(keyword in k.lower() for k in keys for keyword in time_keywords):
            return "line"
        
        # Check for categories
        if len(keys) == 2:
            first_col = data[keys[0]]
            if isinstance(first_col, list) and len(first_col) < 10:
                return "bar"
        
        # Check for multiple series
        if len(keys) > 2:
            return "line"
        
        return "bar"  # Default
    
    def get_visualization_history(self) -> List[Dict[str, Any]]:
        """Get all visualizations created in this session."""
        return self.visualizations


def create_visualization_workflow() -> VisualizationWorkflow:
    """Factory function to create a VisualizationWorkflow."""
    return VisualizationWorkflow()
