#!/usr/bin/env python3
"""
Social Media Agent Test Script
==============================
Test the Social Media Agent's capabilities for social media content management.
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

from projects.social_media_management.agents.social_media_agent import create_social_media_agent

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


def test_twitter_post():
    """Test Twitter post generation."""
    print("=" * 80)
    print("TEST 1: Twitter Post")
    print("=" * 80)
    
    agent = create_social_media_agent(model=os.getenv("SOCIAL_MODEL", "gpt-4o-mini"))
    
    result = agent.run(
        platform="twitter",
        topic="Launching our new AI agent platform",
        tone="exciting",
        include_hashtags=True
    )
    
    print("\n🐦 Twitter Post:\n")
    print(result)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_output(f"twitter_post_{timestamp}.txt", result)
    
    print("\n" + "=" * 80 + "\n")
    
    return result


def test_linkedin_post():
    """Test LinkedIn post generation."""
    print("=" * 80)
    print("TEST 2: LinkedIn Post")
    print("=" * 80)
    
    agent = create_social_media_agent(model=os.getenv("SOCIAL_MODEL", "gpt-4o-mini"))
    
    result = agent.run(
        platform="linkedin",
        topic="The future of AI in enterprise software",
        tone="professional",
        length="medium"
    )
    
    print("\n💼 LinkedIn Post:\n")
    print(result)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_output(f"linkedin_post_{timestamp}.txt", result)
    
    print("\n" + "=" * 80 + "\n")
    
    return result


def test_instagram_caption():
    """Test Instagram caption generation."""
    print("=" * 80)
    print("TEST 3: Instagram Caption")
    print("=" * 80)
    
    agent = create_social_media_agent(model=os.getenv("SOCIAL_MODEL", "gpt-4o-mini"))
    
    result = agent.run(
        platform="instagram",
        topic="Behind the scenes at our AI lab",
        tone="casual",
        include_hashtags=True,
        include_emojis=True
    )
    
    print("\n📸 Instagram Caption:\n")
    print(result)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_output(f"instagram_caption_{timestamp}.txt", result)
    
    print("\n" + "=" * 80 + "\n")
    
    return result


def test_content_calendar():
    """Test social media content calendar generation."""
    print("=" * 80)
    print("TEST 4: Content Calendar (7 days)")
    print("=" * 80)
    
    agent = create_social_media_agent(model=os.getenv("SOCIAL_MODEL", "gpt-4o-mini"))
    
    result = agent.run(
        task="content_calendar",
        theme="AI and Innovation",
        platforms=["twitter", "linkedin"],
        duration_days=7
    )
    
    print("\n📅 Content Calendar:\n")
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_output(f"content_calendar_{timestamp}.md", result)
    
    print("\n" + "=" * 80 + "\n")
    
    return result


def main():
    """Run all tests."""
    print("\n🚀 Starting Social Media Agent Tests\n")
    print(f"📁 Outputs will be saved to: {OUTPUT_DIR}\n")
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OPENAI_API_KEY not found in .env file!")
        print("Please set your OpenAI API key in .env file.")
        sys.exit(1)
    
    print(f"✅ Using model: {os.getenv('SOCIAL_MODEL', 'gpt-4o-mini')}\n")
    
    try:
        # Run tests
        test_twitter_post()
        input("Press Enter to continue to next test...")
        
        test_linkedin_post()
        input("Press Enter to continue to next test...")
        
        test_instagram_caption()
        input("Press Enter to continue to next test...")
        
        test_content_calendar()
        
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
