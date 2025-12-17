"""
Architecture Diagram Generator
Creates visual flowcharts for all agent projects
"""

try:
    from diagrams import Diagram, Cluster, Edge
    from diagrams.custom import Custom
    from diagrams.programming.language import Python
    from diagrams.onprem.client import User
    from diagrams.onprem.compute import Server
    from diagrams.onprem.database import MongoDB
    DIAGRAMS_AVAILABLE = True
except ImportError:
    DIAGRAMS_AVAILABLE = False
    print("⚠️  'diagrams' package not installed. Installing...")
    print("Run: pip install diagrams")


def create_research_diagram():
    """Create Research Agent architecture diagram"""
    if not DIAGRAMS_AVAILABLE:
        return
    
    with Diagram("Research Agent Architecture", filename="docs/diagrams/research_architecture", show=False, direction="LR"):
        user = User("User")
        
        with Cluster("Research Agent"):
            with Cluster("LLM Router"):
                llm = Server("GPT-4/Claude")
            
            prompt = Python("System Prompt:\nResearch Expert")
            memory = MongoDB("Conversation\nMemory")
            
            with Cluster("Tools"):
                tool1 = Python("Tavily Search\n(Web Search)")
                tool2 = Python("Wikipedia\n(Encyclopedia)")
                tool3 = Python("arXiv\n(Academic Papers)")
            
            user >> Edge(label="Query") >> llm
            llm >> prompt
            llm >> memory
            llm >> Edge(label="Uses") >> tool1
            llm >> Edge(label="Uses") >> tool2
            llm >> Edge(label="Uses") >> tool3
            
            tool1 >> Edge(label="Results") >> llm
            tool2 >> Edge(label="Results") >> llm
            tool3 >> Edge(label="Results") >> llm
            
            llm >> Edge(label="Response") >> user


def create_visualization_diagram():
    """Create Data Visualization Agent architecture diagram"""
    if not DIAGRAMS_AVAILABLE:
        return
    
    with Diagram("Data Visualization Agent Architecture", filename="docs/diagrams/visualization_architecture", show=False, direction="LR"):
        user = User("User + Data")
        
        with Cluster("Chart Agent"):
            with Cluster("LLM Router"):
                llm = Server("GPT-4")
            
            prompt = Python("System Prompt:\nData Analyst")
            memory = MongoDB("Chart\nHistory")
            
            with Cluster("Tools"):
                tool1 = Python("Data Analysis\n(Stats & Insights)")
                tool2 = Python("Line Chart")
                tool3 = Python("Bar Chart")
                tool4 = Python("Scatter Plot")
                tool5 = Python("Pie Chart")
                tool6 = Python("Heatmap")
            
            user >> Edge(label="Data + Request") >> llm
            llm >> prompt
            llm >> memory
            llm >> tool1
            llm >> tool2
            llm >> tool3
            llm >> tool4
            llm >> tool5
            llm >> tool6
            
            tool1 >> Edge(label="Analysis") >> llm
            tool2 >> Edge(label="Chart") >> llm
            
            llm >> Edge(label="Visualization") >> user


def create_content_diagram():
    """Create Content Creation Agent architecture diagram"""
    if not DIAGRAMS_AVAILABLE:
        return
    
    with Diagram("Content Creation Agent Architecture", filename="docs/diagrams/content_architecture", show=False, direction="LR"):
        user = User("User")
        
        with Cluster("Content Writer Agent"):
            with Cluster("LLM Router"):
                llm = Server("GPT-4")
            
            prompt = Python("System Prompt:\nExpert Content Writer")
            memory = MongoDB("Content\nLibrary")
            
            with Cluster("Tools"):
                tool1 = Python("Keyword Research\n(SEO Keywords)")
                tool2 = Python("SEO Optimizer\n(Content Analysis)")
            
            with Cluster("Content Types"):
                type1 = Python("Blog Post")
                type2 = Python("Article")
                type3 = Python("Landing Page")
                type4 = Python("Social Post")
            
            user >> Edge(label="Topic") >> llm
            llm >> prompt
            llm >> memory
            llm >> tool1
            llm >> tool2
            llm >> type1
            llm >> type2
            llm >> type3
            llm >> type4
            
            tool1 >> Edge(label="Keywords") >> llm
            tool2 >> Edge(label="Optimization") >> llm
            
            llm >> Edge(label="Content") >> user


