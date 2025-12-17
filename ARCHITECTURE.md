# Architecture Diagrams

Visual representation of all AI agent architectures and workflows.

## Overview

This document contains architecture diagrams showing the structure and flow of each agent project.

## Diagram Legend

- **User**: End user interacting with the system
- **LLM Router**: Central language model (GPT-4/Claude) handling requests
- **Prompt**: System prompt defining agent behavior
- **Memory**: Conversation/state storage
- **Tools**: External capabilities the agent can use
- **Features**: Built-in functionality

---

## 1. Research Agent Architecture

```
┌──────┐
│ User │
└───┬──┘
    │ Query
    ▼
┌─────────────────────────────────────────────┐
│            Research Agent                    │
│  ┌─────────────────┐                        │
│  │   LLM Router    │                        │
│  │   GPT-4/Claude  │                        │
│  └────┬───┬───┬────┘                        │
│       │   │   │                             │
│   ┌───▼───▼───▼───┐                        │
│   │ System Prompt: │                        │
│   │Research Expert │                        │
│   └────────────────┘                        │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │           Tools                       │  │
│  │  ┌─────────────────────────┐         │  │
│  │  │ Tavily Search           │         │  │
│  │  │ (Web Search)            │         │  │
│  │  └─────────────────────────┘         │  │
│  │  ┌─────────────────────────┐         │  │
│  │  │ Wikipedia               │         │  │
│  │  │ (Encyclopedia)          │         │  │
│  │  └─────────────────────────┘         │  │
│  │  ┌─────────────────────────┐         │  │
│  │  │ arXiv                   │         │  │
│  │  │ (Academic Papers)       │         │  │
│  │  └─────────────────────────┘         │  │
│  └──────────────────────────────────────┘  │
│                                             │
│  ┌──────────────┐                          │
│  │   Memory     │                          │
│  │Conversation  │                          │
│  └──────────────┘                          │
└─────────────────────────────────────────────┘
    │ Response
    ▼
┌──────┐
│ User │
└──────┘
```

**Tools:**
- Tavily Search: Web search for current information
- Wikipedia: Encyclopedia lookups
- arXiv: Academic paper search

**Use Cases:**
- Comprehensive topic research
- Comparative analysis
- Trend analysis
- Expert synthesis

---

## 2. Data Visualization Agent Architecture

```
┌─────────────┐
│ User + Data │
└──────┬──────┘
       │ Data + Request
       ▼
┌──────────────────────────────────────────────┐
│         Chart Agent                          │
│  ┌─────────────────┐                         │
│  │   LLM Router    │                         │
│  │     GPT-4       │                         │
│  └────┬────────────┘                         │
│       │                                      │
│  ┌────▼──────────┐                           │
│  │System Prompt: │                           │
│  │ Data Analyst  │                           │
│  └───────────────┘                           │
│                                              │
│  ┌─────────────────────────────────────┐    │
│  │         Tools                        │    │
│  │  ┌────────────────────────┐          │    │
│  │  │ Data Analysis Tool     │          │    │
│  │  │ (Stats & Insights)     │          │    │
│  │  └────────────────────────┘          │    │
│  │  ┌────────────────────────┐          │    │
│  │  │ Chart Generation Tool  │          │    │
│  │  │ • Line Chart           │          │    │
│  │  │ • Bar Chart            │          │    │
│  │  │ • Scatter Plot         │          │    │
│  │  │ • Pie Chart            │          │    │
│  │  │ • Heatmap              │          │    │
│  │  └────────────────────────┘          │    │
│  └─────────────────────────────────────┘    │
│                                              │
│  ┌──────────────┐                            │
│  │   Memory     │                            │
│  │Chart History │                            │
│  └──────────────┘                            │
└──────────────────────────────────────────────┘
       │ Visualization
       ▼
┌─────────────┐
│    User     │
└─────────────┘
```

**Tools:**
- Data Analysis: Statistical analysis and insights
- Chart Generation: 5 types of visualizations

**Use Cases:**
- Sales trend visualization
- Data analysis
- Multi-chart dashboards
- Correlation analysis

---

## 3. Content Creation Agent Architecture

