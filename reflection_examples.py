"""
Reflection Examples
===================
Demonstrates how agents can self-evaluate and improve their outputs.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def example_1_basic_reflection():
    """Example 1: Basic reflection on research output"""
    print("\n" + "="*70)
    print("Example 1: Basic Reflection on Research Agent")
    print("="*70)
    
    from projects.research.agent import ResearchAgent
    
    agent = ResearchAgent()
    
    # Get initial output
    query = "What is quantum computing?"
    print(f"\n📝 Query: {query}")
    output = agent.run(query)
    print(f"\n✅ Initial Output:\n{output[:200]}...")
    
    # Reflect on the output
    print(f"\n🔍 Running reflection...")
    reflection = agent.reflect(output)
    
    print(f"\n📊 Reflection Results:")
    print(f"Score: {reflection['score']}/10")
    print(f"\n💪 Strengths:")
    for s in reflection['strengths']:
        print(f"  • {s}")
    print(f"\n⚠️  Weaknesses:")
    for w in reflection['weaknesses']:
        print(f"  • {w}")
    print(f"\n🎯 Improvements:")
    for i in reflection['improvements']:
        print(f"  • {i}")
    
    if reflection['revised_output']:
        print(f"\n✨ Revised Output Available")


def example_2_auto_improvement():
    """Example 2: Automatic improvement with reflection"""
    print("\n" + "="*70)
    print("Example 2: Auto-Improvement with Content Agent")
    print("="*70)
    
    from projects.content_creation.agent import ContentWriterAgent
    
    agent = ContentWriterAgent()
    
    # Run with automatic improvement
    topic = "Benefits of remote work"
    print(f"\n📝 Topic: {topic}")
    print(f"\n🔄 Running with auto-improvement (max 2 iterations)...")
    
    result = agent.run_with_reflection(
        f"Write a short blog intro about {topic}",
        auto_improve=True,
        max_iterations=2
    )
    
    print(f"\n✅ Final Output:\n{result['output'][:300]}...")
    print(f"\n📊 Quality Score: {result['reflection']['score']}/10")
    print(f"🔁 Improvement Iterations: {result['iterations']}")


def example_3_custom_criteria():
    """Example 3: Reflection with custom criteria"""
    print("\n" + "="*70)
    print("Example 3: Custom Evaluation Criteria")
    print("="*70)
    
    from projects.customer_support.agent import SupportAgent
    
    agent = SupportAgent()
    
    # Simulate support ticket
    ticket = "My order hasn't arrived and I'm very frustrated!"
    print(f"\n🎫 Ticket: {ticket}")
    
    response = agent.run(ticket)
    print(f"\n✅ Response:\n{response[:200]}...")
    
    # Reflect with custom criteria specific to support
    custom_criteria = [
        "Empathy and emotional intelligence",
        "Problem-solving effectiveness",
        "Response time appropriateness",
        "Professional and calming tone",
        "Clear next steps provided"
    ]
    
    print(f"\n🔍 Evaluating with support-specific criteria...")
    reflection = agent.reflect(response, criteria=custom_criteria)
    
    print(f"\n📊 Support Quality Score: {reflection['score']}/10")
    print(f"\n💪 Strengths:")
    for s in reflection['strengths']:
        print(f"  • {s}")
    print(f"\n🎯 Improvements:")
    for i in reflection['improvements']:
        print(f"  • {i}")


def example_4_data_visualization_reflection():
    """Example 4: Reflection on chart recommendations"""
    print("\n" + "="*70)
    print("Example 4: Chart Agent Reflection")
    print("="*70)
    
    from projects.data_visualization.agent import ChartAgent
    import pandas as pd
    
    agent = ChartAgent()
    
    # Sample data
    data = pd.DataFrame({
        'month': ['Jan', 'Feb', 'Mar', 'Apr'],
        'sales': [100, 150, 120, 180]
    })
    
    print(f"\n📊 Data: Sales by month")
    print(data)
    
    # Get chart recommendation
    query = "What's the best way to visualize this sales data?"
    output = agent.run(query, data=data)
    print(f"\n✅ Recommendation:\n{output[:250]}...")
    
    # Reflect with visualization-specific criteria
    viz_criteria = [
        "Appropriate chart type selection",
        "Clear explanation of visual reasoning",
        "Consideration of data characteristics",
        "Accessibility and readability",
        "Alternative options discussed"
    ]
    
    reflection = agent.reflect(output, criteria=viz_criteria)
    
    print(f"\n📊 Visualization Recommendation Score: {reflection['score']}/10")
    print(f"\n💪 Strengths:")
    for s in reflection['strengths']:
        print(f"  • {s}")


def example_5_iterative_improvement():
    """Example 5: Multiple rounds of improvement"""
    print("\n" + "="*70)
    print("Example 5: Iterative Improvement Process")
    print("="*70)
    
    from projects.email_automation.agent import EmailAgent
    
    agent = EmailAgent()
    
    # Create initial email
    topic = "New product launch announcement"
    print(f"\n📧 Email Topic: {topic}")
    
    # Round 1
    print(f"\n🔄 Round 1: Initial draft")
    output_v1 = agent.run(f"Write a promotional email subject line and first paragraph for {topic}")
    print(f"Draft: {output_v1[:150]}...")
    
    reflection_v1 = agent.reflect(output_v1)
    print(f"Score: {reflection_v1['score']}/10")
    
    if reflection_v1['revised_output'] and reflection_v1['score'] < 9:
        # Round 2
        print(f"\n🔄 Round 2: Improvement based on feedback")
        output_v2 = reflection_v1['revised_output']
        print(f"Revised: {output_v2[:150]}...")
        
        reflection_v2 = agent.reflect(output_v2)
        print(f"Score: {reflection_v2['score']}/10")
        print(f"Improvement: +{reflection_v2['score'] - reflection_v1['score']:.1f} points")


def example_6_analytics_reflection():
    """Example 6: Analytics agent self-evaluation"""
    print("\n" + "="*70)
    print("Example 6: Analytics Report Reflection")
    print("="*70)
    
    from projects.ecommerce_analytics.agent import AnalyticsAgent
    import pandas as pd
    
    agent = AnalyticsAgent()
    
    # Sample sales data
    data = pd.DataFrame({
        'product': ['A', 'B', 'C', 'D', 'E'],
        'revenue': [5000, 3000, 8000, 2000, 4500],
        'units': [100, 150, 80, 200, 90]
    })
    
    print(f"\n📊 Sales Data:")
    print(data)
    
    query = "Which products are our best performers?"
    output = agent.run(query, data=data)
    print(f"\n✅ Analysis:\n{output[:250]}...")
    
    # Analytics-specific criteria
    analytics_criteria = [
        "Data accuracy and correct calculations",
        "Actionable insights provided",
        "Clear data-driven recommendations",
        "Relevant metrics highlighted",
        "Business context considered"
    ]
    
    reflection = agent.reflect(output, criteria=analytics_criteria)
    
    print(f"\n📊 Analysis Quality Score: {reflection['score']}/10")
    print(f"\n🎯 Key Improvements Suggested:")
    for i in reflection['improvements'][:3]:
        print(f"  • {i}")


def example_7_social_media_reflection():
    """Example 7: Social media post quality check"""
    print("\n" + "="*70)
    print("Example 7: Social Media Content Reflection")
    print("="*70)
    
    from projects.social_media_management.agent import SocialMediaAgent
    
    agent = SocialMediaAgent()
    
    # Create Instagram post
    topic = "Weekend fitness motivation"
    print(f"\n📱 Creating Instagram post: {topic}")
    
    output = agent.run(f"Create an engaging Instagram post about {topic}")
    print(f"\n✅ Generated Post:\n{output[:200]}...")
    
    # Social media specific criteria
    social_criteria = [
        "Engaging and attention-grabbing",
        "Appropriate hashtag usage",
        "Clear call-to-action",
        "Brand voice consistency",
        "Platform-appropriate format",
        "Encourages interaction"
    ]
    
    reflection = agent.reflect(output, criteria=social_criteria)
    
    print(f"\n📊 Social Media Quality Score: {reflection['score']}/10")
    print(f"\n💪 Strengths:")
    for s in reflection['strengths'][:2]:
        print(f"  • {s}")
    print(f"\n🎯 Improvements:")
    for i in reflection['improvements'][:2]:
        print(f"  • {i}")


def main():
    """Run all reflection examples"""
    print("\n" + "="*70)
    print("🔍 AGENT REFLECTION EXAMPLES")
    print("="*70)
    print("\nReflection allows agents to:")
    print("  • Self-evaluate their outputs")
    print("  • Identify strengths and weaknesses")
    print("  • Suggest improvements")
    print("  • Automatically refine responses")
    
    examples = [
        ("Basic Reflection", example_1_basic_reflection),
        ("Auto-Improvement", example_2_auto_improvement),
        ("Custom Criteria", example_3_custom_criteria),
        ("Visualization Reflection", example_4_data_visualization_reflection),
        ("Iterative Improvement", example_5_iterative_improvement),
        ("Analytics Reflection", example_6_analytics_reflection),
        ("Social Media Reflection", example_7_social_media_reflection),
    ]
    
    print(f"\nAvailable examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    choice = input(f"\nSelect example (1-{len(examples)}, or 'all'): ").strip().lower()
    
    if choice == 'all':
        for name, func in examples:
            try:
                func()
                input("\nPress Enter to continue...")
            except Exception as e:
                print(f"\n❌ Error in {name}: {e}")
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        try:
            examples[int(choice)-1][1]()
        except Exception as e:
            print(f"\n❌ Error: {e}")
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()
