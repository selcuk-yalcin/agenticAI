#!/usr/bin/env python3
"""
Advanced Email Automation Tests
================================
Comprehensive testing of Email Agent capabilities.
"""

import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from projects.email_automation.agents.email_agent import create_email_agent

# Create outputs directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "advanced_tests")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_result(filename: str, content: str):
    """Save test result to file."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        if isinstance(content, dict):
            f.write(json.dumps(content, indent=2, ensure_ascii=False))
        else:
            f.write(str(content))
    print(f"💾 Saved to: {filepath}")
    return filepath


def test_welcome_email_series():
    """Test 1: Welcome email sequence for new customers."""
    print("\n" + "=" * 80)
    print("TEST 1: Welcome Email Series")
    print("=" * 80)
    
    agent = create_email_agent(
        model=os.getenv("EMAIL_MODEL", "gpt-4o-mini"),
        temperature=0.7,
        enable_personalization=True
    )
    
    print("\n📧 Creating welcome email sequence...")
    print(f"   Campaign: Onboarding")
    print(f"   Emails: 3")
    print(f"   Interval: 2 days")
    
    result = agent.create_email_sequence(
        campaign_type="New Customer Welcome and Onboarding",
        num_emails=3,
        interval_days=2
    )
    
    print(f"\n✅ Sequence Created:")
    print(f"   Campaign: {result['campaign_type']}")
    print(f"   Total Emails: {result['num_emails']}")
    print(f"\n📋 Preview (first 400 chars):\n{str(result['sequence'])[:400]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"welcome_email_series_{timestamp}.json", result)
    
    print("\n" + "=" * 80)
    return result


def test_abandoned_cart_recovery():
    """Test 2: Abandoned cart recovery email sequence."""
    print("\n" + "=" * 80)
    print("TEST 2: Abandoned Cart Recovery")
    print("=" * 80)
    
    agent = create_email_agent(
        model=os.getenv("EMAIL_MODEL", "gpt-4o-mini"),
        temperature=0.7,
        enable_personalization=True
    )
    
    print("\n🛒 Creating cart recovery sequence...")
    print(f"   Timing: 1 hour, 24 hours, 3 days")
    print(f"   Goal: Recover abandoned purchases")
    
    result = agent.create_email_sequence(
        campaign_type="Abandoned Cart Recovery with Progressive Incentives",
        num_emails=3,
        interval_days=1
    )
    
    print(f"\n✅ Recovery Sequence Created:")
    print(f"   Emails: {result['num_emails']}")
    print(f"\n📋 Preview (first 400 chars):\n{str(result['sequence'])[:400]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"abandoned_cart_recovery_{timestamp}.json", result)
    
    print("\n" + "=" * 80)
    return result


def test_personalized_recommendations():
    """Test 3: Personalized product recommendation emails."""
    print("\n" + "=" * 80)
    print("TEST 3: Personalized Product Recommendations")
    print("=" * 80)
    
    agent = create_email_agent(
        model=os.getenv("EMAIL_MODEL", "gpt-4o-mini"),
        temperature=0.7,
        enable_personalization=True
    )
    
    # Test for VIP customer
    print("\n🎁 Creating personalized recommendation email...")
    print(f"   Recipient: Sarah Johnson (VIP)")
    print(f"   Segment: VIP Electronics Enthusiast")
    
    result = agent.compose_personalized_email(
        recipient_name="Sarah Johnson",
        recipient_segment="VIP - Electronics Enthusiast",
        occasion="Monthly personalized recommendations",
        include_recommendations=True
    )
    
    print(f"\n✅ Personalized Email Created:")
    print(f"   Recipient: {result['recipient']}")
    print(f"   Segment: {result['segment']}")
    print(f"   Personalized: {result['personalized']}")
    print(f"\n📧 Preview (first 400 chars):\n{str(result['content'])[:400]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"personalized_recommendations_{timestamp}.json", result)
    
    print("\n" + "=" * 80)
    return result


def test_ab_testing_variants():
    """Test 4: A/B test variants for email optimization."""
    print("\n" + "=" * 80)
    print("TEST 4: A/B Test Variants")
    print("=" * 80)
    
    agent = create_email_agent(
        model=os.getenv("EMAIL_MODEL", "gpt-4o-mini"),
        temperature=0.7
    )
    
    base_email = """
    Subject: Don't miss out on our sale!
    
    Hi there,
    
    We're having a sale this weekend with up to 50% off on selected items.
    Check out our website to see all deals.
    
    Shop now!
    """
    
    print("\n🧪 Creating A/B test variants...")
    print(f"   Base email: Sale announcement")
    print(f"   Test element: Subject line")
    print(f"   Variants: 3")
    
    result = agent.generate_ab_variants(
        base_email=base_email,
        test_element="subject_line",
        num_variants=3
    )
    
    print(f"\n✅ Variants Created:")
    print(f"   Test Element: {result['test_element']}")
    print(f"   Number of Variants: {result['num_variants']}")
    print(f"\n📊 Preview (first 400 chars):\n{str(result['variants'])[:400]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"ab_test_variants_{timestamp}.json", result)
    
    print("\n" + "=" * 80)
    return result


def test_reengagement_campaign():
    """Test 5: Re-engagement campaign for inactive customers."""
    print("\n" + "=" * 80)
    print("TEST 5: Re-engagement Campaign")
    print("=" * 80)
    
    agent = create_email_agent(
        model=os.getenv("EMAIL_MODEL", "gpt-4o-mini"),
        temperature=0.7,
        enable_personalization=True
    )
    
    print("\n🔄 Creating re-engagement sequence...")
    print(f"   Target: Inactive customers (90+ days)")
    print(f"   Strategy: Win-back with incentives")
    
    result = agent.create_email_sequence(
        campaign_type="Customer Re-engagement and Win-back for 90-day Inactive Users",
        num_emails=4,
        interval_days=5
    )
    
    print(f"\n✅ Re-engagement Sequence Created:")
    print(f"   Emails: {result['num_emails']}")
    print(f"   Interval: {result['interval_days']} days")
    print(f"\n📧 Preview (first 400 chars):\n{str(result['sequence'])[:400]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"reengagement_campaign_{timestamp}.json", result)
    
    print("\n" + "=" * 80)
    return result


def test_seasonal_promotions():
    """Test 6: Seasonal promotion emails (Holiday, Black Friday, etc)."""
    print("\n" + "=" * 80)
    print("TEST 6: Seasonal Promotion Emails")
    print("=" * 80)
    
    agent = create_email_agent(
        model=os.getenv("EMAIL_MODEL", "gpt-4o-mini"),
        temperature=0.7
    )
    
    # Black Friday email
    print("\n🎉 Creating Black Friday promotion email...")
    
    result = agent.compose_email(
        email_type="promotional",
        subject_style="urgent and exciting",
        tone="energetic",
        purpose="Black Friday Sale - 24 hours only, up to 70% off"
    )
    
    print(f"\n✅ Promotional Email Created:")
    print(f"   Type: {result['type']}")
    print(f"   Tone: {result['metadata']['tone']}")
    print(f"   Purpose: {result['metadata']['purpose']}")
    print(f"\n📧 Preview (first 400 chars):\n{str(result['content'])[:400]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"seasonal_black_friday_{timestamp}.json", result)
    
    print("\n" + "=" * 80)
    return result


def test_newsletter_content():
    """Test 7: Monthly newsletter with multiple topics."""
    print("\n" + "=" * 80)
    print("TEST 7: Monthly Newsletter")
    print("=" * 80)
    
    agent = create_email_agent(
        model=os.getenv("EMAIL_MODEL", "gpt-4o-mini"),
        temperature=0.7
    )
    
    topics = [
        "New Product Launches",
        "Customer Success Stories",
        "Industry Trends",
        "Company Updates",
        "Upcoming Events"
    ]
    
    print("\n📰 Creating monthly newsletter...")
    print(f"   Topics: {len(topics)}")
    print(f"   Sections: Intro, Main Content, Updates, CTA")
    
    result = agent.generate_newsletter(
        topics=topics,
        tone="informative and friendly",
        include_sections=["intro", "featured_story", "main_content", "quick_updates", "events", "cta"]
    )
    
    print(f"\n✅ Newsletter Created:")
    print(f"   Topics: {', '.join(result['topics'][:3])}...")
    print(f"   Sections: {len(result['sections'])}")
    print(f"\n📰 Preview (first 400 chars):\n{str(result['content'])[:400]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"monthly_newsletter_{timestamp}.json", result)
    
    print("\n" + "=" * 80)
    return result


def test_transactional_emails():
    """Test 8: Transactional emails (order confirmation, shipping, etc)."""
    print("\n" + "=" * 80)
    print("TEST 8: Transactional Emails")
    print("=" * 80)
    
    agent = create_email_agent(
        model=os.getenv("EMAIL_MODEL", "gpt-4o-mini"),
        temperature=0.3  # Lower temperature for factual content
    )
    
    # Order confirmation
    print("\n📦 Creating order confirmation email...")
    
    order_details = {
        "order_number": "ORD-123456",
        "order_date": "December 19, 2025",
        "items": [
            {"name": "Wireless Headphones", "quantity": 1, "price": "$100"},
            {"name": "USB-C Cable", "quantity": 2, "price": "$30"}
        ],
        "subtotal": "$130",
        "shipping": "$10",
        "total": "$140",
        "shipping_address": "123 Main St, San Francisco, CA 94102",
        "estimated_delivery": "December 23-25, 2025"
    }
    
    result = agent.create_transactional_email(
        transaction_type="Order Confirmation",
        order_details=order_details
    )
    
    print(f"\n✅ Transactional Email Created:")
    print(f"   Type: {result['type']}")
    print(f"   Transactional: {result['transactional']}")
    print(f"\n📧 Preview (first 400 chars):\n{str(result['content'])[:400]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"transactional_order_confirmation_{timestamp}.json", result)
    
    print("\n" + "=" * 80)
    return result


def test_subject_line_optimization():
    """Test 9: Subject line optimization for better open rates."""
    print("\n" + "=" * 80)
    print("TEST 9: Subject Line Optimization")
    print("=" * 80)
    
    agent = create_email_agent(
        model=os.getenv("EMAIL_MODEL", "gpt-4o-mini"),
        temperature=0.7
    )
    
    test_subjects = [
        "Newsletter #47",
        "Check out our products",
        "Important update",
        "Sale happening now"
    ]
    
    results = []
    
    for subject in test_subjects:
        print(f"\n📊 Optimizing: '{subject}'")
        
        result = agent.optimize_subject_line(
            subject=subject,
            goal="higher_open_rate"
        )
        
        results.append(result)
        print(f"   ✅ Optimization complete")
    
    print(f"\n✅ Optimized {len(results)} Subject Lines")
    print(f"\n📈 Example (first result, first 400 chars):\n{str(results[0]['optimization'])[:400]}...")
    
    # Save all results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"subject_line_optimizations_{timestamp}.json", {"optimizations": results})
    
    print("\n" + "=" * 80)
    return results


def test_loyalty_program():
    """Test 10: Loyalty program and VIP customer emails."""
    print("\n" + "=" * 80)
    print("TEST 10: Loyalty Program Communications")
    print("=" * 80)
    
    agent = create_email_agent(
        model=os.getenv("EMAIL_MODEL", "gpt-4o-mini"),
        temperature=0.7,
        enable_personalization=True
    )
    
    print("\n⭐ Creating VIP loyalty email...")
    
    result = agent.compose_personalized_email(
        recipient_name="Michael Chen",
        recipient_segment="VIP Platinum Member - 3 Year Anniversary",
        occasion="Loyalty Program Milestone and Exclusive Rewards",
        include_recommendations=True
    )
    
    print(f"\n✅ VIP Email Created:")
    print(f"   Recipient: {result['recipient']}")
    print(f"   Segment: {result['segment']}")
    print(f"\n💎 Preview (first 400 chars):\n{str(result['content'])[:400]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"loyalty_vip_program_{timestamp}.json", result)
    
    print("\n" + "=" * 80)
    return result


def test_feedback_surveys():
    """Test 11: Post-purchase feedback and survey emails."""
    print("\n" + "=" * 80)
    print("TEST 11: Feedback and Survey Emails")
    print("=" * 80)
    
    agent = create_email_agent(
        model=os.getenv("EMAIL_MODEL", "gpt-4o-mini"),
        temperature=0.7
    )
    
    print("\n📝 Creating post-purchase feedback email...")
    
    result = agent.compose_email(
        email_type="feedback_request",
        subject_style="friendly and appreciative",
        tone="warm and genuine",
        purpose="Request feedback and review for recent purchase, offer incentive for completion"
    )
    
    print(f"\n✅ Feedback Email Created:")
    print(f"   Type: {result['type']}")
    print(f"   Tone: {result['metadata']['tone']}")
    print(f"\n📝 Preview (first 400 chars):\n{str(result['content'])[:400]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"feedback_survey_{timestamp}.json", result)
    
    print("\n" + "=" * 80)
    return result


def test_upsell_crosssell():
    """Test 12: Upsell and cross-sell email campaigns."""
    print("\n" + "=" * 80)
    print("TEST 12: Upsell & Cross-sell Campaigns")
    print("=" * 80)
    
    agent = create_email_agent(
        model=os.getenv("EMAIL_MODEL", "gpt-4o-mini"),
        temperature=0.7,
        enable_personalization=True
    )
    
    print("\n💰 Creating upsell/cross-sell sequence...")
    
    result = agent.create_email_sequence(
        campaign_type="Post-Purchase Upsell and Cross-sell Recommendations",
        num_emails=2,
        interval_days=7
    )
    
    print(f"\n✅ Upsell Sequence Created:")
    print(f"   Emails: {result['num_emails']}")
    print(f"   Strategy: Complementary products + upgrades")
    print(f"\n💎 Preview (first 400 chars):\n{str(result['sequence'])[:400]}...")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_result(f"upsell_crosssell_campaign_{timestamp}.json", result)
    
    print("\n" + "=" * 80)
    return result


def main():
    """Run all advanced email automation tests."""
    print("\n" + "=" * 80)
    print("🚀 ADVANCED EMAIL AUTOMATION TESTS")
    print("=" * 80)
    print(f"\n📁 Outputs: {OUTPUT_DIR}")
    print(f"🤖 Model: {os.getenv('EMAIL_MODEL', 'gpt-4o-mini')}\n")
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OPENAI_API_KEY not found!")
        sys.exit(1)
    
    try:
        # Run all tests
        print("\n▶️  Starting Test Suite...\n")
        
        test_welcome_email_series()
        input("\nPress Enter to continue...")
        
        test_abandoned_cart_recovery()
        input("\nPress Enter to continue...")
        
        test_personalized_recommendations()
        input("\nPress Enter to continue...")
        
        test_ab_testing_variants()
        input("\nPress Enter to continue...")
        
        test_reengagement_campaign()
        input("\nPress Enter to continue...")
        
        test_seasonal_promotions()
        input("\nPress Enter to continue...")
        
        test_newsletter_content()
        input("\nPress Enter to continue...")
        
        test_transactional_emails()
        input("\nPress Enter to continue...")
        
        test_subject_line_optimization()
        input("\nPress Enter to continue...")
        
        test_loyalty_program()
        input("\nPress Enter to continue...")
        
        test_feedback_surveys()
        input("\nPress Enter to continue...")
        
        test_upsell_crosssell()
        
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
