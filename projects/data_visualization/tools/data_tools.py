"""
Data & Visualization Tools
=========================
Tools for data analysis and chart generation.
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, Any, Optional
from core.tools.base_tool import BaseTool


class DataAnalysisTool(BaseTool):
    """
    Analyze data and provide statistics.
    
    Supports:
    - CSV, JSON data formats
    - Descriptive statistics
    - Data profiling
    """
    
    def __init__(self):
        super().__init__(
            name="data_analysis",
            description="Analyze data and provide statistics (mean, median, correlation, etc.)"
        )
    
    def execute(self, data: str, analysis_type: str = "summary") -> str:
        """
        Analyze data.
        
        Args:
            data: JSON string containing data (list of dicts or dict of lists)
            analysis_type: Type of analysis ("summary", "correlation", "distribution")
            
        Returns:
            JSON string with analysis results
        """
        try:
            # Parse data
            data_dict = json.loads(data)
            df = pd.DataFrame(data_dict)
            
            if df.empty:
                return self.format_error("Empty dataset provided")
            
            results = {}
            
            if analysis_type == "summary":
                # Basic statistics
                results["shape"] = {"rows": len(df), "columns": len(df.columns)}
                results["columns"] = list(df.columns)
                results["dtypes"] = df.dtypes.astype(str).to_dict()
                
                # Numeric columns statistics
                numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                if numeric_cols:
                    results["numeric_summary"] = df[numeric_cols].describe().to_dict()
                
                # Missing values
                results["missing_values"] = df.isnull().sum().to_dict()
                
            elif analysis_type == "correlation":
                # Correlation matrix for numeric columns
                numeric_df = df.select_dtypes(include=['number'])
                if numeric_df.empty:
                    return self.format_error("No numeric columns found for correlation")
                results["correlation"] = numeric_df.corr().to_dict()
                
            elif analysis_type == "distribution":
                # Distribution statistics
                numeric_df = df.select_dtypes(include=['number'])
                if numeric_df.empty:
                    return self.format_error("No numeric columns found for distribution analysis")
                
                for col in numeric_df.columns:
                    results[col] = {
                        "mean": float(numeric_df[col].mean()),
                        "median": float(numeric_df[col].median()),
                        "std": float(numeric_df[col].std()),
                        "min": float(numeric_df[col].min()),
                        "max": float(numeric_df[col].max()),
                        "quartiles": {
                            "q1": float(numeric_df[col].quantile(0.25)),
                            "q2": float(numeric_df[col].quantile(0.50)),
                            "q3": float(numeric_df[col].quantile(0.75))
                        }
                    }
            else:
                return self.format_error(f"Unknown analysis type: {analysis_type}")
            
            return self.format_success(results, analysis_type=analysis_type)
            
        except json.JSONDecodeError as e:
            return self.format_error(f"Invalid JSON data: {str(e)}")
        except Exception as e:
            return self.format_error(str(e))
    
    @property
    def tool_definition(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "data": {
                            "type": "string",
                            "description": "JSON string containing the data to analyze. Can be list of dicts or dict of lists."
                        },
                        "analysis_type": {
                            "type": "string",
                            "enum": ["summary", "correlation", "distribution"],
                            "description": "Type of analysis to perform: 'summary' for basic stats, 'correlation' for correlation matrix, 'distribution' for distribution statistics"
                        }
                    },
                    "required": ["data"]
                }
            }
        }


class ChartGenerationTool(BaseTool):
    """
    Generate charts and visualizations.
    
    Supports:
    - Line charts
    - Bar charts
    - Scatter plots
    - Pie charts
    - Heatmaps
    """
    
    def __init__(self, output_dir: str = "./outputs/charts"):
        super().__init__(
            name="generate_chart",
            description="Generate and save charts/visualizations from data"
        )
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set style
        sns.set_theme(style="whitegrid")
        plt.rcParams['figure.figsize'] = (10, 6)
    
    def execute(
        self,
        data: str,
        chart_type: str,
        x_column: Optional[str] = None,
        y_column: Optional[str] = None,
        title: Optional[str] = None,
        filename: Optional[str] = None
    ) -> str:
        """
        Generate a chart.
        
        Args:
            data: JSON string containing data
            chart_type: Type of chart ("line", "bar", "scatter", "pie", "heatmap")
            x_column: Column name for x-axis
            y_column: Column name for y-axis (or values for pie)
            title: Chart title
            filename: Output filename (without extension)
            
        Returns:
            JSON string with chart path
        """
        try:
            # Parse data
            data_dict = json.loads(data)
            df = pd.DataFrame(data_dict)
            
            if df.empty:
                return self.format_error("Empty dataset provided")
            
            # Generate filename if not provided
            if not filename:
                from datetime import datetime
                filename = f"chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create figure
            plt.figure(figsize=(10, 6))
            
            # Generate chart based on type
            if chart_type == "line":
                if not x_column or not y_column:
                    return self.format_error("Line chart requires x_column and y_column")
                plt.plot(df[x_column], df[y_column], marker='o')
                plt.xlabel(x_column)
                plt.ylabel(y_column)
                
            elif chart_type == "bar":
                if not x_column or not y_column:
                    return self.format_error("Bar chart requires x_column and y_column")
                plt.bar(df[x_column], df[y_column])
                plt.xlabel(x_column)
                plt.ylabel(y_column)
                plt.xticks(rotation=45, ha='right')
                
            elif chart_type == "scatter":
                if not x_column or not y_column:
                    return self.format_error("Scatter plot requires x_column and y_column")
                plt.scatter(df[x_column], df[y_column], alpha=0.6)
                plt.xlabel(x_column)
                plt.ylabel(y_column)
                
            elif chart_type == "pie":
                if not x_column or not y_column:
                    return self.format_error("Pie chart requires x_column (labels) and y_column (values)")
                plt.pie(df[y_column], labels=df[x_column], autopct='%1.1f%%', startangle=90)
                plt.axis('equal')
                
            elif chart_type == "heatmap":
                # For heatmap, use correlation matrix or provided data
                numeric_df = df.select_dtypes(include=['number'])
                if numeric_df.empty:
                    return self.format_error("No numeric columns found for heatmap")
                
                correlation = numeric_df.corr()
                sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0)
                
            else:
                return self.format_error(f"Unknown chart type: {chart_type}")
            
            # Set title
            if title:
                plt.title(title)
            
            # Save chart
            output_path = self.output_dir / f"{filename}.png"
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            return self.format_success(
                {"chart_path": str(output_path)},
                chart_type=chart_type,
                filename=filename
            )
            
        except json.JSONDecodeError as e:
            return self.format_error(f"Invalid JSON data: {str(e)}")
        except KeyError as e:
            return self.format_error(f"Column not found: {str(e)}")
        except Exception as e:
            return self.format_error(str(e))
    
    @property
    def tool_definition(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "data": {
                            "type": "string",
                            "description": "JSON string containing the data to visualize"
                        },
                        "chart_type": {
                            "type": "string",
                            "enum": ["line", "bar", "scatter", "pie", "heatmap"],
                            "description": "Type of chart to generate"
                        },
                        "x_column": {
                            "type": "string",
                            "description": "Column name for x-axis (or labels for pie chart)"
                        },
                        "y_column": {
                            "type": "string",
                            "description": "Column name for y-axis (or values for pie chart)"
                        },
                        "title": {
                            "type": "string",
                            "description": "Chart title"
                        },
                        "filename": {
                            "type": "string",
                            "description": "Output filename without extension"
                        }
                    },
                    "required": ["data", "chart_type"]
                }
            }
        }


# Singleton instances
data_analysis_tool = DataAnalysisTool()
chart_generation_tool = ChartGenerationTool()

# Registry
DATA_TOOLS = {
    "data_analysis": data_analysis_tool.tool_definition,
    "generate_chart": chart_generation_tool.tool_definition
}


def get_data_tool_definitions() -> list:
    """Get all data tool definitions for LLM."""
    return list(DATA_TOOLS.values())