def create_support_diagram():
    """Create Customer Support Agent architecture diagram"""
    if not DIAGRAMS_AVAILABLE:
        return
    
    with Diagram("Customer Support Agent Architecture", filename="docs/diagrams/support_architecture", show=False, direction="LR"):
        user = User("Customer")
        
        with Cluster("Support Agent"):
            with Cluster("LLM Router"):
                llm = Server("GPT-4")
            
            prompt = Python("System Prompt:\nProfessional Support")
            memory = MongoDB("Ticket\nHistory")
            
            with Cluster("Analysis"):
                sentiment = Python("Sentiment\nAnalysis")
                escalation = Python("Escalation\nDetection")
            
            with Cluster("Features"):
                kb = Python("Knowledge Base\nSearch")
                categorize = Python("Ticket\nCategorization")
                response = Python("Response\nGeneration")
            
            user >> Edge(label="Inquiry") >> llm
            llm >> prompt
            llm >> memory
            llm >> sentiment
            llm >> escalation
            llm >> kb
            llm >> categorize
            llm >> response
            
            response >> Edge(label="Solution") >> user


def create_analytics_diagram():
    """Create E-commerce Analytics Agent architecture diagram"""
    if not DIAGRAMS_AVAILABLE:
        return
    
    with Diagram("E-commerce Analytics Agent Architecture", filename="docs/diagrams/analytics_architecture", show=False, direction="LR"):
        user = User("Business User")
        
        with Cluster("Analytics Agent"):
            with Cluster("LLM Router"):
                llm = Server("GPT-4")
            
            prompt = Python("System Prompt:\nData Analyst Expert")
            memory = MongoDB("Analysis\nHistory")
            
            with Cluster("Analysis Types"):
                sales = Python("Sales\nTrends")
                product = Python("Product\nPerformance")
                customer = Python("Customer\nBehavior")
                forecast = Python("Revenue\nForecasting")
            
            with Cluster("Features"):
                cart = Python("Cart Abandonment")
                recommend = Python("Product\nRecommendations")
                segment = Python("Customer\nSegmentation")
            
            user >> Edge(label="Business Query") >> llm
            llm >> prompt
            llm >> memory
            llm >> sales
            llm >> product
            llm >> customer
            llm >> forecast
            llm >> cart
            llm >> recommend
            llm >> segment
            
            llm >> Edge(label="Insights & Reports") >> user


def create_email_diagram():
    """Create Email Automation Agent architecture diagram"""
    if not DIAGRAMS_AVAILABLE:
        return
    
    with Diagram("Email Automation Agent Architecture", filename="docs/diagrams/email_architecture", show=False, direction="LR"):
        user = User("Marketer")
        
        with Cluster("Email Agent"):
            with Cluster("LLM Router"):
                llm = Server("GPT-4")
            
            prompt = Python("System Prompt:\nEmail Marketing Expert")
            memory = MongoDB("Campaign\nHistory")
            
            with Cluster("Email Types"):
                marketing = Python("Marketing\nEmails")
                transactional = Python("Transactional\nEmails")
                drip = Python("Drip\nCampaigns")
                newsletter = Python("Newsletters")
            
            with Cluster("Features"):
                personalize = Python("Personalization")
                ab_test = Python("A/B Testing")
                optimize = Python("Subject Line\nOptimization")
                schedule = Python("Smart\nScheduling")
            
            user >> Edge(label="Campaign Brief") >> llm
            llm >> prompt
            llm >> memory
            llm >> marketing
            llm >> transactional
            llm >> drip
            llm >> newsletter
            llm >> personalize
            llm >> ab_test
            llm >> optimize
            
            llm >> Edge(label="Email Content") >> user


def create_social_media_diagram():
    """Create Social Media Agent architecture diagram"""
    if not DIAGRAMS_AVAILABLE:
        return
    
    with Diagram("Social Media Management Agent Architecture", filename="docs/diagrams/social_media_architecture", show=False, direction="LR"):
        user = User("Social Media Manager")
        
        with Cluster("Social Media Agent"):
            with Cluster("LLM Router"):
                llm = Server("GPT-4")
            
            prompt = Python("System Prompt:\nSocial Media Expert")
            memory = MongoDB("Content\nLibrary")
            
            with Cluster("Platforms"):
                instagram = Python("Instagram")
                twitter = Python("Twitter/X")
                linkedin = Python("LinkedIn")
                facebook = Python("Facebook")
                tiktok = Python("TikTok")
            
            with Cluster("Features"):
                hashtags = Python("Hashtag\nOptimization")
                calendar = Python("Content\nCalendar")
                repurpose = Python("Content\nRepurposing")
                analytics = Python("Engagement\nAnalysis")
            
            user >> Edge(label="Campaign Idea") >> llm
            llm >> prompt
            llm >> memory
            llm >> instagram
            llm >> twitter
            llm >> linkedin
            llm >> facebook
            llm >> tiktok
            llm >> hashtags
            llm >> calendar
            llm >> repurpose
            
            llm >> Edge(label="Social Content") >> user


