# Workflows Guide

Complete guide to using workflows for complex multi-step tasks.

## What are Workflows?

Workflows orchestrate multiple agents and tools to complete complex tasks that require multiple steps. Each project has specialized workflows for common use cases.

## Available Workflows

### 1. Research Workflows
**Location:** `projects/research/workflows/`

#### ResearchWorkflow

```python
from projects.research.workflows import ResearchWorkflow

workflow = ResearchWorkflow()

# Comprehensive research
result = workflow.comprehensive_research(
    topic="AI in Healthcare",
    depth="deep"  # light, medium, deep
)

# Comparative research
comparison = workflow.comparative_research(
    topics=["Tool A", "Tool B", "Tool C"],
    comparison_criteria=["cost", "features", "ease of use"]
)

# Trend analysis
trends = workflow.trend_analysis(
    topic="Electric Vehicles",
    time_period="last_year"
)

# Expert synthesis
synthesis = workflow.expert_synthesis(
    topic="Climate Change",
    perspectives=["scientific", "economic", "political"]
)
```

---

### 2. Visualization Workflows
**Location:** `projects/data_visualization/workflows/`

#### VisualizationWorkflow

```python
from projects.data_visualization.workflows import VisualizationWorkflow

workflow = VisualizationWorkflow()

# Analyze and visualize
result = workflow.analyze_and_visualize(
    data={"month": ["Jan", "Feb"], "sales": [100, 150]},
    description="Sales trends"
)

# Multi-chart dashboard
dashboard = workflow.multi_chart_dashboard(
    datasets=[data1, data2, data3],
    chart_types=["line", "bar", "pie"]
)

# Time series analysis
timeseries = workflow.time_series_analysis(
    data=time_data,
    time_column="date",
    value_columns=["revenue", "profit"]
)

# Correlation analysis
correlation = workflow.correlation_analysis(
    data=dataset,
    variables=["age", "income", "spending"]
)
```

---

### 3. Content Workflows
**Location:** `projects/content_creation/workflows/`

#### ContentWorkflow

```python
from projects.content_creation.workflows import ContentWorkflow

workflow = ContentWorkflow()

# Full content pipeline
result = workflow.full_content_pipeline(
    topic="10 Productivity Tips",
    content_type="blog_post",
    target_audience="professionals"
)

# Content series
series = workflow.content_series(
    main_topic="Python Programming",
    num_posts=5,
    content_type="article"
)

# Multi-format content
formats = workflow.multi_format_content(
    topic="AI Tools Review",
    formats=["blog_post", "article", "social_post"]
)

# Content repurposing
repurposed = workflow.content_repurposing(
    source_content=blog_post,
    target_platform="linkedin"
)

# A/B testing
variants = workflow.ab_testing_content(
    topic="New Product Launch",
    test_element="headline",
    num_variants=3
)
```

---

### 4. Support Workflows
**Location:** `projects/customer_support/workflows/`

#### SupportWorkflow

```python
from projects.customer_support.workflows import SupportWorkflow

workflow = SupportWorkflow()

# Full ticket lifecycle
result = workflow.full_ticket_lifecycle(
    ticket_id="TKT-001",
    customer_message="Issue description",
    customer_id="CUST123",
    priority="high"
)

# Batch processing
batch = workflow.batch_ticket_processing(
    tickets=[ticket1, ticket2, ticket3]
)

# Priority routing
routed = workflow.priority_routing(
    tickets=ticket_list
)

# Customer journey analysis
journey = workflow.customer_journey_analysis(
    customer_id="CUST123",
    ticket_history=past_tickets
)

# Knowledge base optimization
kb_articles = workflow.knowledge_base_optimization(
    common_issues=["password_reset", "billing", "shipping"]
)
```

---

### 5. Analytics Workflows
**Location:** `projects/ecommerce_analytics/workflows/`

#### AnalyticsWorkflow

```python
from projects.ecommerce_analytics.workflows import AnalyticsWorkflow

workflow = AnalyticsWorkflow()

# Comprehensive business analysis
analysis = workflow.comprehensive_business_analysis(
    period="last_quarter"
)

# Product optimization
optimization = workflow.product_optimization_workflow(
    product_ids=["PRD001", "PRD002"]
)

# Customer segmentation
segments = workflow.customer_segmentation_workflow()

# Pricing optimization
pricing = workflow.pricing_optimization_workflow(
    product_category="Electronics"
)

# Seasonal trends
seasonal = workflow.seasonal_trend_workflow(
    seasons=["spring", "summer", "fall", "winter"]
)

# Competitor analysis
competitive = workflow.competitor_analysis_workflow(
    competitors=["Competitor A", "Competitor B"]
)
```

---

### 6. Email Workflows
**Location:** `projects/email_automation/workflows/`

#### EmailWorkflow

```python
from projects.email_automation.workflows import EmailWorkflow

workflow = EmailWorkflow()

# Full campaign
campaign = workflow.full_campaign_workflow(
    campaign_name="Summer Sale",
    campaign_type="marketing",
    audience_size=10000
)

# Drip campaign
drip = workflow.drip_campaign_workflow(
    campaign_type="onboarding",
    duration_days=30,
    num_emails=7
)

# Newsletter
newsletter = workflow.newsletter_workflow(
    topics=["AI News", "Tips", "Case Studies"],
    frequency="weekly"
)

# Transactional suite
transactional = workflow.transactional_email_suite(
    business_type="ecommerce"
)

# Personalization
personalized = workflow.personalization_workflow(
    customer_segments=["VIP", "Regular", "New"]
)

# Re-engagement
reengagement = workflow.reengagement_campaign(
    inactive_duration="90_days"
)
```