```
┌──────┐
│ User │
└───┬──┘
    │ Topic
    ▼
┌─────────────────────────────────────────────┐
│       Content Writer Agent                   │
│  ┌─────────────────┐                        │
│  │   LLM Router    │                        │
│  │     GPT-4       │                        │
│  └────┬────────────┘                        │
│       │                                     │
│  ┌────▼──────────────┐                      │
│  │  System Prompt:   │                      │
│  │Expert Content     │                      │
│  │    Writer         │                      │
│  └───────────────────┘                      │
│                                             │
│  ┌──────────────────────────────────┐      │
│  │          Tools                    │      │
│  │  ┌─────────────────────┐          │      │
│  │  │ Keyword Research    │          │      │
│  │  │ (SEO Keywords)      │          │      │
│  │  └─────────────────────┘          │      │
│  │  ┌─────────────────────┐          │      │
│  │  │ SEO Optimizer       │          │      │
│  │  │ (Content Analysis)  │          │      │
│  │  └─────────────────────┘          │      │
│  └──────────────────────────────────┘      │
│                                             │
│  ┌──────────────────────────────────┐      │
│  │      Content Types                │      │
│  │  • Blog Post (800-1500 words)    │      │
│  │  • Article (professional)        │      │
│  │  • Landing Page (conversion)     │      │
│  │  • Social Post (short)           │      │
│  └──────────────────────────────────┘      │
│                                             │
│  ┌──────────────┐                          │
│  │   Memory     │                          │
│  │   Content    │                          │
│  │   Library    │                          │
│  └──────────────┘                          │
└─────────────────────────────────────────────┘
    │ Content
    ▼
┌──────┐
│ User │
└──────┘
```

**Tools:**
- Keyword Research: SEO keyword identification
- SEO Optimizer: Content optimization

**Content Types:**
- Blog Posts
- Articles
- Landing Pages
- Social Media Posts

---

## 4. Customer Support Agent Architecture

```
┌──────────┐
│ Customer │
└────┬─────┘
     │ Inquiry
     ▼
┌──────────────────────────────────────────────┐
│         Support Agent                         │
│  ┌─────────────────┐                         │
│  │   LLM Router    │                         │
│  │     GPT-4       │                         │
│  └────┬────────────┘                         │
│       │                                      │
│  ┌────▼──────────────┐                       │
│  │  System Prompt:   │                       │
│  │Professional       │                       │
│  │    Support        │                       │
│  └───────────────────┘                       │
│                                              │
│  ┌─────────────────────────────────┐        │
│  │        Analysis                  │        │
│  │  ┌───────────────────┐           │        │
│  │  │ Sentiment         │           │        │
│  │  │ Analysis          │           │        │
│  │  └───────────────────┘           │        │
│  │  ┌───────────────────┐           │        │
│  │  │ Escalation        │           │        │
│  │  │ Detection         │           │        │
│  │  └───────────────────┘           │        │
│  └─────────────────────────────────┘        │
│                                              │
│  ┌─────────────────────────────────┐        │
│  │        Features                  │        │
│  │  • Knowledge Base Search         │        │
│  │  • Ticket Categorization        │        │
│  │  • Response Generation          │        │
│  │  • Auto-routing                 │        │
│  └─────────────────────────────────┘        │
│                                              │
│  ┌──────────────┐                            │
│  │   Memory     │                            │
│  │   Ticket     │                            │
│  │   History    │                            │
│  └──────────────┘                            │
└──────────────────────────────────────────────┘
     │ Solution
     ▼
┌──────────┐
│ Customer │
└──────────┘
```

**Features:**
- Sentiment Analysis
- Escalation Detection
- Knowledge Base Search
- Ticket Categorization
- Auto-response Generation

---

## 5. E-commerce Analytics Agent Architecture

```
┌───────────────┐
│ Business User │
└───────┬───────┘
        │ Business Query
        ▼
┌────────────────────────────────────────────────┐
│         Analytics Agent                         │
│  ┌─────────────────┐                           │
│  │   LLM Router    │                           │
│  │     GPT-4       │                           │
│  └────┬────────────┘                           │
│       │                                        │
│  ┌────▼──────────────┐                         │
│  │  System Prompt:   │                         │
│  │Data Analyst Expert│                         │
│  └───────────────────┘                         │
│                                                │
│  ┌────────────────────────────────────┐       │
│  │      Analysis Types                 │       │
│  │  • Sales Trends                     │       │
│  │  • Product Performance              │       │
│  │  • Customer Behavior                │       │
│  │  • Revenue Forecasting              │       │
│  │  • Cart Abandonment                 │       │
│  │  • Product Recommendations          │       │
│  │  • Customer Segmentation            │       │
│  └────────────────────────────────────┘       │
│                                                │
│  ┌──────────────┐                              │
│  │   Memory     │                              │
│  │  Analysis    │                              │
│  │   History    │                              │
│  └──────────────┘                              │
└────────────────────────────────────────────────┘
        │ Insights & Reports
        ▼
┌───────────────┐
│ Business User │
└───────────────┘
```

**Analysis Types:**
- Sales Trends
- Product Performance
- Customer Behavior
- Revenue Forecasting
- Cart Abandonment
- Recommendations
- Segmentation

---

## 6. Email Automation Agent Architecture