def create_overall_architecture():
    """Create overall system architecture"""
    if not DIAGRAMS_AVAILABLE:
        return
    
    with Diagram("AI Agent System - Overall Architecture", filename="docs/diagrams/overall_architecture", show=False, direction="TB"):
        user = User("User")
        
        with Cluster("Core System"):
            base_agent = Python("BaseAgent\n(Abstract)")
            base_tool = Python("BaseTool\n(Abstract)")
            llm_client = Server("LLM Client\n(OpenAI/Anthropic)")
            config = MongoDB("Configuration\n& Settings")
        
        with Cluster("Projects"):
            with Cluster("Research"):
                research_agent = Python("ResearchAgent")
                research_tools = Python("3 Tools")
            
            with Cluster("Data Viz"):
                viz_agent = Python("ChartAgent")
                viz_tools = Python("2 Tools")
            
            with Cluster("Content"):
                content_agent = Python("ContentWriterAgent")
                content_tools = Python("2 Tools")
            
            with Cluster("Support"):
                support_agent = Python("SupportAgent")
                support_tools = Python("Analysis Tools")
            
            with Cluster("Analytics"):
                analytics_agent = Python("AnalyticsAgent")
                analytics_tools = Python("Analysis Methods")
            
            with Cluster("Email"):
                email_agent = Python("EmailAgent")
                email_tools = Python("Campaign Tools")
            
            with Cluster("Social"):
                social_agent = Python("SocialMediaAgent")
                social_tools = Python("Platform Tools")
        
        user >> research_agent
        user >> viz_agent
        user >> content_agent
        user >> support_agent
        user >> analytics_agent
        user >> email_agent
        user >> social_agent
        
        research_agent >> base_agent >> llm_client
        viz_agent >> base_agent
        content_agent >> base_agent
        support_agent >> base_agent
        analytics_agent >> base_agent
        email_agent >> base_agent
        social_agent >> base_agent
        
        research_tools >> base_tool
        viz_tools >> base_tool
        content_tools >> base_tool


def create_workflow_diagram():
    """Create workflow system architecture"""
    if not DIAGRAMS_AVAILABLE:
        return
    
    with Diagram("Workflow System Architecture", filename="docs/diagrams/workflow_architecture", show=False, direction="LR"):
        user = User("User")
        
        with Cluster("Workflow Layer"):
            with Cluster("Research Workflows"):
                research_wf = Python("Comprehensive\nResearch")
                comparative = Python("Comparative\nAnalysis")
            
            with Cluster("Content Workflows"):
                content_wf = Python("Full Content\nPipeline")
                series = Python("Content\nSeries")
            
            with Cluster("Support Workflows"):
                support_wf = Python("Ticket\nLifecycle")
                batch = Python("Batch\nProcessing")
            
            with Cluster("Analytics Workflows"):
                analytics_wf = Python("Business\nAnalysis")
                optimization = Python("Product\nOptimization")
        
        with Cluster("Agent Layer"):
            agents = Python("7 Specialized\nAgents")
        
        with Cluster("Tool Layer"):
            tools = Python("15+ Tools")
        
        with Cluster("LLM Layer"):
            llm = Server("GPT-4 / Claude")
        
        user >> research_wf
        user >> content_wf
        user >> support_wf
        user >> analytics_wf
        
        research_wf >> agents
        content_wf >> agents
        support_wf >> agents
        analytics_wf >> agents
        
        agents >> tools >> llm
        
        llm >> Edge(label="Results") >> user


def generate_all_diagrams():
    """Generate all architecture diagrams"""
    if not DIAGRAMS_AVAILABLE:
        print("\n❌ Cannot generate diagrams. Please install:")
        print("   pip install diagrams")
        print("   brew install graphviz  (on macOS)")
        print("   or visit: https://graphviz.org/download/")
        return
    
    import os
    os.makedirs("docs/diagrams", exist_ok=True)
    
    print("🎨 Generating architecture diagrams...")
    
    diagrams = [
        ("Research Agent", create_research_diagram),
        ("Data Visualization Agent", create_visualization_diagram),
        ("Content Creation Agent", create_content_diagram),
        ("Customer Support Agent", create_support_diagram),
        ("E-commerce Analytics Agent", create_analytics_diagram),
        ("Email Automation Agent", create_email_diagram),
        ("Social Media Agent", create_social_media_diagram),
        ("Overall Architecture", create_overall_architecture),
        ("Workflow Architecture", create_workflow_diagram),
    ]
    
    for name, func in diagrams:
        try:
            print(f"   Creating {name}...")
            func()
            print(f"   ✓ {name} created")
        except Exception as e:
            print(f"   ✗ {name} failed: {e}")
    
    print("\n✅ All diagrams generated in docs/diagrams/")
    print("\nGenerated files:")
    print("   - research_architecture.png")
    print("   - visualization_architecture.png")
    print("   - content_architecture.png")
    print("   - support_architecture.png")
    print("   - analytics_architecture.png")
    print("   - email_architecture.png")
    print("   - social_media_architecture.png")
    print("   - overall_architecture.png")
    print("   - workflow_architecture.png")


if __name__ == "__main__":
    generate_all_diagrams()
