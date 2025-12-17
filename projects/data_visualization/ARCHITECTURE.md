# Data Visualization Agent - Architecture

## 📊 Project Structure
```
data_visualization/
├── README.md                      # Project documentation
├── ARCHITECTURE.md               # This file - how it works
├── __init__.py                   # Package initialization
├── agent.py                      # Main ChartAgent class
├── tools/                        # Visualization tools
│   ├── __init__.py
│   ├── data_analysis_tool.py    # Statistical analysis
│   └── chart_generator.py       # Chart creation
└── workflows/                    # Multi-chart workflows
    ├── __init__.py
    └── visualization_workflow.py # Dashboard creation
```

## 🔄 How It Works

### 1. User Provides Data + Question
```
User: "Analyze sales data and create visualizations"
   + CSV/JSON data or file path
   ↓
```

### 2. Request Goes to ChartAgent
```
data_visualization/agent.py
   ├── ChartAgent.__init__()
   │   ├── Loads system prompt: "You are a data analysis expert"
   │   ├── Registers 2 tools: DataAnalysis, ChartGenerator
   │   └── Connects to OpenAI API
   │
   └── ChartAgent.run(query, data)
       ├── Sends query + data + tools to GPT-4
       ├── LLM analyzes data patterns
       ├── LLM decides which charts to create
       └── Returns charts + insights
```

### 3. Tools Are Called (Based on LLM Decision)

#### First: Data Analysis
```
tools/data_analysis_tool.py
   └── DataAnalysisTool.execute(data)
       ├── Statistical analysis
       │   ├── Mean, median, std dev
       │   ├── Correlations
       │   └── Distributions
       ├── Pattern detection
       │   ├── Trends
       │   ├── Outliers
       │   └── Seasonality
       └── Returns insights
```

#### Then: Chart Generation
```
tools/chart_generator.py
   └── ChartGeneratorTool.execute(data, chart_type)
       │
       ├── LINE CHART
       │   ├── For: Time series, trends
       │   ├── Uses: matplotlib/plotly
       │   └── Saves: PNG file
       │
       ├── BAR CHART
       │   ├── For: Comparisons, categories
       │   ├── Options: Horizontal/Vertical
       │   └── Saves: PNG file
       │
       ├── SCATTER PLOT
       │   ├── For: Correlations, relationships
       │   ├── Options: Regression line
       │   └── Saves: PNG file
       │
       ├── PIE CHART
       │   ├── For: Proportions, percentages
       │   ├── Options: Explode slices
       │   └── Saves: PNG file
       │
       └── HEATMAP
           ├── For: Correlation matrix
           ├── Options: Color scheme
           └── Saves: PNG file
```

### 4. Workflow Orchestration (Optional)
```
workflows/visualization_workflow.py
   └── VisualizationWorkflow.analyze_and_visualize()
       │
       Step 1: Analyze data
       ├── agent.run("analyze this dataset")
       ├── Returns: Statistical insights
       │
       Step 2: Recommend chart types
       ├── Based on data characteristics
       ├── Time series? → Line chart
       ├── Categories? → Bar chart
       ├── Correlations? → Scatter + Heatmap
       │
       Step 3: Generate charts
       ├── Create all recommended charts
       ├── Add titles, labels, legends
       │
       Step 4: Create dashboard
       └── Combine charts into single view
```

### 5. Response Returns to User
```
   ↓
Result:
   ├── Chart files (PNG/HTML)
   ├── Statistical analysis
   ├── Key insights
   └── Recommendations
```

## 🎯 Data Flow Diagram

```
┌─────────┐
│  USER   │ Data + "Create visualizations"
└────┬────┘
     │
     ▼
┌──────────────────────────────────────────┐
│     ChartAgent (agent.py)                │
│                                          │
│  ┌───────────────────────────────┐      │
│  │   LLM Router (GPT-4)          │      │
│  │   - Analyzes data structure   │      │
│  │   - Identifies patterns       │      │
│  │   - Selects chart types       │      │
│  └──────────┬────────────────────┘      │
│             │                            │
│   ┌─────────┴──────────┐                │
│   │                    │                │
│   ▼                    ▼                │
│ ┌─────────┐      ┌──────────┐          │
│ │ Memory  │      │ Prompt   │          │
│ │ Previous│      │ Data     │          │
│ │ Charts  │      │ Context  │          │
│ └─────────┘      └──────────┘          │
│                                         │
│   ┌─────────────────────────────┐      │
│   │        Tools (2)            │      │
│   │                             │      │
│   │  📊 Data Analysis           │      │
│   │     ↓ Statistics            │      │
│   │     ↓ Patterns              │      │
│   │     ↓ Insights              │      │
│   │                             │      │
│   │  📈 Chart Generator         │      │
│   │     ↓ Line charts           │      │
│   │     ↓ Bar charts            │      │
│   │     ↓ Scatter plots         │      │
│   │     ↓ Pie charts            │      │
│   │     ↓ Heatmaps              │      │
│   └─────────────────────────────┘      │
└──────────────────────────────────────────┘
     │
     ▼
┌─────────┐
│ RESULT  │ Charts + Analysis
└─────────┘
```

