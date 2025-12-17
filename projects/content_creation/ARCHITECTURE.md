# Content Creation Agent - Architecture

## 📊 Project Structure
```
content_creation/
├── README.md                     # Project documentation
├── ARCHITECTURE.md              # This file - how it works
├── __init__.py                  # Package initialization
├── agent.py                     # Main ContentWriterAgent class
├── tools/                       # Content tools
│   ├── __init__.py
│   ├── keyword_research.py     # SEO keyword discovery
│   └── seo_optimizer.py        # Content optimization
└── workflows/                   # Content pipelines
    ├── __init__.py
    └── content_workflow.py     # Full content creation flow
```

## 🔄 How It Works

### 1. User Requests Content
```
User: "Write a blog post about sustainable fashion"
   + Optional: Target audience, tone, length
   ↓
```

### 2. Request Goes to ContentWriterAgent
```
content_creation/agent.py
   ├── ContentWriterAgent.__init__()
   │   ├── Loads system prompt: "You are an expert content writer"
   │   ├── Registers 2 tools: KeywordResearch, SEOOptimizer
   │   └── Connects to OpenAI API
   │
   └── ContentWriterAgent.run(topic, content_type)
       ├── Sends request + tools to GPT-4
       ├── LLM researches keywords
       ├── LLM creates content
       ├── LLM optimizes for SEO
       └── Returns polished content
```

### 3. Tools Are Called (Sequential Flow)

#### Step 1: Keyword Research
```
tools/keyword_research.py
   └── KeywordResearchTool.execute(topic)
       ├── Analyzes topic
       ├── Identifies main keywords
       │   ├── Primary keywords (high volume)
       │   ├── Secondary keywords (supporting)
       │   └── Long-tail keywords (specific)
       ├── Checks keyword difficulty
       ├── Estimates search volume
       └── Returns keyword list with metrics
```

#### Step 2: Content Creation
```
GPT-4 writes content using keywords
   ├── Creates engaging headline
   ├── Writes introduction (hook reader)
   ├── Develops body paragraphs
   │   ├── Naturally includes keywords
   │   ├── Uses subheadings (H2, H3)
   │   └── Adds examples, data
   ├── Writes conclusion (call-to-action)
   └── Formats properly
```

#### Step 3: SEO Optimization
```
tools/seo_optimizer.py
   └── SEOOptimizerTool.execute(content, keywords)
       ├── Analyzes content
       │   ├── Keyword density (2-3%)
       │   ├── Readability score
       │   ├── Heading structure
       │   └── Meta description
       ├── Provides suggestions
       │   ├── Add keywords to title
       │   ├── Improve readability
       │   ├── Better subheadings
       │   └── Optimize meta tags
       └── Returns SEO score + recommendations
```

### 4. Workflow Orchestration (Full Pipeline)
```
workflows/content_workflow.py
   └── ContentWorkflow.full_content_pipeline()
       │
       Step 1: Keyword Research
       ├── Find best keywords for topic
       ├── Save keywords for reference
       │
       Step 2: Content Outline
       ├── Create structure (H1, H2, H3)
       ├── Plan sections
       │
       Step 3: Draft Writing
       ├── Write full content
       ├── Include keywords naturally
       │
       Step 4: SEO Optimization
       ├── Check keyword usage
       ├── Improve readability
       ├── Optimize meta tags
       │
       Step 5: Final Polish
       ├── Proofread
       ├── Format properly
       └── Ready to publish!
```

### 5. Response Returns to User
```
   ↓
Result:
   ├── Polished content (blog/article/landing page)
   ├── SEO score & recommendations
   ├── Meta description
   ├── Suggested images/media
   └── Publishing checklist
```

## 🎯 Data Flow Diagram

```
┌─────────┐
│  USER   │ Topic + Content Type
└────┬────┘
     │
     ▼
┌───────────────────────────────────────────┐
│  ContentWriterAgent (agent.py)            │
│                                           │
│  ┌────────────────────────────────┐      │
│  │   LLM Router (GPT-4)           │      │
│  │   - Understands topic          │      │
│  │   - Plans content structure    │      │
│  │   - Writes engaging copy       │      │
│  │   - Optimizes for SEO          │      │
│  └──────────┬─────────────────────┘      │
│             │                             │
│   ┌─────────┴──────────┐                 │
│   │                    │                 │
│   ▼                    ▼                 │
│ ┌─────────┐      ┌──────────┐           │
│ │ Memory  │      │ Prompt   │           │
│ │ Past    │      │ Brand    │           │
│ │ Content │      │ Voice    │           │
│ └─────────┘      └──────────┘           │
│                                          │
│   ┌──────────────────────────────┐      │
│   │        Tools (2)             │      │
│   │                              │      │
│   │  🔍 Keyword Research         │      │
│   │     ↓ Main keywords          │      │
│   │     ↓ Long-tail keywords     │      │
│   │     ↓ Search volume          │      │
│   │     ↓ Difficulty scores      │      │
│   │                              │      │
│   │  ✨ SEO Optimizer            │      │
│   │     ↓ Keyword density        │      │
│   │     ↓ Readability score      │      │
│   │     ↓ Meta tags              │      │
│   │     ↓ Optimization tips      │      │
│   └──────────────────────────────┘      │
└───────────────────────────────────────────┘
     │
     ▼
┌─────────┐
│ RESULT  │ SEO-optimized content
└─────────┘
```

## 🚀 Usage Examples

