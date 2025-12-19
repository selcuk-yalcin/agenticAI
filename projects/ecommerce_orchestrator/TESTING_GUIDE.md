# E-Commerce Orchestrator - Testing Guide

## Overview

This guide provides comprehensive testing instructions for the E-Commerce Orchestrator Agent system.

## Test Suite Structure

The test suite includes **15 advanced test scenarios** covering all major capabilities:

### Test Categories

#### 1. **Platform Integration Tests**
- ✅ Test 1: MCP Platform Connection
- ✅ Test 14: Multi-Channel Synchronization

#### 2. **Analytics & Reporting Tests**
- ✅ Test 2: Sales Analytics & Graph Generation
- ✅ Test 6: Comprehensive Business Report
- ✅ Test 15: Customer Lifetime Value Analysis

#### 3. **Image Processing Tests**
- ✅ Test 3: AI Image Processing (5 Variants)

#### 4. **Workflow Automation Tests**
- ✅ Test 4: Complete New Product Workflow
- ✅ Test 7: Inventory Sync and Management

#### 5. **Marketing & Email Tests**
- ✅ Test 5: Automated Customer Email Campaign
- ✅ Test 10: Abandoned Cart Recovery
- ✅ Test 11: Social Media Automation

#### 6. **Intelligence & Optimization Tests**
- ✅ Test 8: Dynamic Pricing Optimization
- ✅ Test 9: Customer Segmentation Analysis
- ✅ Test 12: Fraud Detection
- ✅ Test 13: AI Product Recommendations

## Running Tests

### Option 1: Run All Tests
```bash
cd projects/ecommerce_orchestrator
python test_advanced_features.py
```

### Option 2: Run Individual Tests
```python
from test_advanced_features import *

# Test specific feature
test_platform_connection()
test_image_processing_5_variants()
test_new_product_complete_workflow()
```

## Test Details

### Test 1: Platform Connection via MCP
**What it tests:**
- Connection to e-commerce platform
- MCP protocol authentication
- Capability verification
- Session management

**Expected Output:**
```json
{
  "status": "connected",
  "platform": "Shopify",
  "session_id": "mcp_session_...",
  "capabilities": ["read_products", "write_products", ...]
}
```

### Test 2: Sales Analytics & Graphs
**What it tests:**
- Sales data fetching
- Graph generation (line, bar charts)
- KPI calculation
- Insights generation

**Expected Output:**
- Revenue trend graphs
- Top products analysis
- Performance metrics
- Actionable recommendations

### Test 3: AI Image Processing (5 Variants)
**What it tests:**
- Image upload handling
- AI variant generation
- Quality optimization
- Format conversion

**Expected Output:**
```json
{
  "variants_generated": {
    "original": {...},
    "lifestyle": {...},
    "closeup": {...},
    "transparent": {...},
    "social": {...}
  },
  "processing_time": "8.5 seconds",
  "quality_scores": {...}
}
```

### Test 4: Complete New Product Workflow
**What it tests:**
- End-to-end product launch
- Image processing
- Listing creation
- Price optimization
- Publishing
- Email campaign
- Social media posting

**Expected Output:**
- 6 workflow steps completed
- Product published live
- Campaigns scheduled
- Performance tracking enabled

**Timeline:** ~20 seconds

### Test 5: Automated Customer Email Campaign
**What it tests:**
- Email sequence creation
- Customer segmentation
- Personalization
- Scheduling optimization
- Performance tracking

**Expected Output:**
- Campaign created with 4-email sequence
- 2847 recipients segmented
- Open/click rates predicted
- Conversion tracking enabled

### Test 6: Comprehensive Business Report
**What it tests:**
- Data aggregation
- Report generation
- Insight extraction
- Export formats

**Expected Output:**
- Multi-section report
- 12+ charts included
- AI insights
- PDF/Excel/HTML exports

### Test 7: Inventory Sync and Management
**What it tests:**
- Inventory fetching
- Low stock detection
- Reorder recommendations
- Stock alerts
- Turnover analysis

**Expected Output:**
- Current inventory status
- Low stock items identified
- Reorder suggestions
- Optimization recommendations

### Test 8: Dynamic Pricing Optimization
**What it tests:**
- Competitor analysis
- Price elasticity
- Historical performance
- Dynamic pricing strategy

**Expected Output:**
- Optimal price recommendations
- A/B testing suggestions
- Revenue impact projections
- Profit margin analysis

### Test 9: Customer Segmentation Analysis
**What it tests:**
- RFM segmentation
- Behavioral analysis
- Lifetime value calculation
- Churn prediction

**Expected Output:**
- Customer segments defined
- Characteristics per segment
- Marketing strategies
- Personalized offers

### Test 10: Abandoned Cart Recovery
**What it tests:**
- Cart abandonment detection
- Multi-step recovery sequence
- Discount progression
- Recovery tracking

**Expected Output:**
- Abandoned carts identified
- 3-email recovery sequence
- Expected recovery rate
- ROI projection

### Test 11: Social Media Automation
**What it tests:**
- Multi-platform posting
- Caption generation
- Hashtag optimization
- Scheduling algorithms
- Engagement tracking

**Expected Output:**
- Posts created for 4 platforms
- Optimal timing scheduled
- Content variants
- Performance metrics

### Test 12: Fraud Detection
**What it tests:**
- Order screening
- Risk scoring
- Pattern detection
- Verification workflows

