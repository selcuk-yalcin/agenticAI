"""
Workflow Examples
Demonstrates how to use workflows across all projects
"""

def example_research_workflow():
    """Example: Comprehensive research workflow"""
    print("\n" + "="*60)
    print("RESEARCH WORKFLOW EXAMPLE")
    print("="*60)
    
    from projects.research.workflows import ResearchWorkflow
    
    workflow = ResearchWorkflow()
    
    # Comprehensive research
    result = workflow.comprehensive_research(
        topic="Artificial Intelligence in Healthcare",
        depth="medium"
    )
    
    print(f"\nResearch completed:")
    print(f"- Overview: {result['overview'][:100]}...")
    print(f"- Synthesis: {result['synthesis'][:100]}...")
    print(f"- Sources used: {len(result['sources_used'])}")


def example_visualization_workflow():
    """Example: Data visualization workflow"""
    print("\n" + "="*60)
    print("VISUALIZATION WORKFLOW EXAMPLE")
    print("="*60)
    
    from projects.data_visualization.workflows import VisualizationWorkflow
    
    workflow = VisualizationWorkflow()
    
    # Sample data
    data = {
        "month": ["Jan", "Feb", "Mar", "Apr", "May"],
        "sales": [100, 150, 130, 180, 200],
        "profit": [20, 30, 25, 40, 50]
    }
    
    # Analyze and visualize
    result = workflow.analyze_and_visualize(
        data=data,
        description="Monthly sales and profit trends"
    )
    
    print(f"\nVisualization created:")
    print(f"- Analysis: {result['analysis'][:100]}...")
    print(f"- Chart type: {result['chart_type']}")


def example_content_workflow():
    """Example: Content creation workflow"""
    print("\n" + "="*60)
    print("CONTENT CREATION WORKFLOW EXAMPLE")
    print("="*60)
    
    from projects.content_creation.workflows import ContentWorkflow
    
    workflow = ContentWorkflow()
    
    # Full content pipeline
    result = workflow.full_content_pipeline(
        topic="Top 10 AI Tools for Productivity",
        content_type="blog_post",
        target_audience="professionals"
    )
    
    print(f"\nContent created:")
    print(f"- Topic: {result['topic']}")
    print(f"- Keywords: {result['keywords']}")
    print(f"- Word count: {result['metadata']['word_count']}")
    print(f"- Final content: {result['final_content'][:100]}...")


def example_support_workflow():
    """Example: Customer support workflow"""
    print("\n" + "="*60)
    print("CUSTOMER SUPPORT WORKFLOW EXAMPLE")
    print("="*60)
    
    from projects.customer_support.workflows import SupportWorkflow
    
    workflow = SupportWorkflow()
    
    # Full ticket lifecycle
    result = workflow.full_ticket_lifecycle(
        ticket_id="TKT-001",
        customer_message="I can't access my account after password reset",
        customer_id="CUST123",
        priority="high"
    )
    
    print(f"\nTicket processed:")
    print(f"- Ticket ID: {result['ticket_id']}")
    print(f"- Priority: {result['priority']}")
    print(f"- Requires escalation: {result['requires_escalation']}")
    print(f"- Response: {result['response']['response'][:100]}...")


def example_analytics_workflow():
    """Example: E-commerce analytics workflow"""
    print("\n" + "="*60)
    print("E-COMMERCE ANALYTICS WORKFLOW EXAMPLE")
    print("="*60)
    
    from projects.ecommerce_analytics.workflows import AnalyticsWorkflow
    
    workflow = AnalyticsWorkflow()
    
    # Comprehensive business analysis
    result = workflow.comprehensive_business_analysis(
        period="last_month"
    )
    
    print(f"\nBusiness analysis completed:")
    print(f"- Period: {result['period']}")
    print(f"- Sales trends: {result['sales_trends']['analysis'][:100]}...")
    print(f"- Recommendations: {result['recommendations'][:100]}...")


def example_email_workflow():
    """Example: Email automation workflow"""
    print("\n" + "="*60)
    print("EMAIL AUTOMATION WORKFLOW EXAMPLE")
    print("="*60)
    
    from projects.email_automation.workflows import EmailWorkflow
    
    workflow = EmailWorkflow()
    
    # Full campaign workflow
    result = workflow.full_campaign_workflow(
        campaign_name="Summer Sale 2024",
        campaign_type="marketing",
        audience_size=5000
    )
    
    print(f"\nEmail campaign created:")
    print(f"- Campaign: {result['campaign_name']}")
    print(f"- Audience size: {result['plan']['audience_size']}")
    print(f"- A/B variants: {result['ab_variants']['num_variants']}")
    print(f"- Schedule: {result['schedule']['send_date']}")