```
┌──────────┐
│ Marketer │
└────┬─────┘
     │ Campaign Brief
     ▼
┌──────────────────────────────────────────────┐
│         Email Agent                           │
│  ┌─────────────────┐                         │
│  │   LLM Router    │                         │
│  │     GPT-4       │                         │
│  └────┬────────────┘                         │
│       │                                      │
│  ┌────▼──────────────┐                       │
│  │  System Prompt:   │                       │
│  │Email Marketing    │                       │
│  │    Expert         │                       │
│  └───────────────────┘                       │
│                                              │
│  ┌─────────────────────────────────┐        │
│  │      Email Types                 │        │
│  │  • Marketing Emails              │        │
│  │  • Transactional Emails          │        │
│  │  • Drip Campaigns                │        │
│  │  • Newsletters                   │        │
│  └─────────────────────────────────┘        │
│                                              │
│  ┌─────────────────────────────────┐        │
│  │        Features                  │        │
│  │  • Personalization               │        │
│  │  • A/B Testing                   │        │
│  │  • Subject Optimization          │        │
│  │  • Smart Scheduling              │        │
│  └─────────────────────────────────┘        │
│                                              │
│  ┌──────────────┐                            │
│  │   Memory     │                            │
│  │  Campaign    │                            │
│  │   History    │                            │
│  └──────────────┘                            │
└──────────────────────────────────────────────┘
     │ Email Content
     ▼
┌──────────┐
│ Marketer │
└──────────┘
```

**Email Types:**
- Marketing Emails
- Transactional Emails
- Drip Campaigns
- Newsletters

**Features:**
- Personalization at scale
- A/B Testing
- Subject Line Optimization
- Smart Scheduling

---

## 7. Social Media Management Agent Architecture

```
┌──────────────────────┐
│ Social Media Manager │
└──────────┬───────────┘
           │ Campaign Idea
           ▼
┌────────────────────────────────────────────────┐
│      Social Media Agent                         │
│  ┌─────────────────┐                           │
│  │   LLM Router    │                           │
│  │     GPT-4       │                           │
│  └────┬────────────┘                           │
│       │                                        │
│  ┌────▼──────────────┐                         │
│  │  System Prompt:   │                         │
│  │Social Media Expert│                         │
│  └───────────────────┘                         │
│                                                │
│  ┌────────────────────────────────────┐       │
│  │        Platforms                    │       │
│  │  • Instagram (2200 chars)           │       │
│  │  • Twitter/X (280 chars)            │       │
│  │  • LinkedIn (3000 chars)            │       │
│  │  • Facebook (63K chars)             │       │
│  │  • TikTok (2200 chars)              │       │
│  └────────────────────────────────────┘       │
│                                                │
│  ┌────────────────────────────────────┐       │
│  │        Features                     │       │
│  │  • Hashtag Optimization             │       │
│  │  • Content Calendar                 │       │
│  │  • Content Repurposing              │       │
│  │  • Engagement Analysis              │       │
│  │  • Viral Content Creation           │       │
│  └────────────────────────────────────┘       │
│                                                │
│  ┌──────────────┐                              │
│  │   Memory     │                              │
│  │   Content    │                              │
│  │   Library    │                              │
│  └──────────────┘                              │
└────────────────────────────────────────────────┘
           │ Social Content
           ▼
┌──────────────────────┐
│ Social Media Manager │
└──────────────────────┘
```

**Platforms:**
- Instagram
- Twitter/X
- LinkedIn
- Facebook
- TikTok

**Features:**
- Hashtag Optimization
- Content Calendar
- Content Repurposing
- Engagement Analysis

---

## Overall System Architecture

```
                    ┌──────┐
                    │ User │
                    └───┬──┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
    ┌────────────────────────────────────┐
    │         Core System                │
    │  ┌──────────────────────────┐     │
    │  │      BaseAgent           │     │
    │  │   (Abstract Base)        │     │
    │  └──────────────────────────┘     │
    │  ┌──────────────────────────┐     │
    │  │      BaseTool            │     │
    │  │   (Abstract Base)        │     │
    │  └──────────────────────────┘     │
    │  ┌──────────────────────────┐     │
    │  │    LLM Client            │     │
    │  │ (OpenAI/Anthropic)       │     │
    │  └──────────────────────────┘     │
    │  ┌──────────────────────────┐     │
    │  │   Configuration          │     │
    │  │   & Settings             │     │
    │  └──────────────────────────┘     │
    └────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Research │  │   Data   │  │ Content  │
│  Agent   │  │   Viz    │  │  Writer  │
│          │  │  Agent   │  │  Agent   │
│ 3 Tools  │  │ 2 Tools  │  │ 2 Tools  │
└──────────┘  └──────────┘  └──────────┘

┌──────────┐  ┌──────────┐  ┌──────────┐
│ Support  │  │Analytics │  │  Email   │
│  Agent   │  │  Agent   │  │  Agent   │
│          │  │          │  │          │
│ Analysis │  │ Analysis │  │ Campaign │
│  Tools   │  │ Methods  │  │  Tools   │
└──────────┘  └──────────┘  └──────────┘

        ┌──────────┐
        │  Social  │
        │  Media   │
        │  Agent   │
        │          │
        │ Platform │
        │  Tools   │
        └──────────┘
```

