# 🧪 Agentic AI - Test Guide

This guide explains how to test each AI agent project in the Agentic-AI system.

## 📋 Available Test Scripts

Each project has its own dedicated test script with multiple test scenarios:

| Project | Test Script | Description |
|---------|-------------|-------------|
| **Content Creation** | `test_content_writer.py` | Blog posts, social posts, landing pages |
| **Research** | `projects/research/test_research_agent.py` | Web research, arXiv, Wikipedia |
| **Data Visualization** | `projects/data_visualization/test_chart_agent.py` | Charts, graphs, plots |
| **Email Automation** | `projects/email_automation/test_email_agent.py` | Welcome, promotional, newsletters |
| **Social Media** | `projects/social_media_management/test_social_media_agent.py` | Twitter, LinkedIn, Instagram |
| **Customer Support** | `projects/customer_support/test_support_agent.py` | Technical, billing, product support |
| **E-commerce Analytics** | `projects/ecommerce_analytics/test_analytics_agent.py` | Sales, customers, products |

## 🚀 Quick Start

### Prerequisites

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

3. **Verify setup:**
   ```bash
   python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('✅ API Key loaded' if os.getenv('OPENAI_API_KEY') else '❌ No API Key')"
   ```

## 📝 Running Tests

### Option 1: Run Individual Project Tests

Navigate to project directory and run:

```bash
# Content Writer
cd /path/to/Agentic-AI
python test_content_writer.py

# Research Agent
python projects/research/test_research_agent.py

# Chart Agent
python projects/data_visualization/test_chart_agent.py

# Email Agent
python projects/email_automation/test_email_agent.py

# Social Media Agent
python projects/social_media_management/test_social_media_agent.py

# Support Agent
python projects/customer_support/test_support_agent.py

# Analytics Agent
python projects/ecommerce_analytics/test_analytics_agent.py
```

### Option 2: Run All Tests (Coming Soon)

```bash
python run_all_tests.py
```

## 📁 Output Locations

Each test script saves outputs to its project's `outputs/` directory:

```
Agentic-AI/
├── outputs/
│   └── content_creation/        # Content Writer outputs
├── projects/
│   ├── research/
│   │   └── outputs/             # Research outputs
│   ├── data_visualization/
│   │   └── outputs/             # Chart outputs
│   ├── email_automation/
│   │   └── outputs/             # Email outputs
│   ├── social_media_management/
│   │   └── outputs/             # Social media outputs
│   ├── customer_support/
│   │   └── outputs/             # Support outputs
│   └── ecommerce_analytics/
│       └── outputs/             # Analytics outputs
```

## 🧪 Test Examples

### Content Writer Agent

```python
from projects.content_creation.agents.content_writer_agent import create_content_writer_agent

agent = create_content_writer_agent()
result = agent.run(
    topic="AI in Healthcare",
    content_type="blog_post",
    word_count=500,
    tone="professional"
)
print(result)
```

### Research Agent

```python
from projects.research.agents.research_agent import create_research_agent

agent = create_research_agent()
result = agent.run(
    query="Latest AI trends in 2024",
    depth="comprehensive",
    include_citations=True
)
print(result)
```

### Chart Agent

```python
from projects.data_visualization.agents.chart_agent import create_chart_agent

agent = create_chart_agent()
data = {
    "categories": ["Jan", "Feb", "Mar"],
    "values": [100, 150, 200]
}
result = agent.run(
    chart_type="bar",
    data=data,
    title="Monthly Sales"
)
print(f"Chart saved to: {result}")
```

## 🔧 Customization

### Environment Variables

Configure in `.env` file:

```properties
# Model selection
DEFAULT_MODEL=gpt-4o-mini
RESEARCH_MODEL=gpt-4o-mini
CHART_MODEL=gpt-4o-mini

# Temperature settings
DEFAULT_TEMPERATURE=0.7
RESEARCH_TEMPERATURE=0.0

# Output settings
OUTPUT_FORMAT=markdown
SAVE_OUTPUTS=true
```

### Test Script Parameters

Each test script accepts interactive inputs and saves outputs automatically. You can modify the test scripts to:

- Change model parameters
- Adjust output formats
- Customize test scenarios
- Add new test cases

## 📊 Test Results

After running tests, you'll see:

- ✅ Success indicators
- 📝 Generated content previews
- 💾 File save confirmations
- 📁 Output directory locations

## 🐛 Troubleshooting

### Common Issues

**1. API Key Not Found**
```
❌ ERROR: OPENAI_API_KEY not found in .env file!
```
**Solution:** Add your OpenAI API key to the `.env` file.

**2. Module Import Error**
```
ModuleNotFoundError: No module named 'projects'
```
**Solution:** Run tests from the Agentic-AI root directory or ensure `sys.path` is set correctly.

**3. Permission Denied (Output Directory)**
```
PermissionError: [Errno 13] Permission denied: 'outputs/'
```
**Solution:** Ensure you have write permissions in the project directory.

## 🎯 Best Practices

1. **Start Small:** Test individual agents before running full workflows
2. **Check Outputs:** Review generated files in `outputs/` directories
3. **Monitor Costs:** Use `gpt-4o-mini` for testing (60x cheaper than GPT-4)
4. **Iterate:** Adjust parameters based on initial results
5. **Save Examples:** Keep good outputs as reference examples

## 📚 Next Steps

- Read individual project READMEs for detailed documentation
- Check `ARCHITECTURE.md` files for agent design details
- Explore `examples/` directories for more use cases
- Review `WORKFLOW_SUMMARY.md` for integration patterns

## 🤝 Contributing

When adding new tests:

1. Follow the existing test script structure
2. Include multiple test scenarios
3. Save outputs to project's `outputs/` directory
4. Add timestamps to output filenames
5. Update this README with new test information

## 📞 Support

For issues or questions:
- Check project documentation
- Review GitHub issues
- Contact development team

---

**Happy Testing! 🚀**