## 🚀 Usage Examples

### Simple Visualization
```python
from projects.data_visualization.agent import ChartAgent
import pandas as pd

agent = ChartAgent()
data = pd.read_csv("sales_data.csv")
result = agent.run("Create a visualization showing sales trends", data)
```

**Flow:**
1. User provides data + query → ChartAgent
2. Agent → GPT-4 with data + tools
3. GPT-4 analyzes → Time series detected
4. GPT-4 decides → Use line chart
5. ChartGenerator → Creates chart
6. Result → Chart file + insights

### Dashboard Creation
```python
from projects.data_visualization.workflows.visualization_workflow import VisualizationWorkflow

workflow = VisualizationWorkflow()
dashboard = workflow.multi_chart_dashboard(
    data=sales_data,
    chart_types=["line", "bar", "pie"]
)
```

**Flow:**
1. Workflow receives data
2. Step 1: Analyze data structure
3. Step 2: Create line chart (trends)
4. Step 3: Create bar chart (comparisons)
5. Step 4: Create pie chart (proportions)
6. Step 5: Combine into dashboard
7. Result → Multi-panel dashboard

## 🔧 Key Components

### agent.py
- **Purpose:** Main agent class
- **Responsibilities:**
  - Initialize LLM connection
  - Register visualization tools
  - Handle data + queries
  - Coordinate chart creation
- **Key Methods:**
  - `__init__()`: Setup
  - `run(query, data)`: Create visualization
  - `_prepare_data()`: Data preprocessing

### tools/data_analysis_tool.py
- **Purpose:** Statistical analysis
- **Features:**
  - Descriptive statistics
  - Correlation analysis
  - Distribution analysis
  - Outlier detection
  - Trend identification
- **Returns:** JSON with insights

### tools/chart_generator.py
- **Purpose:** Chart creation
- **Supported Charts:**
  - Line: Time series, trends
  - Bar: Comparisons, categories
  - Scatter: Correlations
  - Pie: Proportions
  - Heatmap: Matrix data
- **Libraries:** matplotlib, seaborn, plotly
- **Output:** PNG/HTML files

### workflows/visualization_workflow.py
- **Purpose:** Complex visualizations
- **Features:**
  - Multi-chart dashboards
  - Time series analysis
  - Distribution analysis
  - Correlation analysis
  - Automatic chart selection

## 💡 When to Use What

| Data Type | Recommended Chart | Tool Flow |
|-----------|------------------|-----------|
| Time series | Line chart | Analyze → Line chart |
| Categories | Bar chart | Analyze → Bar chart |
| Proportions | Pie chart | Analyze → Pie chart |
| Two variables | Scatter plot | Analyze → Correlation → Scatter |
| Matrix data | Heatmap | Analyze → Correlation → Heatmap |
| Mixed data | Dashboard | Workflow → Multiple charts |

## 📈 Chart Selection Logic

```
Data Analysis
   ↓
┌──────────────────────────────┐
│ Data Characteristics:        │
│                              │
│ Has timestamp? → LINE CHART  │
│ Has categories? → BAR CHART  │
│ Has percentages? → PIE CHART │
│ Two numeric cols? → SCATTER  │
│ Multiple numeric? → HEATMAP  │
└──────────────────────────────┘
   ↓
LLM makes final decision
   ↓
ChartGenerator creates
```

## 🔍 Reflection & Self-Improvement

The Chart Agent evaluates visualization quality:

```python
# Reflect with visualization-specific criteria
reflection = agent.reflect(output, criteria=[
    "Appropriate chart type selection",
    "Clear explanation of visual reasoning",
    "Data characteristics considered",
    "Accessibility and readability",
    "Alternative options discussed"
])

print(f"Visualization Quality: {reflection['score']}/10")
```

### Example: Auto-Improving Chart Recommendations
```python
result = agent.run_with_reflection(
    "Best way to visualize quarterly sales?",
    data=sales_data,
    auto_improve=True
)

# Agent may suggest:
# Initial: Bar chart
# After reflection: Combo chart (bar + line) for better trend visibility
```

See [REFLECTION.md](../../REFLECTION.md) for more examples.

## 🎓 Technical Details

- **LLM:** OpenAI GPT-4
- **Tools:** 2 (DataAnalysis, ChartGenerator)
- **Libraries:** matplotlib, seaborn, plotly, pandas
- **Output Formats:** PNG, HTML (interactive)
- **Response Time:** 3-10 seconds per chart
- **Max Data Size:** 100k rows (configurable)
- **Chart Dimensions:** Customizable (default: 10x6 inches)
- **Reflection:** Visualization quality evaluation supported
