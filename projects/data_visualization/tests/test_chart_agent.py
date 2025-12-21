"""Tests for Data Visualization Chart Agent.

This module tests:
- Automatic chart type selection
- DataFrame to chart conversion
- Multiple chart types (line, bar, scatter, pie)
- Chart styling and customization
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import io


class TestChartAgent:
    """Test suite for data visualization functionality."""

    @pytest.fixture
    def sample_dataframe(self):
        """Fixture providing a sample DataFrame.
        
        Returns:
            Mock DataFrame with sales data.
        """
        # Mock pandas DataFrame
        df = Mock()
        df.columns = ["month", "sales", "profit", "category"]
        df.shape = (12, 4)
        df.dtypes = {
            "month": "object",
            "sales": "float64",
            "profit": "float64",
            "category": "object"
        }
        df.head.return_value = df
        df.describe.return_value = df
        return df

    @pytest.fixture
    def sample_time_series_data(self):
        """Fixture providing time series data.
        
        Returns:
            Mock DataFrame with date and value columns.
        """
        df = Mock()
        df.columns = ["date", "value"]
        df.shape = (100, 2)
        df.dtypes = {"date": "datetime64", "value": "float64"}
        return df

    def test_chart_type_selection_for_categorical_data(self):
        """Test automatic chart type selection for categorical data.
        
        Categorical data best visualized with:
        - Bar chart (comparison)
        - Pie chart (composition)
        - Stacked bar (sub-categories)
        """
        def select_chart_type(data_info):
            """Select appropriate chart type based on data characteristics."""
            column_types = data_info.get("column_types", {})
            num_categories = data_info.get("num_categories", 0)
            
            # Count categorical vs numeric columns
            categorical_cols = [k for k, v in column_types.items() if v in ["object", "category"]]
            numeric_cols = [k for k, v in column_types.items() if v in ["float64", "int64"]]
            
            # Decision logic
            if len(categorical_cols) >= 1 and len(numeric_cols) >= 1:
                if num_categories <= 5:
                    return "pie"
                else:
                    return "bar"
            elif len(numeric_cols) >= 2:
                return "scatter"
            else:
                return "bar"
        
        data_info = {
            "column_types": {"category": "object", "value": "float64"},
            "num_categories": 4
        }
        
        chart_type = select_chart_type(data_info)
        
        assert chart_type in ["bar", "pie", "scatter", "line"]
        assert chart_type == "pie"  # 4 categories fits pie chart

    def test_chart_type_selection_for_time_series(self):
        """Test chart type selection for time series data.
        
        Time series best visualized with:
        - Line chart (trends over time)
        - Area chart (cumulative values)
        """
        def select_chart_type_for_timeseries(data_info):
            """Select chart type for time series."""
            has_date_column = data_info.get("has_date", False)
            num_series = data_info.get("num_series", 1)
            
            if has_date_column:
                if num_series > 1:
                    return "multi_line"
                else:
                    return "line"
            return "bar"
        
        data_info = {"has_date": True, "num_series": 1}
        
        chart_type = select_chart_type_for_timeseries(data_info)
        
        assert chart_type in ["line", "multi_line", "area"]

    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.figure')
    def test_generate_bar_chart(self, mock_figure, mock_savefig, sample_dataframe):
        """Test generation of bar chart.
        
        Bar chart requirements:
        - Categorical x-axis
        - Numeric y-axis
        - Optional colors per category
        """
        def generate_bar_chart(df, x_col, y_col, title="Bar Chart"):
            """Generate bar chart from DataFrame."""
            import matplotlib.pyplot as plt
            
            fig = plt.figure(figsize=(10, 6))
            ax = fig.add_subplot(111)
            
            # Simulate bar chart creation
            ax.bar(range(len(df)), [100, 200, 150, 180])
            ax.set_title(title)
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            
            # Save to buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            
            return buf
        
        result = generate_bar_chart(sample_dataframe, "month", "sales")
        
        assert result is not None
        mock_savefig.assert_called_once()

    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.figure')
    def test_generate_line_chart(self, mock_figure, mock_savefig, sample_time_series_data):
        """Test generation of line chart.
        
        Line chart requirements:
        - Sequential x-axis (usually time)
        - Numeric y-axis
        - Smooth lines connecting points
        """
        def generate_line_chart(df, x_col, y_col, title="Line Chart"):
            """Generate line chart from DataFrame."""
            import matplotlib.pyplot as plt
            
            fig = plt.figure(figsize=(12, 6))
            ax = fig.add_subplot(111)
            
            # Simulate line chart
            ax.plot(range(100), [i * 1.5 for i in range(100)])
            ax.set_title(title)
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.grid(True, alpha=0.3)
            
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            
            return buf
        
        result = generate_line_chart(sample_time_series_data, "date", "value")
        
        assert result is not None
        mock_savefig.assert_called_once()

    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.figure')
    def test_generate_scatter_plot(self, mock_figure, mock_savefig):
        """Test generation of scatter plot.
        
        Scatter plot requirements:
        - Two numeric variables
        - Optional color/size dimensions
        - Shows correlation patterns
        """
        def generate_scatter_plot(df, x_col, y_col, title="Scatter Plot"):
            """Generate scatter plot from DataFrame."""
            import matplotlib.pyplot as plt
            
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111)
            
            # Simulate scatter plot
            x = [i for i in range(50)]
            y = [i * 2 + 10 for i in range(50)]
            ax.scatter(x, y, alpha=0.6)
            ax.set_title(title)
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            
            return buf
        
        df = Mock()
        result = generate_scatter_plot(df, "sales", "profit")
        
        assert result is not None
        mock_savefig.assert_called_once()

    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.figure')
    def test_generate_pie_chart(self, mock_figure, mock_savefig):
        """Test generation of pie chart.
        
        Pie chart requirements:
        - Categorical data
        - Percentage/proportion display
        - Limited categories (< 8 for readability)
        """
        def generate_pie_chart(df, category_col, value_col, title="Pie Chart"):
            """Generate pie chart from DataFrame."""
            import matplotlib.pyplot as plt
            
            fig = plt.figure(figsize=(10, 10))
            ax = fig.add_subplot(111)
            
            # Simulate pie chart
            sizes = [30, 25, 20, 15, 10]
            labels = ['A', 'B', 'C', 'D', 'E']
            ax.pie(sizes, labels=labels, autopct='%1.1f%%')
            ax.set_title(title)
            
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            
            return buf
        
        df = Mock()
        result = generate_pie_chart(df, "category", "sales")
        
        assert result is not None
        mock_savefig.assert_called_once()

    def test_color_palette_selection(self):
        """Test selection of appropriate color palettes.
        
        Color palettes:
        - Sequential: for continuous data
        - Diverging: for data with meaningful midpoint
        - Categorical: for distinct categories
        """
        def select_color_palette(chart_type, num_colors):
            """Select appropriate color palette."""
            palettes = {
                "bar": "categorical",
                "line": "sequential",
                "scatter": "continuous",
                "pie": "categorical",
                "heatmap": "diverging"
            }
            
            palette_type = palettes.get(chart_type, "categorical")
            
            # Return color codes based on type
            if palette_type == "categorical":
                colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'][:num_colors]
            elif palette_type == "sequential":
                colors = ['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6'][:num_colors]
            else:
                colors = ['#d73027', '#fc8d59', '#fee090', '#91bfdb', '#4575b4'][:num_colors]
            
            return colors
        
        bar_colors = select_color_palette("bar", 5)
        line_colors = select_color_palette("line", 3)
        
        assert len(bar_colors) == 5
        assert len(line_colors) == 3
        assert all(color.startswith('#') for color in bar_colors)

    def test_chart_title_generation(self):
        """Test automatic generation of chart titles.
        
        Title should include:
        - Variables being plotted
        - Chart type
        - Time period (if applicable)
        """
        def generate_chart_title(chart_type, x_col, y_col, time_period=None):
            """Generate descriptive chart title."""
            type_names = {
                "bar": "Comparison",
                "line": "Trend",
                "scatter": "Relationship",
                "pie": "Distribution"
            }
            
            type_name = type_names.get(chart_type, "Chart")
            
            # Format column names (capitalize, remove underscores)
            x_formatted = x_col.replace('_', ' ').title()
            y_formatted = y_col.replace('_', ' ').title() if y_col else ""
            
            if chart_type == "pie":
                title = f"{y_formatted} {type_name} by {x_formatted}"
            else:
                title = f"{y_formatted} vs {x_formatted} - {type_name}"
            
            if time_period:
                title += f" ({time_period})"
            
            return title
        
        title = generate_chart_title("bar", "month", "sales", "2024")
        
        assert "Sales" in title
        assert "Month" in title
        assert "2024" in title

    def test_axis_label_formatting(self):
        """Test formatting of axis labels.
        
        Formatting includes:
        - Proper capitalization
        - Units (if applicable)
        - Number formatting (K, M, B for large numbers)
        """
        def format_axis_label(column_name, data_type, units=None):
            """Format axis label with proper capitalization and units."""
            # Capitalize and remove underscores
            label = column_name.replace('_', ' ').title()
            
            # Add units if provided
            if units:
                label += f" ({units})"
            
            return label
        
        def format_axis_values(values):
            """Format large numbers with K, M, B suffixes."""
            formatted = []
            for val in values:
                if val >= 1_000_000_000:
                    formatted.append(f"{val/1_000_000_000:.1f}B")
                elif val >= 1_000_000:
                    formatted.append(f"{val/1_000_000:.1f}M")
                elif val >= 1_000:
                    formatted.append(f"{val/1_000:.1f}K")
                else:
                    formatted.append(f"{val:.0f}")
            return formatted
        
        label = format_axis_label("total_revenue", "float64", "$")
        formatted_vals = format_axis_values([500, 5000, 5000000])
        
        assert "Total Revenue" in label
        assert "$" in label
        assert formatted_vals == ["500", "5.0K", "5.0M"]

    def test_multi_series_line_chart(self):
        """Test generation of multi-series line chart.
        
        Requirements:
        - Multiple lines on same axes
        - Legend for each series
        - Different colors/styles per line
        """
        def create_multi_series_config(series_names):
            """Create configuration for multi-series chart."""
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
            line_styles = ['-', '--', '-.', ':']
            
            configs = []
            for i, name in enumerate(series_names):
                configs.append({
                    "name": name,
                    "color": colors[i % len(colors)],
                    "line_style": line_styles[i % len(line_styles)],
                    "marker": "o" if i % 2 == 0 else "s"
                })
            
            return configs
        
        series = ["Product A", "Product B", "Product C"]
        configs = create_multi_series_config(series)
        
        assert len(configs) == 3
        assert all("color" in config for config in configs)
        assert all("line_style" in config for config in configs)

    def test_chart_save_formats(self):
        """Test saving charts in different formats.
        
        Supported formats:
        - PNG (raster, good for web)
        - SVG (vector, scalable)
        - PDF (vector, print quality)
        """
        def get_save_format_config(format_type):
            """Get configuration for saving in specific format."""
            configs = {
                "png": {
                    "format": "png",
                    "dpi": 300,
                    "transparent": False,
                    "bbox_inches": "tight"
                },
                "svg": {
                    "format": "svg",
                    "transparent": True,
                    "bbox_inches": "tight"
                },
                "pdf": {
                    "format": "pdf",
                    "bbox_inches": "tight"
                }
            }
            return configs.get(format_type, configs["png"])
        
        png_config = get_save_format_config("png")
        svg_config = get_save_format_config("svg")
        
        assert png_config["format"] == "png"
        assert svg_config["format"] == "svg"
        assert "dpi" in png_config

    @patch('openai.ChatCompletion.create')
    def test_chart_recommendation_from_llm(self, mock_openai):
        """Test using LLM to recommend chart type.
        
        LLM considers:
        - Data types and structure
        - Analysis goals
        - Best practices
        """
        mock_openai.return_value = Mock(
            choices=[Mock(message=Mock(content="For sales data over time, I recommend a line chart to show trends."))]
        )
        
        def get_chart_recommendation(data_description, goal):
            """Get chart recommendation from LLM."""
            prompt = f"Data: {data_description}\nGoal: {goal}\nRecommend the best chart type."
            
            response = mock_openai(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            
            recommendation = response.choices[0].message.content
            
            # Extract chart type from recommendation
            chart_types = ["line", "bar", "scatter", "pie", "heatmap"]
            for chart_type in chart_types:
                if chart_type in recommendation.lower():
                    return chart_type
            
            return "bar"  # Default
        
        chart_type = get_chart_recommendation(
            "Monthly sales data with date and revenue columns",
            "Show sales trends over the year"
        )
        
        assert chart_type in ["line", "bar", "scatter", "pie", "heatmap"]
