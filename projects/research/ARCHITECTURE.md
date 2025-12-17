# Research Agent - Architecture

## 📊 Project Structure
```
research/
├── README.md                  # Project documentation
├── ARCHITECTURE.md           # This file - how it works
├── __init__.py               # Package initialization
├── agent.py                  # Main ResearchAgent class
├── tools/                    # Research tools
│   ├── __init__.py
│   ├── tavily_search.py     # Web search tool
│   ├── wikipedia_tool.py    # Encyclopedia lookup
│   └── arxiv_tool.py        # Academic papers
└── workflows/                # Multi-step workflows
    ├── __init__.py
    └── research_workflow.py  # Orchestration logic
```

## 🔄 How It Works

### 1. User Makes Request
```
User: "Research latest AI developments"
   ↓
```

### 2. Request Goes to ResearchAgent
```
research/agent.py
   ├── ResearchAgent.__init__()
   │   ├── Loads system prompt: "You are an expert research assistant"
   │   ├── Registers 3 tools: Tavily, Wikipedia, arXiv
   │   └── Connects to OpenAI API
   │
   └── ResearchAgent.run(query)
       ├── Sends query + tools to GPT-4
       ├── LLM decides which tools to use
       └── Returns synthesized results
```

### 3. Tools Are Called (Based on LLM Decision)
```
tools/tavily_search.py
   └── TavilySearchTool.execute()
       ├── Searches current web content
       ├── Returns latest news & articles
       └── Provides source URLs

tools/wikipedia_tool.py
   └── WikipediaTool.execute()
       ├── Looks up encyclopedia entries
       ├── Returns factual background
       └── Provides context

tools/arxiv_tool.py
   └── ArxivTool.execute()
       ├── Searches academic papers
       ├── Returns scientific research
       └── Provides citations
```

### 4. Workflow Orchestration (Optional)
```
workflows/research_workflow.py
   └── ResearchWorkflow.comprehensive_research()
       │
       Step 1: Web search for current info
       ├── agent.run("search latest developments")
       │
       Step 2: Get background from Wikipedia
       ├── agent.run("get overview from Wikipedia")
       │
       Step 3: Find academic papers
       ├── agent.run("search arXiv papers")
       │
       Step 4: Synthesize all findings
       └── agent.run("combine and analyze all results")
```

### 5. Response Returns to User
```
   ↓
Result:
   ├── Comprehensive research report
   ├── Multiple sources cited
   ├── Current + Historical context
   └── Academic backing
```

## 🎯 Data Flow Diagram

```
┌─────────┐
│  USER   │ "Research AI trends"
└────┬────┘
     │
     ▼
┌─────────────────────────────────────────┐
│     ResearchAgent (agent.py)            │
│                                         │
│  ┌──────────────────────────────┐      │
│  │   LLM Router (GPT-4)         │      │
│  │   - Analyzes query           │      │
│  │   - Decides which tools      │      │
│  │   - Combines results         │      │
│  └──────────┬───────────────────┘      │
│             │                           │
│   ┌─────────┴──────────┐               │
│   │                    │               │
│   ▼                    ▼               │
│ ┌─────────┐      ┌──────────┐         │
│ │ Memory  │      │ Prompt   │         │
│ │ History │      │ Context  │         │
│ └─────────┘      └──────────┘         │
│                                        │
│   ┌────────────────────────────┐      │
│   │        Tools               │      │
│   │                            │      │
│   │  🔍 Tavily Search         │      │
│   │     ↓ Current web data    │      │
│   │                            │      │
│   │  📚 Wikipedia             │      │
│   │     ↓ Encyclopedia info   │      │
│   │                            │      │
│   │  📄 arXiv                 │      │
│   │     ↓ Academic papers     │      │
│   └────────────────────────────┘      │
└─────────────────────────────────────────┘
     │
     ▼
┌─────────┐
│ RESULT  │ Comprehensive research report
└─────────┘
```