---

## Workflow System Architecture

```
┌──────┐
│ User │
└───┬──┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│            Workflow Layer                        │
│  ┌──────────────┐  ┌──────────────┐            │
│  │  Research    │  │   Content    │            │
│  │  Workflows   │  │  Workflows   │            │
│  │              │  │              │            │
│  │• Comprehen-  │  │• Full        │            │
│  │  sive        │  │  Pipeline    │            │
│  │• Comparative │  │• Series      │            │
│  │• Trends      │  │• A/B Test    │            │
│  └──────────────┘  └──────────────┘            │
│                                                 │
│  ┌──────────────┐  ┌──────────────┐            │
│  │  Support     │  │  Analytics   │            │
│  │  Workflows   │  │  Workflows   │            │
│  │              │  │              │            │
│  │• Ticket      │  │• Business    │            │
│  │  Lifecycle   │  │  Analysis    │            │
│  │• Batch       │  │• Optimiza-   │            │
│  │  Process     │  │  tion        │            │
│  └──────────────┘  └──────────────┘            │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│              Agent Layer                         │
│     7 Specialized Agents                        │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│              Tool Layer                          │
│     15+ Specialized Tools                       │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│              LLM Layer                           │
│        GPT-4 / Claude                           │
└─────────────────────────────────────────────────┘
    │
    ▼
┌──────┐
│ User │
└──────┘
```

---

## Integrated Workflow Example

```
Research → Content → Social Media → Email

┌──────┐
│ User │ "Create content about AI Trends"
└───┬──┘
    │
    ▼
┌─────────────────────────┐
│  1. Research Workflow   │
│  • Comprehensive        │
│    research on AI       │
│  • Multiple sources     │
│  • Expert synthesis     │
└────────┬────────────────┘
         │ Research Results
         ▼
┌─────────────────────────┐
│  2. Content Workflow    │
│  • Full pipeline        │
│  • SEO optimization     │
│  • Blog post creation   │
└────────┬────────────────┘
         │ Blog Content
         ▼
┌─────────────────────────┐
│  3. Social Workflow     │
│  • Repurpose content    │
│  • Multi-platform       │
│  • Hashtag optimization │
└────────┬────────────────┘
         │ Social Posts
         ▼
┌─────────────────────────┐
│  4. Email Workflow      │
│  • Newsletter creation  │
│  • Subscriber segment   │
│  • Campaign launch      │
└────────┬────────────────┘
         │ Campaign Complete
         ▼
┌──────┐
│ User │ Results Delivered
└──────┘
```

---

## Generating Visual Diagrams

To generate visual PNG diagrams:

```bash
# Install required packages
pip install diagrams
brew install graphviz  # macOS
# or apt-get install graphviz  # Linux

# Generate all diagrams
python generate_diagrams.py
```

This will create PNG files in `docs/diagrams/`:
- `research_architecture.png`
- `visualization_architecture.png`
- `content_architecture.png`
- `support_architecture.png`
- `analytics_architecture.png`
- `email_architecture.png`
- `social_media_architecture.png`
- `overall_architecture.png`
- `workflow_architecture.png`

---

## Key Concepts

### Agent Components
1. **LLM Router**: Central intelligence using GPT-4 or Claude
2. **System Prompt**: Defines agent's role and expertise
3. **Memory**: Maintains conversation context
4. **Tools**: External capabilities and integrations

### Data Flow
```
User Input → LLM Router → Tools/Analysis → LLM Processing → Response
                ↓
             Memory (State Tracking)
```

### Tool Integration
- Tools inherit from `BaseTool`
- Each tool has `execute()` and `tool_definition`
- LLM decides which tools to use
- Results are formatted and returned

---

## Performance Characteristics

| Agent | Avg Response Time | Tools Used | Memory Size |
|-------|------------------|------------|-------------|
| Research | 5-10s | 1-3 | Conversation |
| Visualization | 3-8s | 1-2 | Chart History |
| Content | 10-20s | 0-2 | Content Library |
| Support | 2-5s | 0-2 | Ticket History |
| Analytics | 3-7s | 0 | Analysis History |
| Email | 5-15s | 0 | Campaign History |
| Social Media | 3-8s | 0 | Content Library |

---

For detailed implementation, see individual project READMEs in `projects/*/README.md`
