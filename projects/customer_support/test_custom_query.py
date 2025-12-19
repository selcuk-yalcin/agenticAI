#!/usr/bin/env python3
"""
Custom Support Query Test
=========================
Test Support Agent with custom customer queries.
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

from projects.customer_support.agents.support_agent import create_support_agent

# Create outputs directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def test_custom_query(query: str, category: str = "general", tone: str = "helpful"):
    """
    Test Support Agent with a custom query.
    
    Args:
        query: Customer question/issue
        category: technical, billing, product, troubleshooting, account, general
        tone: helpful, empathetic, patient, professional, friendly
    """
    print("\n" + "=" * 80)
    print("🎯 CUSTOM SUPPORT QUERY TEST")
    print("=" * 80)
    
    print(f"\n📝 Customer Query:")
    print(f"   {query}")
    print(f"\n🏷️  Category: {category}")
    print(f"🎨 Tone: {tone}")
    print("\n" + "-" * 80)
    
    # Create agent
    agent = create_support_agent(model=os.getenv("SUPPORT_MODEL", "gpt-4o-mini"))
    
    # Get response
    print("\n⏳ Processing...")
    result = agent.run(
        query=query,
        category=category,
        tone=tone
    )
    
    # Display response
    print("\n💬 Support Agent Response:")
    print("-" * 80)
    print(result)
    print("-" * 80)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"custom_query_{category}_{timestamp}.txt"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"CUSTOMER QUERY:\n{query}\n\n")
        f.write(f"CATEGORY: {category}\n")
        f.write(f"TONE: {tone}\n")
        f.write(f"\n{'=' * 80}\n\n")
        f.write(f"SUPPORT RESPONSE:\n{result}\n")
    
    print(f"\n💾 Saved to: {filepath}")
    print("=" * 80 + "\n")
    
    return result


def interactive_mode():
    """Interactive mode for testing multiple queries."""
    print("\n" + "=" * 80)
    print("🤖 SUPPORT AGENT - INTERACTIVE TEST MODE")
    print("=" * 80)
    print("\nTest the Support Agent with your own queries!")
    print("Type 'exit' or 'quit' to stop.\n")
    
    agent = create_support_agent(model=os.getenv("SUPPORT_MODEL", "gpt-4o-mini"))
    
    while True:
        print("-" * 80)
        query = input("\n❓ Enter customer query: ").strip()
        
        if query.lower() in ['exit', 'quit', 'q']:
            print("\n👋 Exiting interactive mode...")
            break
        
        if not query:
            print("⚠️  Please enter a query.")
            continue
        
        # Ask for category
        print("\n🏷️  Select category:")
        print("   1. Technical")
        print("   2. Billing")
        print("   3. Product")
        print("   4. Troubleshooting")
        print("   5. Account")
        print("   6. General")
        
        category_choice = input("\nEnter number (default: 6): ").strip() or "6"
        categories = {
            "1": "technical",
            "2": "billing",
            "3": "product",
            "4": "troubleshooting",
            "5": "account",
            "6": "general"
        }
        category = categories.get(category_choice, "general")
        
        # Ask for tone
        print("\n🎨 Select tone:")
        print("   1. Helpful")
        print("   2. Empathetic")
        print("   3. Patient")
        print("   4. Professional")
        print("   5. Friendly")
        
        tone_choice = input("\nEnter number (default: 1): ").strip() or "1"
        tones = {
            "1": "helpful",
            "2": "empathetic",
            "3": "patient",
            "4": "professional",
            "5": "friendly"
        }
        tone = tones.get(tone_choice, "helpful")
        
        # Get response
        print("\n⏳ Processing...\n")
        result = agent.run(query=query, category=category, tone=tone)
        
        print("\n💬 Support Agent Response:")
        print("-" * 80)
        print(result)
        print("-" * 80)
        
        # Save option
        save = input("\n💾 Save this response? (y/n): ").strip().lower()
        if save == 'y':
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"interactive_{category}_{timestamp}.txt"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"CUSTOMER QUERY:\n{query}\n\n")
                f.write(f"CATEGORY: {category}\n")
                f.write(f"TONE: {tone}\n")
                f.write(f"\n{'=' * 80}\n\n")
                f.write(f"SUPPORT RESPONSE:\n{result}\n")
            
            print(f"✅ Saved to: {filepath}")


def main():
    """Main function with example queries."""
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OPENAI_API_KEY not found in .env file!")
        sys.exit(1)
    
    print("\n🚀 Custom Support Query Tester")
    print(f"📁 Outputs: {OUTPUT_DIR}")
    print(f"🤖 Model: {os.getenv('SUPPORT_MODEL', 'gpt-4o-mini')}\n")
    
    # Ask user what they want to do
    print("Choose an option:")
    print("1. Test with example queries")
    print("2. Interactive mode (enter your own queries)")
    print("3. Single custom query")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        # Example queries
        print("\n📚 Running Example Queries...\n")
        
        # Example 1: Account access issue
        test_custom_query(
            query="Hesabıma giriş yapamıyorum. Şifremi unuttum ve sıfırlama maili gelmiyor.",
            category="account",
            tone="empathetic"
        )
        
        input("Press Enter for next example...")
        
        # Example 2: Feature request
        test_custom_query(
            query="Ürününüze mobil uygulama ekleyecek misiniz? Telefondan kullanmak çok daha kolay olurdu.",
            category="product",
            tone="professional"
        )
        
        input("Press Enter for next example...")
        
        # Example 3: Integration question
        test_custom_query(
            query="API'nizi Slack ile entegre edebilir miyim? Dokümantasyonda örnek bulamadım.",
            category="technical",
            tone="helpful"
        )
        
    elif choice == "2":
        interactive_mode()
        
    elif choice == "3":
        query = input("\n❓ Enter your query: ").strip()
        if query:
            category = input("📋 Category (technical/billing/product/general): ").strip() or "general"
            tone = input("🎨 Tone (helpful/empathetic/patient): ").strip() or "helpful"
            test_custom_query(query, category, tone)
    
    print("\n✅ Done!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Test interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
