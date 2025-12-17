# Agent Reflection System

## 🔍 Overview

Reflection is a powerful feature that allows agents to **self-evaluate** their outputs and **automatically improve** their responses. This creates a feedback loop where agents learn from their own performance.

## 🎯 Key Features

### 1. **Self-Evaluation**
Agents can critically analyze their own outputs based on:
- Accuracy and correctness
- Completeness of information
- Clarity and readability
- Relevance to the query
- Professional tone

### 2. **Automatic Improvement**
With `auto_improve=True`, agents will:
- Generate initial output
- Reflect on quality (score 0-10)
- If score < 9, create improved version
- Repeat until quality threshold met or max iterations reached

### 3. **Custom Criteria**
Each agent type can use specialized evaluation criteria:
- **Research:** Source quality, citation accuracy
- **Content:** SEO optimization, engagement potential
- **Support:** Empathy, problem-solving effectiveness
- **Analytics:** Data accuracy, actionable insights
- **Email:** Conversion potential, personalization
- **Social Media:** Engagement, platform appropriateness

## 📊 How It Works

```
┌─────────────────────────────────────────────────────┐
│                   USER INPUT                         │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│                 AGENT EXECUTION                      │
│  • Processes query                                   │
│  • Uses tools if needed                              │
│  • Generates initial output                          │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│                  REFLECTION                          │
│  ┌──────────────────────────────────────────┐       │
│  │  LLM evaluates its own output:           │       │
│  │  • Score: 0-10                           │       │
│  │  • Strengths: What worked well           │       │
│  │  • Weaknesses: What needs improvement    │       │
│  │  • Improvements: Specific suggestions    │       │
│  │  • Revised output: Improved version      │       │
│  └──────────────────────────────────────────┘       │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│           AUTO-IMPROVEMENT (Optional)                │
│  If score < 9.0 and revised output exists:          │
│  • Use revised output as new version                │
│  • Reflect again                                    │
│  • Repeat until quality threshold or max iterations │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│                   FINAL OUTPUT                       │
│  • High-quality response                            │
│  • Reflection analysis                              │
│  • Improvement history                              │
└─────────────────────────────────────────────────────┘
```

## 🚀 Usage Examples

### Basic Reflection

```python
from projects.research.agent import ResearchAgent

agent = ResearchAgent()

# Generate output
output = agent.run("Explain quantum computing")

# Reflect on quality
reflection = agent.reflect(output)

print(f"Quality Score: {reflection['score']}/10")
print(f"Strengths: {reflection['strengths']}")
print(f"Weaknesses: {reflection['weaknesses']}")
print(f"Improvements: {reflection['improvements']}")
```

### Auto-Improvement

```python
# Run with automatic improvement
result = agent.run_with_reflection(
    "Explain quantum computing",
    auto_improve=True,      # Enable auto-improvement
    max_iterations=2        # Maximum improvement rounds
)

print(f"Final Output: {result['output']}")
print(f"Final Score: {result['reflection']['score']}/10")
print(f"Iterations: {result['iterations']}")
```

### Custom Criteria

```python
# Custom evaluation criteria for support agent
support_criteria = [
    "Empathy and emotional intelligence",
    "Problem-solving effectiveness",
    "Response time appropriateness",
    "Professional and calming tone",
    "Clear next steps provided"
]

reflection = agent.reflect(output, criteria=support_criteria)
```

## 📈 Reflection Output Structure

```python
{
    "score": 8.5,                    # Overall quality (0-10)
    "strengths": [                   # What worked well
        "Clear and concise explanation",
        "Good use of examples",
        "Professional tone maintained"
    ],
    "weaknesses": [                  # Areas for improvement
        "Could include more technical details",
        "Missing practical applications"
    ],
    "improvements": [                # Specific suggestions
        "Add 2-3 real-world use cases",
        "Include comparison with classical computing",
        "Explain quantum superposition more clearly"
    ],
    "revised_output": "...",         # Improved version (if applicable)
    "raw_reflection": "..."          # Full LLM reflection response
}
```

## 🎯 Agent-Specific Use Cases

### Research Agent
```python
# Reflect on research quality
reflection = agent.reflect(research_output, criteria=[
    "Source diversity and credibility",
    "Citation accuracy",
    "Factual correctness",
    "Balanced perspective",
    "Current information"
])
```

### Content Writer Agent
```python
# Reflect on content quality
reflection = agent.reflect(blog_post, criteria=[
    "SEO optimization",
    "Engagement potential",
    "Readability score",
    "Call-to-action effectiveness",
    "Target audience alignment"
])
```

### Support Agent
```python
# Reflect on support response
reflection = agent.reflect(support_response, criteria=[
    "Customer satisfaction potential",
    "Problem resolution completeness",
    "Empathy demonstration",
    "Response clarity",
    "Follow-up actions defined"
])
```

### Analytics Agent
```python
# Reflect on analysis quality
reflection = agent.reflect(analysis_report, criteria=[
    "Data accuracy",
    "Insight actionability",
    "Visualization appropriateness",
    "Business context",
    "Recommendation clarity"
])
```

