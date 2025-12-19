#!/usr/bin/env python3
"""
Support Agent Test Script
=========================
Test the Support Agent's capabilities for customer support.
"""

import os
import sys
import argparse
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from projects.customer_support.agents.support_agent import create_support_agent

# Create outputs directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Global verbose flag
VERBOSE = False


def log_verbose(message: str):
    """Print verbose message if verbose mode is enabled."""
    if VERBOSE:
        print(f"🔍 [VERBOSE] {message}")


def save_output(filename: str, content: str):
    """Save output to file."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    log_verbose(f"Saving output to {filepath}")
    log_verbose(f"Content length: {len(content)} characters")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"💾 Saved to: {filepath}")
    return filepath


def test_technical_support():
    """Test technical support response."""
    print("=" * 80)
    print("TEST 1: Technical Support Query")
    print("=" * 80)
    
    log_verbose("Creating Support Agent...")
    log_verbose(f"Model: {os.getenv('SUPPORT_MODEL', 'gpt-4o-mini')}")
    agent = create_support_agent(model=os.getenv("SUPPORT_MODEL", "gpt-4o-mini"))
    
    log_verbose("Sending query to agent...")
    log_verbose("Query: 'My API key is not working. I keep getting 401 errors.'")
    log_verbose("Category: technical")
    log_verbose("Tone: helpful")
    
    result = agent.run(
        query="My API key is not working. I keep getting 401 errors.",
        category="technical",
        tone="helpful"
    )
    
    log_verbose(f"Response received, length: {len(result)} characters")
    print("\n🔧 Technical Support Response:\n")
    print(result)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_output(f"technical_support_{timestamp}.txt", result)
    
    print("\n" + "=" * 80 + "\n")
    
    return result


def test_billing_support():
    """Test billing support response."""
    print("=" * 80)
    print("TEST 2: Billing Support Query")
    print("=" * 80)
    
    log_verbose("Creating Support Agent...")
    agent = create_support_agent(model=os.getenv("SUPPORT_MODEL", "gpt-4o-mini"))
    log_verbose("Billing support query starting...")
    
    result = agent.run(
        query="I was charged twice for my subscription this month.",
        category="billing",
        tone="empathetic"
    )
    
    print("\n💳 Billing Support Response:\n")
    print(result)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_output(f"billing_support_{timestamp}.txt", result)
    
    print("\n" + "=" * 80 + "\n")
    
    return result


def test_product_inquiry():
    """Test product inquiry response."""
    print("=" * 80)
    print("TEST 3: Product Inquiry")
    print("=" * 80)
    
    agent = create_support_agent(model=os.getenv("SUPPORT_MODEL", "gpt-4o-mini"))
    
    result = agent.run(
        query="What are the differences between your Basic and Pro plans?",
        category="product",
        tone="informative"
    )
    
    print("\n📦 Product Inquiry Response:\n")
    print(result)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_output(f"product_inquiry_{timestamp}.txt", result)
    
    print("\n" + "=" * 80 + "\n")
    
    return result


def test_troubleshooting():
    """Test troubleshooting with step-by-step guidance."""
    print("=" * 80)
    print("TEST 4: Troubleshooting Guide")
    print("=" * 80)
    
    agent = create_support_agent(model=os.getenv("SUPPORT_MODEL", "gpt-4o-mini"))
    
    result = agent.run(
        query="The agent is not returning any results. How do I debug this?",
        category="troubleshooting",
        tone="patient",
        include_steps=True
    )
    
    print("\n🔍 Troubleshooting Guide:\n")
    print(result)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_output(f"troubleshooting_{timestamp}.txt", result)
    
    print("\n" + "=" * 80 + "\n")
    
    return result


def main():
    """Run all tests."""
    global VERBOSE
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Test Support Agent with various scenarios')
    parser.add_argument('-v', '--verbose', action='store_true', 
                        help='Enable verbose output with detailed logs')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug logging')
    args = parser.parse_args()
    
    VERBOSE = args.verbose or args.debug
    
    # Setup logging if debug mode
    if args.debug:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        log_verbose("Debug logging enabled")
    
    print("\n🚀 Starting Support Agent Tests\n")
    if VERBOSE:
        print("📢 VERBOSE MODE ENABLED\n")
    print(f"📁 Outputs will be saved to: {OUTPUT_DIR}\n")
    
    # Check API key
    log_verbose("Checking for OPENAI_API_KEY...")
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OPENAI_API_KEY not found in .env file!")
        print("Please set your OpenAI API key in .env file.")
        sys.exit(1)
    log_verbose("API key found ✓")
    
    print(f"✅ Using model: {os.getenv('SUPPORT_MODEL', 'gpt-4o-mini')}\n")
    log_verbose(f"Temperature: 0.3 (default for support agent)")
    log_verbose(f"Output directory: {OUTPUT_DIR}")
    
    try:
        # Run tests
        test_technical_support()
        input("Press Enter to continue to next test...")
        
        test_billing_support()
        input("Press Enter to continue to next test...")
        
        test_product_inquiry()
        input("Press Enter to continue to next test...")
        
        test_troubleshooting()
        
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
