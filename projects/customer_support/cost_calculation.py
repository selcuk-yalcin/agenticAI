#!/usr/bin/env python3
"""
Calculate the cost of running advanced feature tests
"""

import json
import tiktoken

def count_tokens(text: str, model: str = "gpt-4o-mini") -> int:
    """Count tokens in text using tiktoken."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    
    return len(encoding.encode(text))


def calculate_cost(input_tokens: int, output_tokens: int, model: str = "gpt-4o-mini") -> dict:
    """Calculate cost based on token counts."""
    
    # Pricing per 1M tokens (as of Dec 2024)
    pricing = {
        "gpt-4o-mini": {
            "input": 0.150,   # $0.150 per 1M input tokens
            "output": 0.600   # $0.600 per 1M output tokens
        },
        "gpt-4o": {
            "input": 2.50,
            "output": 10.00
        },
        "gpt-4-turbo": {
            "input": 10.00,
            "output": 30.00
        }
    }
    
    if model not in pricing:
        model = "gpt-4o-mini"
    
    input_cost = (input_tokens / 1_000_000) * pricing[model]["input"]
    output_cost = (output_tokens / 1_000_000) * pricing[model]["output"]
    total_cost = input_cost + output_cost
    
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
        "model": model
    }


def analyze_test_outputs():
    """Analyze all test outputs and calculate costs."""
    
    print("=" * 80)
    print("ADVANCED FEATURES TEST - COST ANALYSIS")
    print("=" * 80)
    print()
    
    # Load and analyze each test result
    test_files = {
        "Handle Inquiry": "outputs/advanced_tests/handle_inquiry_20251218_051849.json",
        "Ticket Analysis": "outputs/advanced_tests/ticket_analysis_20251218_051850.json",
        "KB Search": "outputs/advanced_tests/kb_search_20251218_051852.json",
        "Templates": "outputs/advanced_tests/all_templates_20251218_051903.json",
        "Sentiment": "outputs/advanced_tests/sentiment_analysis_20251218_051905.json",
        "Escalation": "outputs/advanced_tests/escalation_detection_20251218_051906.json"
    }
    
    total_input_tokens = 0
    total_output_tokens = 0
    
    test_costs = []
    
    for test_name, filepath in test_files.items():
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Estimate tokens for this test
            input_text = json.dumps(data)
            output_text = json.dumps(data)
            
            input_tokens = count_tokens(input_text)
            output_tokens = count_tokens(output_text)
            
            cost = calculate_cost(input_tokens, output_tokens)
            
            total_input_tokens += input_tokens
            total_output_tokens += output_tokens
            
            test_costs.append({
                "test": test_name,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost": cost["total_cost"]
            })
            
            print(f"📊 {test_name}")
            print(f"   Input:  {input_tokens:,} tokens")
            print(f"   Output: {output_tokens:,} tokens")
            print(f"   Cost:   ${cost['total_cost']:.6f}")
            print()
            
        except FileNotFoundError:
            print(f"⚠️  {test_name}: File not found - {filepath}")
            print()
    
    # Calculate total
    total_cost = calculate_cost(total_input_tokens, total_output_tokens)
    
    print("=" * 80)
    print("TOTAL COST SUMMARY")
    print("=" * 80)
    print()
    print(f"Model: {total_cost['model']}")
    print(f"Total Input Tokens:  {total_cost['input_tokens']:,}")
    print(f"Total Output Tokens: {total_cost['output_tokens']:,}")
    print(f"Total Tokens:        {total_cost['total_tokens']:,}")
    print()
    print(f"Input Cost:  ${total_cost['input_cost']:.6f}")
    print(f"Output Cost: ${total_cost['output_cost']:.6f}")
    print(f"TOTAL COST:  ${total_cost['total_cost']:.6f}")
    print()
    
    # Extrapolations
    print("=" * 80)
    print("COST EXTRAPOLATIONS")
    print("=" * 80)
    print()
    
    # Cost per test (average)
    avg_cost_per_test = total_cost['total_cost'] / len(test_costs) if test_costs else 0
    print(f"Average cost per test:     ${avg_cost_per_test:.6f}")
    print()
    
    # Volume estimates
    volumes = [100, 1000, 10000, 100000]
    for volume in volumes:
        estimated_cost = total_cost['total_cost'] * volume
        print(f"Cost for {volume:,} similar requests: ${estimated_cost:.2f}")
    
    print()
    
    # Monthly estimates (based on different daily volumes)
    print("=" * 80)
    print("MONTHLY COST ESTIMATES")
    print("=" * 80)
    print()
    
    daily_volumes = [10, 50, 100, 500, 1000, 5000]
    for daily in daily_volumes:
        monthly_requests = daily * 30
        monthly_cost = total_cost['total_cost'] * monthly_requests
        print(f"{daily:,} requests/day ({monthly_requests:,}/month): ${monthly_cost:.2f}/month")
    
    print()
    
    # Comparison with other models
    print("=" * 80)
    print("COST COMPARISON WITH OTHER MODELS")
    print("=" * 80)
    print()
    
    models_to_compare = ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"]
    for model in models_to_compare:
        model_cost = calculate_cost(total_input_tokens, total_output_tokens, model)
        print(f"{model:20s} Total: ${model_cost['total_cost']:.6f}")
    
    print()
    
    # Save report
    report = {
        "test_costs": test_costs,
        "total": total_cost,
        "extrapolations": {
            "per_100": total_cost['total_cost'] * 100,
            "per_1000": total_cost['total_cost'] * 1000,
            "per_10000": total_cost['total_cost'] * 10000
        },
        "monthly_estimates": {
            f"{daily}_per_day": {
                "daily_requests": daily,
                "monthly_requests": daily * 30,
                "monthly_cost": total_cost['total_cost'] * daily * 30
            }
            for daily in daily_volumes
        }
    }
    
    report_path = "outputs/advanced_tests/cost_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    print(f"💾 Detailed report saved to: {report_path}")
    print()


if __name__ == "__main__":
    try:
        analyze_test_outputs()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()