### Email Agent
```python
# Reflect on email quality
reflection = agent.reflect(email_campaign, criteria=[
    "Subject line effectiveness",
    "Call-to-action clarity",
    "Personalization level",
    "Conversion potential",
    "Brand voice consistency"
])
```

### Social Media Agent
```python
# Reflect on social content
reflection = agent.reflect(social_post, criteria=[
    "Engagement potential",
    "Platform appropriateness",
    "Hashtag strategy",
    "Visual appeal description",
    "Call-to-action effectiveness"
])
```

## 💡 Best Practices

### 1. **Choose Appropriate Criteria**
- Use default criteria for general quality
- Use custom criteria for specialized evaluation
- Align criteria with business goals

### 2. **Set Reasonable Thresholds**
```python
# Auto-improve until score >= 9.0
result = agent.run_with_reflection(
    query,
    auto_improve=True,
    max_iterations=3  # Prevent infinite loops
)
```

### 3. **Monitor Iterations**
```python
if result['iterations'] > 0:
    print(f"Output improved {result['iterations']} times")
    print(f"Quality gain: +{result['reflection']['score'] - initial_score:.1f}")
```

### 4. **Use Reflection for Learning**
```python
# Collect reflection data for training
reflections = []
for query in queries:
    result = agent.run_with_reflection(query)
    reflections.append({
        'query': query,
        'score': result['reflection']['score'],
        'weaknesses': result['reflection']['weaknesses']
    })

# Analyze common weaknesses
from collections import Counter
all_weaknesses = [w for r in reflections for w in r['weaknesses']]
common_issues = Counter(all_weaknesses).most_common(5)
```

## 🔬 Advanced Features

### Comparative Reflection
```python
# Compare multiple outputs
outputs = [
    agent.run(query, model="gpt-4"),
    agent.run(query, model="gpt-3.5-turbo")
]

reflections = [agent.reflect(o) for o in outputs]

best_idx = max(range(len(reflections)), key=lambda i: reflections[i]['score'])
print(f"Best model: {['gpt-4', 'gpt-3.5-turbo'][best_idx]}")
```

### Iterative Refinement
```python
output = agent.run(query)

for iteration in range(3):
    reflection = agent.reflect(output)
    
    if reflection['score'] >= 9.5:
        break
    
    if reflection['revised_output']:
        output = reflection['revised_output']
        print(f"Iteration {iteration + 1}: Score {reflection['score']}/10")
```

### Quality Tracking
```python
# Track quality over time
quality_log = []

for query in test_queries:
    result = agent.run_with_reflection(query, auto_improve=True)
    quality_log.append({
        'query': query,
        'initial_score': result['reflection']['score'],
        'iterations': result['iterations']
    })

avg_quality = sum(r['initial_score'] for r in quality_log) / len(quality_log)
print(f"Average quality: {avg_quality:.1f}/10")
```

## 📊 Performance Considerations

- **Response Time:** Reflection adds 5-10 seconds per evaluation
- **Cost:** Each reflection is an additional LLM call
- **Iterations:** Limit to 2-3 for production use
- **When to Use:**
  - High-stakes content (marketing, support)
  - Quality-critical applications
  - Training and evaluation
  - A/B testing

## 🎓 Example Workflow

```python
# Complete reflection workflow
from projects.content_creation.agent import ContentWriterAgent

agent = ContentWriterAgent()

# 1. Generate initial content
print("Generating initial draft...")
draft = agent.run("Write a blog intro about AI")

# 2. Reflect on quality
print("Evaluating quality...")
reflection = agent.reflect(draft)

# 3. Show results
print(f"\nQuality Score: {reflection['score']}/10")
print("\nStrengths:")
for s in reflection['strengths']:
    print(f"  ✓ {s}")

print("\nAreas for Improvement:")
for w in reflection['weaknesses']:
    print(f"  ⚠ {w}")

# 4. Use improved version if available
if reflection['revised_output']:
    final_output = reflection['revised_output']
    print("\n✨ Using improved version")
else:
    final_output = draft
    print("\n✓ Original draft is high quality")

# 5. Publish
print(f"\nFinal content ready for publishing!")
```

## 🔗 Integration with Workflows

Reflection can be integrated into workflows:

```python
from projects.content_creation.workflows.content_workflow import ContentWorkflow

workflow = ContentWorkflow()

# Workflow with reflection at each step
def enhanced_content_pipeline(topic):
    # Step 1: Research
    research = workflow.agent.run(f"Research {topic}")
    research_quality = workflow.agent.reflect(research)
    
    # Step 2: Outline (only if research is good)
    if research_quality['score'] >= 7.0:
        outline = workflow.agent.run(f"Create outline for {topic}")
        # ... continue
    else:
        # Improve research first
        research = research_quality['revised_output']
```

## 📚 See Also

- `reflection_examples.py` - 7 complete examples
- `core/agents/base_agent.py` - Reflection implementation
- Individual agent documentation for specialized criteria
