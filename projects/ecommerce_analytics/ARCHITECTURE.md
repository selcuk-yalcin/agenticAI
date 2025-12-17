# E-commerce Analytics Agent - Architecture

## 📊 Project Structure
```
ecommerce_analytics/
├── README.md                        # Project documentation
├── ARCHITECTURE.md                 # This file - how it works
├── __init__.py                     # Package initialization
├── agent.py                        # Main AnalyticsAgent class
├── tools/                          # Analytics tools
│   ├── __init__.py
│   ├── sales_analyzer.py          # Sales metrics & trends
│   ├── customer_segmentation.py   # Customer behavior analysis
│   ├── product_analyzer.py        # Product performance
│   └── forecasting_tool.py        # Predictive analytics
└── workflows/                      # Analytics workflows
    ├── __init__.py
    └── analytics_workflow.py      # Business intelligence flows
```

## 🔄 How It Works

### 1. Business Question Arrives
```
Manager: "What are our best selling products this quarter?"
   + Sales data (CSV/Database)
   + Date range
   + Optional filters
   ↓
```

### 2. Request Goes to AnalyticsAgent
```
ecommerce_analytics/agent.py
   ├── AnalyticsAgent.__init__()
   │   ├── Loads system prompt: "You are a data analyst expert"
   │   ├── Registers 4 tools: Sales, Customer, Product, Forecasting
   │   └── Connects to OpenAI API
   │
   └── AnalyticsAgent.run(question, data)
       ├── Analyzes business question
       ├── Selects appropriate metrics
       ├── Processes data
       ├── Generates insights
       └── Creates visualizations
```

### 3. Tools Are Called (Based on Question Type)

#### Sales Analysis
```
tools/sales_analyzer.py
   └── SalesAnalyzerTool.execute(data, period)
       ├── Calculates metrics
       │   ├── Total revenue
       │   ├── Average order value (AOV)
       │   ├── Growth rate (% change)
       │   ├── Sales by category
       │   └── Top products
       ├── Trend analysis
       │   ├── Daily/Weekly/Monthly trends
       │   ├── Seasonal patterns
       │   └── Anomaly detection
       └── Returns metrics + insights
```

#### Customer Segmentation
```
tools/customer_segmentation.py
   └── CustomerSegmentationTool.execute(customer_data)
       ├── RFM Analysis
       │   ├── Recency (last purchase)
       │   ├── Frequency (purchase count)
       │   └── Monetary (total spent)
       ├── Segment creation
       │   ├── Champions (high RFM)
       │   ├── Loyal customers
       │   ├── At-risk customers
       │   └── Lost customers
       ├── Behavior patterns
       │   ├── Purchase frequency
       │   ├── Average basket size
       │   └── Product preferences
       └── Returns segments + characteristics
```

#### Product Analysis
```
tools/product_analyzer.py
   └── ProductAnalyzerTool.execute(product_data)
       ├── Performance metrics
       │   ├── Units sold
       │   ├── Revenue per product
       │   ├── Profit margins
       │   └── Stock turnover
       ├── Product rankings
       │   ├── Best sellers
       │   ├── Worst performers
       │   └── Trending products
       ├── Category analysis
       │   ├── Category performance
       │   └── Cross-sell opportunities
       └── Returns product insights
```

#### Forecasting
```
tools/forecasting_tool.py
   └── ForecastingTool.execute(historical_data)
       ├── Time series analysis
       │   ├── Trend decomposition
       │   ├── Seasonality detection
       │   └── Pattern identification
       ├── Prediction models
       │   ├── Linear regression
       │   ├── Moving averages
       │   └── ARIMA (if available)
       ├── Future projections
       │   ├── Next 30/60/90 days
       │   ├── Confidence intervals
       │   └── Scenario analysis
       └── Returns forecast + accuracy metrics
```

### 4. Workflow Orchestration (Business Intelligence)
```
workflows/analytics_workflow.py
   └── AnalyticsWorkflow.comprehensive_business_analysis()
       │
       Step 1: Sales Performance
       ├── Analyze current period
       ├── Compare to previous period
       ├── Identify trends
       │
       Step 2: Customer Insights
       ├── Segment customers
       ├── Identify high-value segments
       ├── Analyze behavior patterns
       │
       Step 3: Product Performance
       ├── Rank products
       ├── Identify opportunities
       ├── Spot declining items
       │
       Step 4: Forecasting
       ├── Predict next period
       ├── Revenue projections
       ├── Inventory needs
       │
       Step 5: Recommendations
       ├── Actionable insights
       ├── Priority actions
       └── Expected impact
```

### 5. Response Returns to Manager
```
   ↓
Result:
   ├── Executive summary
   ├── Key metrics & KPIs
   ├── Visualizations (charts)
   ├── Detailed insights
   ├── Recommendations
   └── Forecast projections
```

