#!/usr/bin/env python3
"""
Email Agent Test Script
=======================
Test the Email Agent's capabilities for email generation and management.
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

from projects.email_automation.agents.email_agent import create_email_agent

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


def test_welcome_email():
    """Test welcome email generation."""
    print("=" * 80)
    print("TEST 1: Welcome Email")
    print("=" * 80)
    
    agent = create_email_agent(model=os.getenv("EMAIL_MODEL", "gpt-4o-mini"))
    
    result = agent.run(
        email_type="welcome",
        recipient_name="John Doe",
        company_name="TechCorp",
        tone="friendly"
    )
    
    print("\n📧 Welcome Email:\n")
    print(result)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_output(f"welcome_email_{timestamp}.txt", result)
    
    print("\n" + "=" * 80 + "\n")
    
    return result


def test_promotional_email():
    """Test promotional email generation."""
    print("=" * 80)
    print("TEST 2: Promotional Email")
    print("=" * 80)
    
    agent = create_email_agent(model=os.getenv("EMAIL_MODEL", "gpt-4o-mini"))
    
    result = agent.run(
        email_type="promotional",
        product_name="AI Agent Platform",
        discount="20%",
        cta="Get Started Today",
        tone="exciting"
    )
    
    print("\n🎉 Promotional Email:\n")
    print(result)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_output(f"promotional_email_{timestamp}.txt", result)
    
    print("\n" + "=" * 80 + "\n")
    
    return result


def test_newsletter():
    """Test newsletter generation."""
    print("=" * 80)
    print("TEST 3: Newsletter")
    print("=" * 80)
    
    agent = create_email_agent(model=os.getenv("EMAIL_MODEL", "gpt-4o-mini"))
    
    result = agent.run(
        email_type="newsletter",
        topics=["AI trends", "Product updates", "Community highlights"],
        tone="professional"
    )
    
    print("\n📰 Newsletter:\n")
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_output(f"newsletter_{timestamp}.html", result)
    
    print("\n" + "=" * 80 + "\n")
    
    return result


def test_follow_up_email():
    """Test follow-up email generation."""
    print("=" * 80)
    print("TEST 4: Follow-up Email")
    print("=" * 80)
    
    agent = create_email_agent(model=os.getenv("EMAIL_MODEL", "gpt-4o-mini"))
    
    result = agent.run(
        email_type="follow_up",
        context="demo request",
        recipient_name="Jane Smith",
        tone="professional"
    )
    
    print("\n📨 Follow-up Email:\n")
    print(result)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_output(f"follow_up_email_{timestamp}.txt", result)
    
    print("\n" + "=" * 80 + "\n")
    
    return result


def main():
    """Run all tests."""
    print("\n🚀 Starting Email Agent Tests\n")
    print(f"📁 Outputs will be saved to: {OUTPUT_DIR}\n")
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OPENAI_API_KEY not found in .env file!")
        print("Please set your OpenAI API key in .env file.")
        sys.exit(1)
    
    print(f"✅ Using model: {os.getenv('EMAIL_MODEL', 'gpt-4o-mini')}\n")
    
    try:
        # Run tests
        test_welcome_email()
        input("Press Enter to continue to next test...")
        
        test_promotional_email()
        input("Press Enter to continue to next test...")
        
        test_newsletter()
        input("Press Enter to continue to next test...")
        
        test_follow_up_email()
        
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