def example_social_media_workflow():
    """Example: Social media workflow"""
    print("\n" + "="*60)
    print("SOCIAL MEDIA WORKFLOW EXAMPLE")
    print("="*60)
    
    from projects.social_media_management.workflows import SocialMediaWorkflow
    
    workflow = SocialMediaWorkflow()
    
    # Full campaign workflow
    result = workflow.full_campaign_workflow(
        campaign_name="Product Launch Campaign",
        platforms=["instagram", "twitter", "linkedin"],
        duration_days=14
    )
    
    print(f"\nSocial media campaign created:")
    print(f"- Campaign: {result['campaign_name']}")
    print(f"- Platforms: {', '.join(result['platforms'])}")
    print(f"- Duration: {result['duration_days']} days")
    print(f"- Posts created: {len(result['posts'])}")


def example_integrated_workflow():
    """Example: Integrated multi-project workflow"""
    print("\n" + "="*60)
    print("INTEGRATED WORKFLOW EXAMPLE")
    print("="*60)
    print("Combining Research → Content → Social Media")
    
    # Step 1: Research
    print("\n1. Researching topic...")
    from projects.research.workflows import ResearchWorkflow
    research_wf = ResearchWorkflow()
    research = research_wf.comprehensive_research(
        topic="AI in Customer Service",
        depth="light"
    )
    print(f"   ✓ Research completed")
    
    # Step 2: Create content
    print("\n2. Creating content based on research...")
    from projects.content_creation.workflows import ContentWorkflow
    content_wf = ContentWorkflow()
    content = content_wf.full_content_pipeline(
        topic="AI in Customer Service",
        content_type="article",
        target_audience="business_owners"
    )
    print(f"   ✓ Article created ({content['metadata']['word_count']} words)")
    
    # Step 3: Create social media posts
    print("\n3. Creating social media promotion...")
    from projects.social_media_management.workflows import SocialMediaWorkflow
    social_wf = SocialMediaWorkflow()
    social = social_wf.content_repurposing_workflow(
        original_content=content['final_content'][:500],
        source_platform="blog",
        target_platforms=["twitter", "linkedin", "instagram"]
    )
    print(f"   ✓ Social posts created for {len(social['target_platforms'])} platforms")
    
    print("\n✓ Integrated workflow completed!")


def example_batch_processing():
    """Example: Batch processing workflow"""
    print("\n" + "="*60)
    print("BATCH PROCESSING EXAMPLE")
    print("="*60)
    
    from projects.customer_support.workflows import SupportWorkflow
    
    workflow = SupportWorkflow()
    
    # Sample batch of tickets
    tickets = [
        {
            "ticket_id": "TKT-001",
            "message": "How do I reset my password?",
            "customer_id": "CUST123",
            "priority": "medium"
        },
        {
            "ticket_id": "TKT-002",
            "message": "My order hasn't arrived",
            "customer_id": "CUST456",
            "priority": "high"
        },
        {
            "ticket_id": "TKT-003",
            "message": "Need help with billing",
            "customer_id": "CUST789",
            "priority": "medium"
        }
    ]
    
    # Process batch
    result = workflow.batch_ticket_processing(tickets)
    
    print(f"\nBatch processing completed:")
    print(f"- Total tickets: {result['total_tickets']}")
    print(f"- Processed: {result['processed']}")
    print(f"- Escalations: {result['escalations']}")
    print(f"- Summary: {result['summary']}")


def example_campaign_sequences():
    """Example: Campaign sequences"""
    print("\n" + "="*60)
    print("CAMPAIGN SEQUENCES EXAMPLE")
    print("="*60)
    
    from projects.email_automation.workflows import EmailWorkflow
    
    workflow = EmailWorkflow()
    
    # Drip campaign
    result = workflow.drip_campaign_workflow(
        campaign_type="onboarding",
        duration_days=21,
        num_emails=7
    )
    
    print(f"\nDrip campaign created:")
    print(f"- Type: {result['campaign_type']}")
    print(f"- Duration: {result['duration_days']} days")
    print(f"- Emails: {result['num_emails']}")
    print(f"- Interval: Every {result['interval_days']} days")
    
    for email in result['emails'][:3]:  # Show first 3
        print(f"   - Email {email['email_number']} (Day {email['send_day']})")


def main():
    """Run all workflow examples"""
    print("=" * 60)
    print("AI AGENT WORKFLOWS - EXAMPLES")
    print("=" * 60)
    
    examples = [
        ("Research Workflow", example_research_workflow),
        ("Visualization Workflow", example_visualization_workflow),
        ("Content Workflow", example_content_workflow),
        ("Support Workflow", example_support_workflow),
        ("Analytics Workflow", example_analytics_workflow),
        ("Email Workflow", example_email_workflow),
        ("Social Media Workflow", example_social_media_workflow),
        ("Integrated Workflow", example_integrated_workflow),
        ("Batch Processing", example_batch_processing),
        ("Campaign Sequences", example_campaign_sequences)
    ]
    
    for name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"\n❌ {name} Error: {e}")
    
    print("\n" + "="*60)
    print("All workflow examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()