## 🎯 Data Flow Diagram

```
┌─────────┐
│BUSINESS │ Question + Data
│ MANAGER │
└────┬────┘
     │
     ▼
┌─────────────────────────────────────────────┐
│     AnalyticsAgent (agent.py)               │
│                                             │
│  ┌──────────────────────────────────┐      │
│  │   LLM Router (GPT-4)             │      │
│  │   - Interprets business question │      │
│  │   - Selects analysis methods     │      │
│  │   - Generates insights           │      │
│  │   - Creates recommendations      │      │
│  └──────────┬───────────────────────┘      │
│             │                               │
│   ┌─────────┴──────────┐                   │
│   │                    │                   │
│   ▼                    ▼                   │
│ ┌─────────┐      ┌──────────┐             │
│ │ Memory  │      │ Prompt   │             │
│ │ Past    │      │ Business │             │
│ │ Reports │      │ Context  │             │
│ └─────────┘      └──────────┘             │
│                                            │
│   ┌────────────────────────────────┐      │
│   │        Tools (4)               │      │
│   │                                │      │
│   │  💰 Sales Analyzer             │      │
│   │     ↓ Revenue metrics          │      │
│   │     ↓ Trend analysis           │      │
│   │     ↓ Growth rates             │      │
│   │                                │      │
│   │  👥 Customer Segmentation      │      │
│   │     ↓ RFM analysis             │      │
│   │     ↓ Behavior patterns        │      │
│   │     ↓ Segment profiles         │      │
│   │                                │      │
│   │  📦 Product Analyzer           │      │
│   │     ↓ Performance metrics      │      │
│   │     ↓ Rankings                 │      │
│   │     ↓ Category insights        │      │
│   │                                │      │
│   │  🔮 Forecasting Tool           │      │
│   │     ↓ Future predictions       │      │
│   │     ↓ Confidence intervals     │      │
│   │     ↓ Scenario planning        │      │
│   └────────────────────────────────┘      │
└─────────────────────────────────────────────┘
     │
     ▼
┌─────────┐
│BUSINESS │ Insights + Recommendations
│ MANAGER │
└─────────┘
```

## 🚀 Usage Examples

### Sales Analysis
```python
from projects.ecommerce_analytics.agent import AnalyticsAgent
import pandas as pd

agent = AnalyticsAgent()
sales_data = pd.read_csv("sales.csv")
result = agent.run(
    "What were our top selling products last quarter?",
    data=sales_data
)
print(result)
```

**Flow:**
1. Question + Data → AnalyticsAgent
2. Agent → Product Analyzer tool
3. Tool → Calculates product metrics
4. Tool → Ranks by revenue
5. Agent → Generates insights
6. Result → Top 10 products with metrics + trends

### Customer Segmentation
```python
result = agent.run(
    "Segment our customers by purchase behavior",
    data=customer_data
)
```

**Flow:**
1. Question → AnalyticsAgent
2. Agent → Customer Segmentation tool
3. Tool → RFM analysis
4. Tool → Creates 5 segments
5. Agent → Profiles each segment
6. Result → Segment characteristics + recommendations

### Comprehensive Business Report
```python
from projects.ecommerce_analytics.workflows.analytics_workflow import AnalyticsWorkflow

workflow = AnalyticsWorkflow()
report = workflow.comprehensive_business_analysis(
    data=business_data,
    period="Q3_2024"
)
```

**Flow:**
1. Workflow starts with all data
2. Step 1: Sales analysis → Revenue $1.2M (+15%)
3. Step 2: Customer segments → 5 segments identified
4. Step 3: Product ranking → Top 20 products
5. Step 4: Forecast → Next Q: $1.4M projected
6. Step 5: Recommendations → 3 action items
7. Result → Complete business intelligence report

## 🔧 Key Components

### agent.py
- **Purpose:** Main analytics agent
- **Responsibilities:**
  - Initialize LLM connection
  - Register analytics tools
  - Interpret business questions
  - Generate insights
- **Key Methods:**
  - `__init__()`: Setup
  - `run(question, data)`: Analyze
  - `_generate_insights()`: Create recommendations

### tools/sales_analyzer.py
- **Purpose:** Sales metrics & trends
- **Features:**
  - Revenue calculations
  - Growth rate analysis
  - Trend detection
  - Anomaly identification
- **Returns:** Metrics + trends + insights

### tools/customer_segmentation.py
- **Purpose:** Customer behavior analysis
- **Features:**
  - RFM analysis
  - Segment creation
  - Behavior patterns
  - Lifetime value calculation
- **Returns:** Segments + profiles

### tools/product_analyzer.py
- **Purpose:** Product performance
- **Features:**
  - Sales by product
  - Profitability analysis
  - Category performance
  - Cross-sell opportunities
- **Returns:** Product insights

