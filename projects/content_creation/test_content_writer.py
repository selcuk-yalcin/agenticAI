#!/usr/bin/env python3
"""
Content Writer Agent Test Script
================================
Simple test to verify Content Writer Agent functionality.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from projects.content_creation.agents.content_writer_agent import create_content_writer_agent

# Create outputs directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_output(filename: str, content: str):
    """Save output to file."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"💾 Saved to: {filepath}")
    return filepath


def test_blog_post():
    """Test blog post generation."""
    print("=" * 80)
    print("TEST 1: Blog Post Generation")
    print("=" * 80)
    
    agent = create_content_writer_agent(model=os.getenv("CONTENT_MODEL", "gpt-4o-mini"))
    
    result = agent.run(
        topic="Benefits of AI in Content Creation",
        content_type="blog_post",
        word_count=500,
        tone="professional",
        keywords=["AI", "content creation", "automation", "efficiency"]
    )
    
    print("\n📝 Generated Blog Post:\n")
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_output(f"blog_post_{timestamp}.md", result)
    
    print("\n" + "=" * 80 + "\n")
    
    return result


def test_social_post():
    """Test social media post generation."""
    print("=" * 80)
    print("TEST 2: Social Media Post Generation")
    print("=" * 80)
    
    agent = create_content_writer_agent(model=os.getenv("CONTENT_MODEL", "gpt-4o-mini"))
    
    result = agent.run(
        topic="New AI Agent System Launch",
        content_type="social_post",
        platform="twitter",
        tone="exciting"
    )
    
    print("\n🐦 Generated Social Post:\n")
    print(result)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_output(f"social_post_{timestamp}.txt", result)
    
    print("\n" + "=" * 80 + "\n")
    
    return result


def test_landing_page():
    """Test landing page copy generation."""
    print("=" * 80)
    print("TEST 3: Landing Page Copy Generation")
    print("=" * 80)
    
    agent = create_content_writer_agent(model=os.getenv("CONTENT_MODEL", "gpt-4o-mini"))
    
    result = agent.run(
        topic="AI Agent Platform for Developers",
        content_type="landing_page",
        tone="professional",
        sections=["hero", "features", "cta"]
    )
    
    print("\n🚀 Generated Landing Page:\n")
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_output(f"landing_page_{timestamp}.html", result)
    
    print("\n" + "=" * 80 + "\n")
    
    return result


def test_with_reflection():
    """Test content generation with reflection for quality improvement."""
    print("=" * 80)
    print("TEST 4: Blog Post with Reflection (Auto-Improvement)")
    print("=" * 80)
    
    agent = create_content_writer_agent(model=os.getenv("CONTENT_MODEL", "gpt-4o-mini"))
    
    result = agent.run_with_reflection(
        user_input="Write a 300-word blog post about the future of AI agents in a professional tone",
        max_iterations=2,
        auto_improve=True
    )
    
    print("\n✨ Generated Blog Post (with reflection):\n")
    if isinstance(result, dict):
        output = result.get('output', str(result))
        print(output[:500] + "..." if len(output) > 500 else output)
    else:
        print(result[:500] + "..." if len(result) > 500 else result)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    content_to_save = result.get('output', str(result)) if isinstance(result, dict) else result
    save_output(f"blog_post_reflected_{timestamp}.md", content_to_save)
    
    print("\n" + "=" * 80 + "\n")
    
    return result


def main():
    """Run all tests."""
    print("\n🚀 Starting Content Writer Agent Tests\n")
    print(f"📁 Outputs will be saved to: {OUTPUT_DIR}\n")
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OPENAI_API_KEY not found in .env file!")
        print("Please set your OpenAI API key in .env file.")
        sys.exit(1)
    
    print(f"✅ Using model: {os.getenv('CONTENT_MODEL', 'gpt-4o-mini')}\n")
    
    try:
        # Run tests
        test_blog_post()
        input("Press Enter to continue to next test...")
        
        test_social_post()
        input("Press Enter to continue to next test...")
        
        test_landing_page()
        input("Press Enter to continue to next test...")
        
        test_with_reflection()
        
        print("\n" + "=" * 80)
        print("✅ All tests completed successfully!")
        print(f"📁 All outputs saved to: {OUTPUT_DIR}")
        print("=" * 80)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