---

### 7. Social Media Workflows
**Location:** `projects/social_media_management/workflows/`

#### SocialMediaWorkflow

```python
from projects.social_media_management.workflows import SocialMediaWorkflow

workflow = SocialMediaWorkflow()

# Full campaign
campaign = workflow.full_campaign_workflow(
    campaign_name="Product Launch",
    platforms=["instagram", "twitter", "linkedin"],
    duration_days=14
)

# Content repurposing
repurposed = workflow.content_repurposing_workflow(
    original_content=blog_post,
    source_platform="blog",
    target_platforms=["twitter", "linkedin"]
)

# Viral content
viral = workflow.viral_content_workflow(
    topic="Behind The Scenes",
    platform="instagram"
)

# Influencer collaboration
influencer = workflow.influencer_collaboration_workflow(
    campaign_name="Brand Partnership",
    influencer_tier="micro"
)

# Product launch
launch = workflow.product_launch_workflow(
    product_name="New Product",
    launch_date="2024-07-01",
    platforms=["instagram", "twitter"]
)

# Performance analysis
performance = workflow.performance_analysis_workflow(
    posts=post_list,
    time_period="last_month"
)
```

---

## Integrated Workflows

Combine multiple workflows for complex tasks:

### Example: Content Marketing Pipeline

```python
# 1. Research
from projects.research.workflows import ResearchWorkflow
research_wf = ResearchWorkflow()
research = research_wf.comprehensive_research(
    topic="AI Trends 2024",
    depth="medium"
)

# 2. Create content
from projects.content_creation.workflows import ContentWorkflow
content_wf = ContentWorkflow()
content = content_wf.full_content_pipeline(
    topic="AI Trends 2024",
    content_type="blog_post",
    target_audience="tech_professionals"
)

# 3. Social media promotion
from projects.social_media_management.workflows import SocialMediaWorkflow
social_wf = SocialMediaWorkflow()
social = social_wf.content_repurposing_workflow(
    original_content=content['final_content'],
    source_platform="blog",
    target_platforms=["twitter", "linkedin", "instagram"]
)

# 4. Email newsletter
from projects.email_automation.workflows import EmailWorkflow
email_wf = EmailWorkflow()
newsletter = email_wf.newsletter_workflow(
    topics=["AI Trends", research['synthesis']],
    frequency="weekly"
)
```

### Example: Customer Intelligence Pipeline

```python
# 1. Analyze customer behavior
from projects.ecommerce_analytics.workflows import AnalyticsWorkflow
analytics_wf = AnalyticsWorkflow()
segments = analytics_wf.customer_segmentation_workflow()

# 2. Create targeted email campaigns
from projects.email_automation.workflows import EmailWorkflow
email_wf = EmailWorkflow()
campaigns = email_wf.personalization_workflow(
    customer_segments=segments['segments']
)

# 3. Setup support for each segment
from projects.customer_support.workflows import SupportWorkflow
support_wf = SupportWorkflow()
# Configure support based on segments
```

---

## Best Practices

### 1. Workflow Selection
- Use **single-agent** for simple tasks
- Use **workflows** for multi-step processes
- Use **integrated workflows** for cross-project needs

### 2. Error Handling
```python
try:
    result = workflow.comprehensive_research(topic="...")
except Exception as e:
    print(f"Workflow error: {e}")
    # Fallback or retry logic
```

### 3. State Management
```python
# Workflows maintain history
workflow = ResearchWorkflow()
workflow.comprehensive_research(topic="Topic 1")
workflow.comprehensive_research(topic="Topic 2")

# Get all results
history = workflow.get_research_history()
```

### 4. Custom Workflows

Create your own workflows:

```python
from projects.research.workflows import ResearchWorkflow
from projects.content_creation.workflows import ContentWorkflow

class CustomWorkflow:
    def __init__(self):
        self.research = ResearchWorkflow()
        self.content = ContentWorkflow()
    
    def custom_pipeline(self, topic: str):
        # Your custom logic
        research = self.research.comprehensive_research(topic)
        content = self.content.full_content_pipeline(topic)
        
        return {
            "research": research,
            "content": content
        }
```

---

## Workflow Outputs

All workflows return structured dictionaries:

```python
{
    "status": "completed",
    "results": {...},
    "metadata": {
        "started_at": "...",
        "completed_at": "...",
        "duration_seconds": 45
    },
    "history": [...]
}
```

---

## Testing Workflows

```bash
# Test specific workflow
python workflow_examples.py

# Test integrated workflows
python -c "from workflow_examples import example_integrated_workflow; example_integrated_workflow()"
```

---

## Performance Tips

1. **Batch Processing**: Use batch methods when available
2. **Async Operations**: Some workflows support async (check docs)
3. **Caching**: Results are cached in workflow history
4. **Parallel Execution**: Run independent workflows in parallel

---

## Troubleshooting

### Common Issues

**Issue**: Workflow takes too long
- **Solution**: Use "light" depth for research, reduce data size

**Issue**: Out of memory
- **Solution**: Process in batches, clear history periodically

**Issue**: Incomplete results
- **Solution**: Check API rate limits, verify data format

---

## Next Steps

1. Try basic workflows: `python workflow_examples.py`
2. Create custom workflows for your needs
3. Integrate multiple workflows
4. Monitor performance and optimize

For more details, see individual project READMEs in `projects/*/README.md`