### tools/forecasting_tool.py
- **Purpose:** Predictive analytics
- **Features:**
  - Time series decomposition
  - Trend projection
  - Seasonality adjustment
  - Confidence intervals
- **Returns:** Forecast + accuracy

### workflows/analytics_workflow.py
- **Purpose:** Business intelligence
- **Features:**
  - Comprehensive analysis
  - Product optimization
  - Customer strategies
  - Pricing optimization
  - Inventory planning

## 💡 Analysis Types & When to Use

| Question Type | Tool Used | Output | Time |
|--------------|-----------|--------|------|
| "What are sales?" | Sales Analyzer | Revenue metrics | 3-5s |
| "Who are best customers?" | Customer Segmentation | RFM segments | 5-10s |
| "Which products sell best?" | Product Analyzer | Product rankings | 3-5s |
| "What's the forecast?" | Forecasting | Future projections | 10-15s |
| "Complete business review" | Workflow | Full report | 30-60s |

## 📊 Key Metrics Calculated

```
SALES METRICS
├── Total Revenue
├── Average Order Value (AOV)
├── Growth Rate (%)
├── Sales per Category
└── Best Selling Items

CUSTOMER METRICS
├── Customer Count
├── New vs Returning
├── Customer Lifetime Value (CLV)
├── Churn Rate
└── Purchase Frequency

PRODUCT METRICS
├── Units Sold
├── Revenue per Product
├── Profit Margin
├── Stock Turnover
└── Category Performance

FORECAST METRICS
├── Next Period Revenue
├── Confidence Interval
├── Growth Projection
└── Seasonal Adjustment
```

## 🎯 RFM Segmentation Logic

```
RFM Analysis
   ↓
Recency (Days since last purchase)
Frequency (Number of purchases)
Monetary (Total spent)
   ↓
Score: 1-5 for each dimension
   ↓
Segments Created:

🏆 Champions (555)
   └── Recent, frequent, high spend
       → VIP treatment, exclusive offers

❤️ Loyal (X5X)
   └── Frequent buyers
       → Loyalty program, rewards

⚠️ At Risk (51X)
   └── Haven't bought recently
       → Re-engagement campaign

😴 Hibernating (111)
   └── Long time, no purchase
       → Win-back offers

🆕 New Customers (5XX)
   └── Recent first purchase
       → Onboarding, nurture
```

## 🔮 Forecasting Process

```
Historical Data
   ↓
1. DATA PREPARATION
   ├── Clean data
   ├── Handle missing values
   └── Detect outliers
   ↓
2. TREND ANALYSIS
   ├── Identify trend (up/down/flat)
   ├── Detect seasonality
   └── Calculate growth rate
   ↓
3. MODEL SELECTION
   ├── Simple moving average
   ├── Linear regression
   └── Time series model
   ↓
4. PREDICTION
   ├── Generate forecast
   ├── Calculate confidence
   └── Scenario analysis
   ↓
5. VALIDATION
   ├── Check accuracy
   ├── Adjust if needed
   └── Present results
```

## 🔍 Reflection & Self-Improvement

Analytics accuracy is critical for business decisions:

```python
# Reflect on analysis quality
reflection = agent.reflect(analysis_report, criteria=[
    "Data accuracy and correct calculations",
    "Actionable insights provided",
    "Clear data-driven recommendations",
    "Relevant metrics highlighted",
    "Business context considered"
])

print(f"Analysis Quality: {reflection['score']}/10")
```

### Analytics Reflection Example
```python
{
    "score": 8.5,
    "strengths": [
        "Accurate RFM segmentation",
        "Clear actionable recommendations",
        "Good use of statistical metrics"
    ],
    "weaknesses": [
        "Could include year-over-year comparison",
        "Missing confidence intervals on forecast"
    ],
    "improvements": [
        "Add YoY growth rate for context",
        "Include 95% confidence interval on projections",
        "Suggest specific actions for each segment"
    ]
}
```

### Quality-Checked Reports
```python
# Generate report with quality assurance
result = agent.run_with_reflection(
    "Comprehensive business analysis",
    data=business_data,
    auto_improve=True,  # Ensure high-quality insights
    max_iterations=2
)

if result['reflection']['score'] >= 9.0:
    send_to_stakeholders(result['output'])
```

See [REFLECTION.md](../../REFLECTION.md) for complete guide.

## 🎓 Technical Details

- **LLM:** OpenAI GPT-4
- **Tools:** 4 (Sales, Customer, Product, Forecasting)
- **Data Processing:** pandas, numpy
- **Visualization:** matplotlib, seaborn
- **Response Time:** 5-30 seconds per analysis
- **Forecast Accuracy:** 80-90% (depends on data)
- **RFM Segments:** 5 main segments
- **Max Data Size:** 1M rows (configurable)
- **Reflection:** Analysis quality & accuracy validation supported