**Expected Output:**
- Risk scores calculated
- Flagged orders identified
- Recommended actions
- False positive rate

### Test 13: AI Product Recommendations
**What it tests:**
- Collaborative filtering
- Personalization algorithms
- Cross-sell/upsell logic
- Conversion tracking

**Expected Output:**
- Recommendation types (7)
- Implementation strategy
- A/B testing plan
- Revenue impact estimate

### Test 14: Multi-Channel Sync
**What it tests:**
- Multi-platform integration
- Inventory synchronization
- Order centralization
- Pricing consistency

**Expected Output:**
- 5 channels synchronized
- Real-time updates enabled
- Unified dashboard
- Oversell prevention

### Test 15: Customer Lifetime Value
**What it tests:**
- CLV calculation
- Future value prediction
- Segment identification
- Retention strategies

**Expected Output:**
- 12-month CLV forecasts
- High-value customers identified
- At-risk detection
- Optimization strategies

## Test Results

### Output Location
All test results are saved to:
```
outputs/advanced_tests/
├── platform_connection_YYYYMMDD_HHMMSS.json
├── sales_analytics_YYYYMMDD_HHMMSS.json
├── image_5_variants_YYYYMMDD_HHMMSS.json
├── ...
└── test_summary.json
```

### Success Criteria
- ✅ All 15 tests pass
- ✅ Response time < 10 seconds per test
- ✅ Valid JSON output
- ✅ No errors or exceptions
- ✅ Actionable insights generated

### Expected Success Rate
**Target: 100%** (15/15 tests passing)

## Performance Benchmarks

| Test | Expected Time | Success Rate |
|------|--------------|--------------|
| Platform Connection | 1-2s | 100% |
| Sales Analytics | 2-3s | 100% |
| Image Processing | 8-10s | 100% |
| New Product Workflow | 18-22s | 100% |
| Email Campaign | 1-2s | 100% |
| Business Report | 3-5s | 100% |
| Inventory Sync | 2-3s | 100% |
| Pricing Optimization | 2-4s | 100% |
| Customer Segmentation | 3-5s | 100% |
| Cart Recovery | 2-3s | 100% |
| Social Automation | 2-3s | 100% |
| Fraud Detection | 1-2s | 100% |
| Recommendations | 2-3s | 100% |
| Multi-Channel Sync | 3-5s | 100% |
| CLV Analysis | 3-5s | 100% |

**Total Suite Runtime:** ~60-90 seconds

## Interpreting Results

### Successful Test
```json
{
  "test_name": "platform_connection",
  "status": "success",
  "response": {...},
  "timestamp": "2025-12-19T..."
}
```

### Failed Test
```json
{
  "test": "test_name",
  "status": "failed",
  "error": "Error message"
}
```

## Troubleshooting

### Common Issues

**Issue 1: Import Error**
```
ModuleNotFoundError: No module named 'core.base_agent'
```
**Solution:** Ensure you're running from the correct directory:
```bash
cd /path/to/Agentic-AI/projects/ecommerce_orchestrator
python test_advanced_features.py
```

**Issue 2: Output Directory Not Found**
```
FileNotFoundError: outputs/advanced_tests/
```
**Solution:** Create the directory:
```bash
mkdir -p outputs/advanced_tests
```

**Issue 3: Slow Performance**
- Expected for first run (model loading)
- Subsequent runs should be faster
- Image processing takes 8-10 seconds (AI generation)

## Advanced Testing

### Custom Test Scenarios

Create your own tests:

```python
from agents.orchestrator_agent import ECommerceOrchestratorAgent

def test_custom_scenario():
    agent = ECommerceOrchestratorAgent()
    
    prompt = """
    Your custom scenario here...
    """
    
    response = agent.run(prompt)
    print(response)

test_custom_scenario()
```

### Batch Testing

Test multiple scenarios:

```python
scenarios = [
    "Generate sales report for Q4 2025",
    "Analyze customer churn in VIP segment",
    "Optimize pricing for top 10 products",
    "Create holiday marketing campaign"
]

for scenario in scenarios:
    result = agent.run(scenario)
    print(f"\nScenario: {scenario}")
    print(f"Result: {result}\n")
```

### Integration Testing

Test with real API credentials:

```python
# Set environment variables
import os
os.environ['SHOPIFY_API_KEY'] = 'your_key'
os.environ['SHOPIFY_SHOP_URL'] = 'your_store.myshopify.com'

# Run tests with real connection
test_platform_connection()
```

## Best Practices

1. **Run Full Suite First**
   - Validates all capabilities
   - Identifies any issues
   - Provides baseline performance

2. **Review Each Test Output**
   - Check JSON structure
   - Verify data accuracy
   - Validate insights

3. **Monitor Performance**
   - Track execution time
   - Watch for degradation
   - Optimize as needed

4. **Save Test Results**
   - Keep historical data
   - Compare across versions
   - Track improvements

5. **Document Custom Tests**
   - Add comments
   - Explain scenarios
   - Share learnings

## Next Steps

After successful testing:

1. ✅ Review test results
2. ✅ Connect to real platform
3. ✅ Upload actual product images
4. ✅ Configure email campaigns
5. ✅ Set up dashboards
6. ✅ Launch first product!

## Support

For issues or questions:
- Check test output files
- Review error messages
- Consult README.md
- Check agent logs

---

**Happy Testing!** 🧪🚀