### Simple Blog Post
```python
from projects.content_creation.agent import ContentWriterAgent

agent = ContentWriterAgent()
result = agent.run(
    topic="Sustainable Fashion Trends",
    content_type="blog_post"
)
print(result)
```

**Flow:**
1. User request → ContentWriterAgent
2. Agent → Keyword research (sustainable fashion, eco-friendly, etc.)
3. Agent → GPT-4 writes blog post
4. Agent → SEO optimization check
5. Result → 800-1200 word optimized blog post

### Full Content Pipeline
```python
from projects.content_creation.workflows.content_workflow import ContentWorkflow

workflow = ContentWorkflow()
result = workflow.full_content_pipeline(
    topic="AI in Healthcare",
    content_type="article",
    target_audience="healthcare professionals",
    tone="professional"
)
```

**Flow:**
1. Workflow starts
2. Step 1: Keyword research → 20 relevant keywords
3. Step 2: Outline creation → 5 sections planned
4. Step 3: Draft writing → 1500 words written
5. Step 4: SEO optimization → Score 85/100
6. Step 5: Final polish → Ready to publish
7. Result → Complete article package

### Content Series
```python
workflow = ContentWorkflow()
series = workflow.content_series(
    main_topic="Web Development",
    num_posts=5,
    subtopics=["HTML", "CSS", "JavaScript", "React", "Node.js"]
)
```

**Flow:**
1. Workflow plans 5-post series
2. Each post:
   - Keyword research
   - Write content
   - SEO optimize
   - Link to other posts in series
3. Result → 5 interconnected blog posts

## 🔧 Key Components

### agent.py
- **Purpose:** Main content creation agent
- **Responsibilities:**
  - Initialize LLM connection
  - Register content tools
  - Handle content requests
  - Manage writing style
- **Key Methods:**
  - `__init__()`: Setup
  - `run(topic, type)`: Create content
  - `_apply_tone()`: Adjust writing style

### tools/keyword_research.py
- **Purpose:** SEO keyword discovery
- **Features:**
  - Main keyword identification
  - Related keywords
  - Long-tail keywords
  - Search volume estimation
  - Keyword difficulty
- **Returns:** List of keywords with metrics

### tools/seo_optimizer.py
- **Purpose:** Content optimization
- **Features:**
  - Keyword density check
  - Readability analysis (Flesch score)
  - Heading structure validation
  - Meta description generation
  - Internal linking suggestions
- **Returns:** SEO score + recommendations

### workflows/content_workflow.py
- **Purpose:** End-to-end content creation
- **Features:**
  - Full content pipeline
  - Content series creation
  - Multi-format content
  - A/B testing variants
  - Content repurposing

## 💡 Content Types & When to Use

| Content Type | Best For | Length | Flow |
|-------------|----------|---------|------|
| Blog Post | Engagement, SEO | 800-1500 words | Research → Write → Optimize |
| Article | Authority, depth | 1500-3000 words | Research → Outline → Write → Optimize |
| Landing Page | Conversions | 300-800 words | Research → Persuasive copy → CTA |
| Social Post | Quick engagement | 50-280 chars | Hook → Value → CTA |

## 📝 Writing Process

```
1. KEYWORD RESEARCH
   └── Identify target keywords
       ├── Primary (1-2)
       ├── Secondary (3-5)
       └── Long-tail (5-10)

2. OUTLINE CREATION
   └── Structure content
       ├── H1: Main title
       ├── H2: Major sections
       └── H3: Subsections

3. DRAFT WRITING
   └── Write content
       ├── Introduction (hook)
       ├── Body (value)
       └── Conclusion (CTA)

4. SEO OPTIMIZATION
   └── Optimize for search
       ├── Keyword placement
       ├── Meta description
       ├── Alt text
       └── Internal links

5. FINAL REVIEW
   └── Polish content
       ├── Grammar check
       ├── Tone consistency
       └── Format properly
```

## 🔍 Reflection & Self-Improvement

Content quality is critical—reflection helps ensure engagement:

```python
# Reflect on blog post quality
reflection = agent.reflect(blog_post, criteria=[
    "SEO optimization",
    "Engagement potential",
    "Readability score",
    "Call-to-action effectiveness",
    "Target audience alignment"
])

# Auto-improve until quality threshold met
result = agent.run_with_reflection(
    "Write blog about sustainable fashion",
    auto_improve=True,
    max_iterations=2
)

print(f"SEO Score: {reflection['score']}/10")
print(f"Improved {result['iterations']} times")
```

### Content Reflection Example
```python
{
    "score": 8.0,
    "strengths": [
        "Strong hook and engaging opening",
        "Good keyword integration (2.5% density)",
        "Clear call-to-action"
    ],
    "weaknesses": [
        "Could use more subheadings for readability",
        "Missing internal links"
    ],
    "improvements": [
        "Add 2-3 more H2 subheadings",
        "Include 3-4 internal links to related content",
        "Add more specific examples"
    ]
}
```

See [REFLECTION.md](../../REFLECTION.md) for complete guide.

## 🎓 Technical Details

- **LLM:** OpenAI GPT-4
- **Tools:** 2 (KeywordResearch, SEOOptimizer)
- **Content Types:** Blog post, Article, Landing page, Social post
- **Response Time:** 10-30 seconds per piece
- **SEO Score:** 0-100 (target: 80+)
- **Readability:** Flesch score 60-70 (target audience dependent)
- **Keyword Density:** 2-3% optimal
- **Reflection:** Content quality & SEO evaluation supported
