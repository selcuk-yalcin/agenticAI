# Reflection System - Quick Reference

## 🎯 What is Reflection?

**Reflection** is a self-evaluation system where agents critically analyze their own outputs and automatically improve them. Think of it as an AI giving itself feedback and revising its work.

## ⚡ Quick Start

### Basic Reflection
```python
agent = ResearchAgent()
output = agent.run("Your query")

# Reflect on the output
reflection = agent.reflect(output)

print(f"Score: {reflection['score']}/10")
print(f"Strengths: {reflection['strengths']}")
print(f"Weaknesses: {reflection['weaknesses']}")
print(f"Improvements: {reflection['improvements']}")
```

### Auto-Improvement
```python
# Agent automatically improves until quality threshold met
result = agent.run_with_reflection(
    "Your query",
    auto_improve=True,
    max_iterations=2
)

print(f"Final output: {result['output']}")
print(f"Quality: {result['reflection']['score']}/10")
print(f"Improvements made: {result['iterations']}")
```

## 📊 Reflection Output

```python
{
    "score": 8.5,              # Quality score (0-10)
    "strengths": [             # What worked well
        "Clear explanation",
        "Good examples"
    ],
    "weaknesses": [            # What needs improvement
        "Missing context",
        "Too technical"
    ],
    "improvements": [          # Specific suggestions
        "Add more examples",
        "Simplify language"
    ],
    "revised_output": "...",   # Improved version
    "raw_reflection": "..."    # Full LLM response
}
```

## 🎨 Agent-Specific Criteria

### Research Agent
```python
criteria = [
    "Source diversity and credibility",
    "Citation accuracy",
    "Factual correctness",
    "Balanced perspective",
    "Current information"
]
```

### Content Writer
```python
criteria = [
    "SEO optimization",
    "Engagement potential",
    "Readability score",
    "Call-to-action effectiveness",
    "Target audience alignment"
]
```

### Support Agent
```python
criteria = [
    "Empathy and emotional intelligence",
    "Problem-solving effectiveness",
    "Professional and calming tone",
    "Clear next steps provided",
    "Response time appropriateness"
]
```

### Analytics Agent
```python
criteria = [
    "Data accuracy",
    "Actionable insights",
    "Clear recommendations",
    "Relevant metrics",
    "Business context"
]
```

### Email Agent
```python
criteria = [
    "Subject line effectiveness",
    "Call-to-action clarity",
    "Personalization level",
    "Conversion potential",
    "Brand voice consistency"
]
```

### Social Media Agent
```python
criteria = [
    "Engagement potential",
    "Platform appropriateness",
    "Hashtag strategy",
    "Visual appeal",
    "Call-to-action effectiveness"
]
```

## 💡 Common Use Cases

### 1. Quality Assurance
```python
output = agent.run(query)
reflection = agent.reflect(output)

if reflection['score'] >= 8.0:
    publish(output)
else:
    output = reflection['revised_output']
    publish(output)
```

### 2. Iterative Improvement
```python
for i in range(3):
    reflection = agent.reflect(output)
    if reflection['score'] >= 9.0:
        break
    output = reflection['revised_output']
```

### 3. A/B Testing
```python
variant_a = agent.run(query)
variant_b = agent.reflect(variant_a)['revised_output']

reflection_a = agent.reflect(variant_a)
reflection_b = agent.reflect(variant_b)

# Use better variant
best = variant_a if reflection_a['score'] > reflection_b['score'] else variant_b
```

### 4. Quality Tracking
```python
quality_log = []

for query in queries:
    result = agent.run_with_reflection(query, auto_improve=True)
    quality_log.append({
        'query': query,
        'score': result['reflection']['score'],
        'iterations': result['iterations']
    })

avg_quality = sum(r['score'] for r in quality_log) / len(quality_log)
print(f"Average quality: {avg_quality:.1f}/10")
```

## 🔧 Configuration

