"""
Quick Examples for All 7 Projects
Run this to test all agents
"""

def test_research_agent():
    """Test Research Agent"""
    print("\n=== Research Agent ===")
    from projects.research import ResearchAgent
    
    agent = ResearchAgent()
    result = agent.run("What is quantum computing?")
    print(f"Result: {result[:200]}...")

def test_chart_agent():
    """Test Chart Agent"""
    print("\n=== Chart Agent ===")
    from projects.data_visualization import ChartAgent
    import json
    
    agent = ChartAgent()
    data = {"month": ["Jan", "Feb", "Mar"], "sales": [100, 150, 120]}
    result = agent.run("Create a line chart", data=json.dumps(data))
    print(f"Chart created: {result.get('output_path', 'N/A')}")

def test_content_writer():
    """Test Content Writer Agent"""
    print("\n=== Content Writer Agent ===")
    from projects.content_creation import ContentWriterAgent
    
    agent = ContentWriterAgent()
    result = agent.run(
        topic="AI in healthcare",
        content_type="blog_post",
        keywords=["artificial intelligence", "medical technology"]
    )
    print(f"Content created: {result[:200]}...")

def test_support_agent():
    """Test Support Agent"""
    print("\n=== Support Agent ===")
    from projects.customer_support import SupportAgent
    
    agent = SupportAgent()
    result = agent.handle_inquiry(
        customer_message="How do I reset my password?",
        customer_id="CUST123"
    )
    print(f"Response: {result.get('response', '')[:200]}...")

def test_analytics_agent():
    """Test Analytics Agent"""
    print("\n=== Analytics Agent ===")
    from projects.ecommerce_analytics import AnalyticsAgent
    
    agent = AnalyticsAgent()
    result = agent.analyze_sales_trends(
        period="last_30_days",
        include_predictions=True
    )
    print(f"Analysis: {result.get('analysis', '')[:200]}...")

def test_email_agent():
    """Test Email Agent"""
    print("\n=== Email Agent ===")
    from projects.email_automation import EmailAgent
    
    agent = EmailAgent()
    result = agent.compose_email(
        email_type="marketing",
        purpose="product_launch",
        tone="friendly"
    )
    print(f"Email created: {result.get('content', '')[:200]}...")

def test_social_media_agent():
    """Test Social Media Agent"""
    print("\n=== Social Media Agent ===")
    from projects.social_media_management import SocialMediaAgent
    
    agent = SocialMediaAgent()
    result = agent.create_post(
        platform="instagram",
        content_type="product_showcase",
        tone="casual"
    )
    print(f"Post created: {result.get('content', '')[:200]}...")

def main():
    """Run all tests"""
    print("=" * 60)
    print("Testing All 7 AI Agent Projects")
    print("=" * 60)
    
    try:
        test_research_agent()
    except Exception as e:
        print(f"Research Agent Error: {e}")
    
    try:
        test_chart_agent()
    except Exception as e:
        print(f"Chart Agent Error: {e}")
    
    try:
        test_content_writer()
    except Exception as e:
        print(f"Content Writer Error: {e}")
    
    try:
        test_support_agent()
    except Exception as e:
        print(f"Support Agent Error: {e}")
    
    try:
        test_analytics_agent()
    except Exception as e:
        print(f"Analytics Agent Error: {e}")
    
    try:
        test_email_agent()
    except Exception as e:
        print(f"Email Agent Error: {e}")
    
    try:
        test_social_media_agent()
    except Exception as e:
        print(f"Social Media Agent Error: {e}")
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
