#!/usr/bin/env python3
"""
Advanced Support Agent Tests
============================
Comprehensive testing of all Support Agent capabilities.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from projects.customer_support.agents.support_agent import create_support_agent

# Create outputs directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "advanced_tests")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_json(filename: str, data: dict):
    """Save data as JSON."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved JSON to: {filepath}")
    return filepath


def save_text(filename: str, content: str):
    """Save content as text."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"💾 Saved to: {filepath}")
    return filepath


def test_handle_inquiry():
    """Test handle_inquiry method with customer context."""
    print("\n" + "=" * 80)
    print("TEST 1: Handle Inquiry with Context")
    print("=" * 80)
    
    agent = create_support_agent(model=os.getenv("SUPPORT_MODEL", "gpt-4o-mini"))
    
    # Test inquiry with context
    result = agent.handle_inquiry(
        customer_message="Siparişim 3 gündür beklemede, ne zaman kargoya verilecek?",
        customer_id="CUST-12345",
        context={
            "order_id": "ORD-98765",
            "order_date": "2025-12-15",
            "status": "processing",
            "previous_tickets": 2
        }
    )
    
    print("\n📋 Inquiry Details:")
    print(f"   Customer ID: {result['customer_id']}")
    print(f"   Sentiment: {result['sentiment']}")
    print(f"   Requires Escalation: {result['requires_escalation']}")
    print("\n💬 Response:")
    print(result['response'])
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_json(f"inquiry_result_{timestamp}.json", result)
    
    print("\n" + "=" * 80)
    return result


def test_analyze_ticket():
    """Test ticket analysis and categorization."""
    print("\n" + "=" * 80)
    print("TEST 2: Ticket Analysis & Categorization")
    print("=" * 80)
    
    agent = create_support_agent(model=os.getenv("SUPPORT_MODEL", "gpt-4o-mini"))
    
    # Test different ticket scenarios
    tickets = [
        {
            "ticket_id": "TKT-001",
            "message": "API authentication keeps failing with 401 error. Tried regenerating key, still not working.",
            "priority": "high"
        },
        {
            "ticket_id": "TKT-002",
            "message": "Credit card was charged twice for the same month. Need immediate refund.",
            "priority": "critical"
        },
        {
            "ticket_id": "TKT-003",
            "message": "How do I export my data? Can't find the option in settings.",
            "priority": "low"
        }
    ]
    
    results = []
    for ticket in tickets:
        print(f"\n📋 Analyzing Ticket: {ticket['ticket_id']}")
        print(f"   Priority: {ticket['priority']}")
        print(f"   Message: {ticket['message'][:60]}...")
        
        result = agent.analyze_ticket(
            ticket_id=ticket['ticket_id'],
            message=ticket['message'],
            priority=ticket['priority']
        )
        
        print(f"\n   Escalation Required: {result['requires_escalation']}")
        print(f"\n   Analysis:\n   {result['analysis'][:200]}...")
        
        results.append(result)
    
    # Save all results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_json(f"ticket_analysis_{timestamp}.json", {"tickets": results})
    
    print("\n" + "=" * 80)
    return results


def test_knowledge_base_search():
    """Test knowledge base search functionality."""
    print("\n" + "=" * 80)
    print("TEST 3: Knowledge Base Search")
    print("=" * 80)
    
    agent = create_support_agent(model=os.getenv("SUPPORT_MODEL", "gpt-4o-mini"))
    
    # Test different search queries
    queries = [
        "How to reset password",
        "API rate limits",
        "Payment methods accepted",
        "Data export and backup",
        "Account deletion process"
    ]
    
    results = []
    for query in queries:
        print(f"\n🔍 Searching: {query}")
        
        result = agent.search_knowledge_base(
            query=query,
            max_results=5
        )
        
        print(f"\n   Results:\n   {result['results'][:200]}...")
        results.append(result)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_json(f"kb_search_{timestamp}.json", {"searches": results})
    
    print("\n" + "=" * 80)
    return results


def test_response_templates():
    """Test response template generation."""
    print("\n" + "=" * 80)
    print("TEST 4: Response Template Generation")
    print("=" * 80)
    
    agent = create_support_agent(model=os.getenv("SUPPORT_MODEL", "gpt-4o-mini"))
    
    # Test different scenarios
    scenarios = [
        {"scenario": "Order delay apology", "tone": "empathetic"},
        {"scenario": "Feature not available", "tone": "professional"},
        {"scenario": "Bug report acknowledgment", "tone": "helpful"},
        {"scenario": "Account suspension notice", "tone": "formal"},
        {"scenario": "Welcome message for new users", "tone": "friendly"}
    ]
    
    templates = []
    for item in scenarios:
        print(f"\n📝 Generating template: {item['scenario']}")
        print(f"   Tone: {item['tone']}")
        
        template = agent.generate_response_template(
            scenario=item['scenario'],
            tone=item['tone']
        )
        
        print(f"\n   Template:\n   {template[:200]}...")
        
        templates.append({
            "scenario": item['scenario'],
            "tone": item['tone'],
            "template": template
        })
        
        # Save individual template
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"template_{item['scenario'].replace(' ', '_')}_{timestamp}.txt"
        save_text(filename, template)
    
    # Save all templates
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_json(f"all_templates_{timestamp}.json", {"templates": templates})
    
    print("\n" + "=" * 80)
    return templates


def test_sentiment_detection():
    """Test sentiment analysis on different messages."""
    print("\n" + "=" * 80)
    print("TEST 5: Sentiment Analysis")
    print("=" * 80)
    
    agent = create_support_agent(
        model=os.getenv("SUPPORT_MODEL", "gpt-4o-mini"),
        enable_sentiment_analysis=True
    )
    
    # Test messages with different sentiments
    test_messages = [
        {"text": "I love this product! It's excellent and works great!", "expected": "positive"},
        {"text": "This is terrible. Worst experience ever. Very disappointed.", "expected": "negative"},
        {"text": "The product arrived on time.", "expected": "neutral"},
        {"text": "I'm frustrated with the service. This is unacceptable!", "expected": "negative"},
        {"text": "Thank you so much! You've been very helpful.", "expected": "positive"}
    ]
    
    results = []
    for msg in test_messages:
        sentiment = agent._analyze_sentiment(msg['text'])
        match = "✅" if sentiment == msg['expected'] else "❌"
        
        print(f"\n{match} Message: {msg['text'][:50]}...")
        print(f"   Expected: {msg['expected']}")
        print(f"   Detected: {sentiment}")
        
        results.append({
            "message": msg['text'],
            "expected": msg['expected'],
            "detected": sentiment,
            "correct": sentiment == msg['expected']
        })
    
    # Calculate accuracy
    correct = sum(1 for r in results if r['correct'])
    accuracy = (correct / len(results)) * 100
    
    print(f"\n📊 Sentiment Analysis Accuracy: {accuracy:.1f}%")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_json(f"sentiment_analysis_{timestamp}.json", {
        "results": results,
        "accuracy": accuracy
    })
    
    print("\n" + "=" * 80)
    return results


def test_escalation_detection():
    """Test escalation detection logic."""
    print("\n" + "=" * 80)
    print("TEST 6: Escalation Detection")
    print("=" * 80)
    
    agent = create_support_agent(model=os.getenv("SUPPORT_MODEL", "gpt-4o-mini"))
    
    # Test messages that should and shouldn't escalate
    test_cases = [
        {"text": "I want to speak to your manager immediately!", "should_escalate": True},
        {"text": "This is unacceptable. I will contact my lawyer.", "should_escalate": True},
        {"text": "How do I reset my password?", "should_escalate": False},
        {"text": "Terrible service! I demand a refund immediately!", "should_escalate": True},
        {"text": "Thank you for your help.", "should_escalate": False},
        {"text": "I'm filing a complaint with consumer protection.", "should_escalate": True}
    ]
    
    results = []
    for case in test_cases:
        requires_escalation = agent._check_escalation(case['text'])
        match = "✅" if requires_escalation == case['should_escalate'] else "❌"
        
        print(f"\n{match} Message: {case['text'][:60]}...")
        print(f"   Should Escalate: {case['should_escalate']}")
        print(f"   Detected: {requires_escalation}")
        
        results.append({
            "message": case['text'],
            "expected": case['should_escalate'],
            "detected": requires_escalation,
            "correct": requires_escalation == case['should_escalate']
        })
    
    # Calculate accuracy
    correct = sum(1 for r in results if r['correct'])
    accuracy = (correct / len(results)) * 100
    
    print(f"\n📊 Escalation Detection Accuracy: {accuracy:.1f}%")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_json(f"escalation_detection_{timestamp}.json", {
        "results": results,
        "accuracy": accuracy
    })
    
    print("\n" + "=" * 80)
    return results


def test_multi_language_support():
    """Test support in different languages."""
    print("\n" + "=" * 80)
    print("TEST 7: Multi-Language Support")
    print("=" * 80)
    
    agent = create_support_agent(model=os.getenv("SUPPORT_MODEL", "gpt-4o-mini"))
    
    # Test queries in different languages
    queries = [
        {"query": "Wie kann ich mein Passwort zurücksetzen?", "language": "German", "category": "account"},
        {"query": "Comment puis-je annuler ma commande?", "language": "French", "category": "billing"},
        {"query": "¿Cómo puedo cambiar mi dirección de correo?", "language": "Spanish", "category": "account"},
        {"query": "Come posso contattare il supporto tecnico?", "language": "Italian", "category": "technical"},
        {"query": "Nasıl hesabımı silebilirim?", "language": "Turkish", "category": "account"}
    ]
    
    results = []
    for item in queries:
        print(f"\n🌍 Language: {item['language']}")
        print(f"   Query: {item['query']}")
        
        response = agent.run(
            query=item['query'],
            category=item['category'],
            tone="helpful"
        )
        
        print(f"   Response (first 150 chars): {response[:150]}...")
        
        results.append({
            "language": item['language'],
            "query": item['query'],
            "response": response
        })
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_json(f"multilanguage_{timestamp}.json", {"tests": results})
    
    print("\n" + "=" * 80)
    return results


def main():
    """Run all advanced tests."""
    print("\n" + "=" * 80)
    print("🚀 ADVANCED SUPPORT AGENT TESTS")
    print("=" * 80)
    print(f"\n📁 Outputs: {OUTPUT_DIR}")
    print(f"🤖 Model: {os.getenv('SUPPORT_MODEL', 'gpt-4o-mini')}\n")
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OPENAI_API_KEY not found!")
        sys.exit(1)
    
    try:
        # Run all tests
        print("\n▶️  Starting Test Suite...\n")
        
        test_handle_inquiry()
        input("\nPress Enter to continue...")
        
        test_analyze_ticket()
        input("\nPress Enter to continue...")
        
        test_knowledge_base_search()
        input("\nPress Enter to continue...")
        
        test_response_templates()
        input("\nPress Enter to continue...")
        
        test_sentiment_detection()
        input("\nPress Enter to continue...")
        
        test_escalation_detection()
        input("\nPress Enter to continue...")
        
        test_multi_language_support()
        
        print("\n" + "=" * 80)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print(f"📁 All results saved to: {OUTPUT_DIR}")
        print("=" * 80 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
