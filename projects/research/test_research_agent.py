#!/usr/bin/env python3
"""
Research Agent Test Script
==========================
Test the Research Agent's capabilities for web research and report generation.
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

from projects.research.agents.research_agent import create_research_agent

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


def test_web_research():
    """Test web research capability."""
    print("=" * 80)
    print("TEST 1: Web Research")
    print("=" * 80)
    
    agent = create_research_agent(model=os.getenv("RESEARCH_MODEL", "gpt-4o-mini"))
    
    result = agent.run(
        query="Latest trends in AI agents and autonomous systems",
        depth="comprehensive",
        include_citations=True
    )
    
    print("\n🔍 Research Results:\n")
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_output(f"web_research_{timestamp}.md", result)
    
    print("\n" + "=" * 80 + "\n")
    
    return result


def test_arxiv_research():
    """Test arXiv research capability."""
    print("=" * 80)
    print("TEST 2: arXiv Research")
    print("=" * 80)
    
    agent = create_research_agent(model=os.getenv("RESEARCH_MODEL", "gpt-4o-mini"))
    
    result = agent.run(
        query="Machine learning optimization techniques",
        sources=["arxiv"],
        max_results=5
    )
    
    print("\n📚 arXiv Research Results:\n")
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_output(f"arxiv_research_{timestamp}.md", result)
    
    print("\n" + "=" * 80 + "\n")
    
    return result


def test_wikipedia_research():
    """Test Wikipedia research capability."""
    print("=" * 80)
    print("TEST 3: Wikipedia Research")
    print("=" * 80)
    
    agent = create_research_agent(model=os.getenv("RESEARCH_MODEL", "gpt-4o-mini"))
    
    result = agent.run(
        query="Artificial intelligence history and development",
        sources=["wikipedia"],
        depth="basic"
    )
    
    print("\n📖 Wikipedia Research Results:\n")
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_output(f"wikipedia_research_{timestamp}.md", result)
    
    print("\n" + "=" * 80 + "\n")
    
    return result


def test_comprehensive_report():
    """Test comprehensive research report generation."""
    print("=" * 80)
    print("TEST 4: Comprehensive Research Report")
    print("=" * 80)
    
    agent = create_research_agent(model=os.getenv("RESEARCH_MODEL", "gpt-4o-mini"))
    
    result = agent.run(
        query="Impact of AI on software development",
        depth="comprehensive",
        format="report",
        include_citations=True
    )
    
    print("\n📊 Comprehensive Report:\n")
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_output(f"comprehensive_report_{timestamp}.md", result)
    
    print("\n" + "=" * 80 + "\n")
    
    return result


def main():
    """Run all tests."""
    print("\n🚀 Starting Research Agent Tests\n")
    print(f"📁 Outputs will be saved to: {OUTPUT_DIR}\n")
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OPENAI_API_KEY not found in .env file!")
        print("Please set your OpenAI API key in .env file.")
        sys.exit(1)
    
    print(f"✅ Using model: {os.getenv('RESEARCH_MODEL', 'gpt-4o-mini')}\n")
    
    try:
        # Run tests
        test_web_research()
        input("Press Enter to continue to next test...")
        
        test_arxiv_research()
        input("Press Enter to continue to next test...")
        
        test_wikipedia_research()
        input("Press Enter to continue to next test...")
        
        test_comprehensive_report()
        
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