### Custom Criteria
```python
custom_criteria = [
    "Your criterion 1",
    "Your criterion 2",
    "Your criterion 3"
]

reflection = agent.reflect(output, criteria=custom_criteria)
```

### Quality Thresholds
```python
# High-stakes content: strict threshold
result = agent.run_with_reflection(
    query,
    auto_improve=True,
    max_iterations=3  # More iterations for critical content
)

# Quick drafts: lower threshold
result = agent.run_with_reflection(
    query,
    auto_improve=True,
    max_iterations=1  # Faster, good enough quality
)
```

## ⚠️ Best Practices

### ✅ DO
- Use reflection for high-stakes content
- Set reasonable max_iterations (1-3)
- Track quality scores over time
- Use custom criteria for specialized tasks
- Review revised outputs before publishing

### ❌ DON'T
- Use unlimited iterations (expensive)
- Rely solely on scores (review content)
- Ignore weaknesses section (valuable insights)
- Use for every simple query (overhead)
- Forget to test with your data first

## 📈 Performance Impact

| Operation | Time | Cost | When to Use |
|-----------|------|------|-------------|
| No reflection | 5-15s | 1x | Quick queries, drafts |
| Single reflection | +5-10s | +1x | Quality check |
| Auto-improve (max 2) | +10-20s | +2-3x | High-quality content |
| Auto-improve (max 3) | +15-30s | +3-4x | Critical content only |

## 🎓 Advanced Features

### Comparative Reflection
```python
models = ["gpt-4", "gpt-3.5-turbo"]
results = []

for model in models:
    agent.set_model(model)
    output = agent.run(query)
    reflection = agent.reflect(output)
    results.append((model, reflection['score'], output))

best = max(results, key=lambda x: x[1])
print(f"Best model: {best[0]} (score: {best[1]})")
```

### Reflection History
```python
history = []

for iteration in range(3):
    reflection = agent.reflect(output)
    history.append({
        'iteration': iteration,
        'score': reflection['score'],
        'improvements': reflection['improvements']
    })
    
    if reflection['score'] >= 9.5:
        break
    output = reflection['revised_output']

# Analyze improvement trajectory
scores = [h['score'] for h in history]
print(f"Improvement: {scores[-1] - scores[0]:.1f} points")
```

### Batch Quality Control
```python
high_quality_outputs = []

for query in queries:
    result = agent.run_with_reflection(
        query,
        auto_improve=True,
        max_iterations=2
    )
    
    if result['reflection']['score'] >= 8.5:
        high_quality_outputs.append(result['output'])
    else:
        print(f"⚠️ Low quality for: {query}")

print(f"✅ {len(high_quality_outputs)} high-quality outputs")
```

## 📚 Resources

- **Full Guide:** [REFLECTION.md](REFLECTION.md)
- **Examples:** [reflection_examples.py](reflection_examples.py)
- **Architecture:** Each project's ARCHITECTURE.md
- **Implementation:** [core/agents/base_agent.py](core/agents/base_agent.py)

## 🚀 Try It Now

```bash
# Run reflection examples
python reflection_examples.py

# Choose from 7 examples:
# 1. Basic Reflection
# 2. Auto-Improvement
# 3. Custom Criteria
# 4. Visualization Reflection
# 5. Iterative Improvement
# 6. Analytics Reflection
# 7. Social Media Reflection
```

## 🤝 Integration

Reflection works seamlessly with all features:

```python
# With workflows
workflow = ContentWorkflow()
result = workflow.full_content_pipeline(topic)
reflection = workflow.agent.reflect(result)

# With tools
agent = ResearchAgent()
result = agent.run("Research topic")  # Uses tools
reflection = agent.reflect(result)     # Reflects on tool-augmented output

# With memory
agent.run("First query")
agent.run("Follow-up query")  # Has context
reflection = agent.reflect(...)  # Evaluates context-aware response
```

---

**Need help?** See [REFLECTION.md](REFLECTION.md) for comprehensive documentation.