## 🚀 Usage Examples

### Simple Query
```python
from projects.research.agent import ResearchAgent

agent = ResearchAgent()
result = agent.run("What are the latest developments in quantum computing?")
print(result)
```

**Flow:**
1. User query → ResearchAgent
2. Agent → GPT-4 with tools
3. GPT-4 decides → Use Tavily + Wikipedia + arXiv
4. Tools execute → Return data
5. GPT-4 synthesizes → Comprehensive answer
6. Result → User

### Workflow Query
```python
from projects.research.workflows.research_workflow import ResearchWorkflow

workflow = ResearchWorkflow()
result = workflow.comprehensive_research(
    topic="AI Ethics",
    depth="detailed"
)
```

**Flow:**
1. Workflow orchestrates multiple steps
2. Step 1: Web search (Tavily)
3. Step 2: Background (Wikipedia)
4. Step 3: Papers (arXiv)
5. Step 4: Synthesis (GPT-4)
6. Complete report → User

## 🔧 Key Components

### agent.py
- **Purpose:** Main agent class
- **Responsibilities:** 
  - Initialize LLM connection
  - Register tools
  - Handle queries
  - Manage conversation history
- **Key Methods:**
  - `__init__()`: Setup
  - `run(query)`: Execute query
  - `_register_tools()`: Add tools

### tools/
- **Purpose:** External data sources
- **tavily_search.py:** Real-time web search
- **wikipedia_tool.py:** Encyclopedia facts
- **arxiv_tool.py:** Academic research
- **Each tool:**
  - Inherits from `BaseTool`
  - Implements `execute()` method
  - Returns structured data

### workflows/
- **Purpose:** Multi-step orchestration
- **research_workflow.py:** Complex research tasks
- **Features:**
  - Sequential steps
  - Error handling
  - Progress tracking
  - Result combination

## 💡 When to Use What

| Task | Use | Why |
|------|-----|-----|
| Quick fact check | `agent.run()` | Single query, fast |
| Current news | Tavily tool | Real-time data |
| Background info | Wikipedia tool | Factual context |
| Academic research | arXiv tool | Scientific papers |
| Comprehensive report | Workflow | Multiple sources + synthesis |
| Comparative analysis | Workflow | Structured multi-step |

## 🔍 Reflection & Self-Improvement

The Research Agent supports **self-evaluation** to ensure high-quality research outputs:

```python
from projects.research.agent import ResearchAgent

agent = ResearchAgent()

# Run with reflection
result = agent.run_with_reflection(
    "Research latest AI developments",
    auto_improve=True,
    max_iterations=2
)

print(f"Quality Score: {result['reflection']['score']}/10")
print(f"Improvements made: {result['iterations']}")
```

### Reflection Criteria (Research-Specific)
- ✅ **Source diversity:** Multiple credible sources used
- ✅ **Citation accuracy:** Proper attribution and references
- ✅ **Factual correctness:** Information is accurate and verified
- ✅ **Balanced perspective:** Multiple viewpoints considered
- ✅ **Current information:** Up-to-date data and findings

### Example Reflection Output
```python
{
    "score": 8.5,
    "strengths": [
        "Used diverse sources (web, encyclopedia, academic)",
        "Proper citations included",
        "Current information from 2024"
    ],
    "weaknesses": [
        "Could include more academic papers",
        "Missing comparison with classical methods"
    ],
    "improvements": [
        "Add 2-3 more arXiv papers for depth",
        "Include practical applications section"
    ]
}
```

See [REFLECTION.md](../../REFLECTION.md) for complete guide.

## 🎓 Technical Details

- **LLM:** OpenAI GPT-4
- **Tools:** 3 (Tavily, Wikipedia, arXiv)
- **Response Time:** 5-15 seconds per query
- **Max Token:** Configurable (default: 4000)
- **Error Handling:** Automatic retry with fallbacks
- **Reflection:** Self-evaluation & auto-improvement supported
