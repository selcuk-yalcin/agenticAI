# Email Automation Agent - Architecture

## 📊 Project Structure
```
email_automation/
├── README.md                      # Project documentation
├── ARCHITECTURE.md               # This file - how it works
├── __init__.py                   # Package initialization
├── agent.py                      # Main EmailAgent class
├── tools/                        # Email tools
│   ├── __init__.py
│   ├── template_generator.py    # Email template creation
│   ├── personalization.py       # Dynamic content
│   ├── segmentation.py          # Audience targeting
│   └── scheduler.py             # Campaign scheduling
└── workflows/                    # Email workflows
    ├── __init__.py
    └── email_workflow.py        # Campaign automation
```

## 🔄 How It Works

### 1. Campaign Request Arrives
```
Marketer: "Create a welcome email campaign for new subscribers"
   + Subscriber list
   + Brand guidelines
   + Campaign goals
   ↓
```

### 2. Request Goes to EmailAgent
```
email_automation/agent.py
   ├── EmailAgent.__init__()
   │   ├── Loads system prompt: "You are an email marketing expert"
   │   ├── Registers 4 tools: Template, Personalization, Segmentation, Scheduler
   │   └── Connects to OpenAI API
   │
   └── EmailAgent.run(campaign_request)
       ├── Understands campaign goals
       ├── Creates email content
       ├── Personalizes for segments
       ├── Schedules delivery
       └── Returns campaign plan
```

### 3. Tools Are Called (Sequential Flow)

#### Step 1: Segmentation
```
tools/segmentation.py
   └── SegmentationTool.execute(subscriber_list)
       ├── Analyzes subscriber data
       │   ├── Demographics (age, location)
       │   ├── Behavior (opens, clicks)
       │   ├── Purchase history
       │   └── Engagement level
       ├── Creates segments
       │   ├── New subscribers
       │   ├── Active users
       │   ├── VIP customers
       │   └── Inactive subscribers
       ├── Calculates segment sizes
       └── Returns segment definitions
```

#### Step 2: Template Generation
```
tools/template_generator.py
   └── TemplateGeneratorTool.execute(campaign_type, brand)
       ├── Selects template type
       │   ├── Welcome email
       │   ├── Newsletter
       │   ├── Promotional
       │   ├── Transactional
       │   └── Re-engagement
       ├── Creates HTML structure
       │   ├── Header with logo
       │   ├── Hero section
       │   ├── Content blocks
       │   ├── CTA buttons
       │   └── Footer
       ├── Applies brand styling
       │   ├── Colors
       │   ├── Fonts
       │   └── Logos
       └── Returns HTML + plain text
```

#### Step 3: Personalization
```
tools/personalization.py
   └── PersonalizationTool.execute(template, subscriber_data)
       ├── Dynamic fields
       │   ├── {{first_name}}
       │   ├── {{product_recommendations}}
       │   ├── {{location}}
       │   └── {{last_purchase}}
       ├── Content variations
       │   ├── A/B test subject lines
       │   ├── Different CTAs
       │   └── Segment-specific offers
       ├── Smart content
       │   ├── If VIP → special offer
       │   ├── If new → onboarding
       │   └── If inactive → win-back
       └── Returns personalized versions
```

#### Step 4: Scheduling
```
tools/scheduler.py
   └── SchedulerTool.execute(campaign, schedule_params)
       ├── Optimal send time
       │   ├── Based on subscriber timezone
       │   ├── Historical open rates
       │   └── Industry best practices
       ├── Drip sequence timing
       │   ├── Email 1: Immediately
       │   ├── Email 2: +3 days
       │   ├── Email 3: +7 days
       │   └── Email 4: +14 days
       ├── A/B test distribution
       │   ├── Variant A: 45%
       │   ├── Variant B: 45%
       │   └── Winner: 10% (test)
       └── Returns schedule + delivery plan
```

### 4. Workflow Orchestration (Full Campaign)
```
workflows/email_workflow.py
   └── EmailWorkflow.full_campaign_workflow()
       │
       Step 1: Audience Segmentation
       ├── Analyze subscriber list
       ├── Create 3-5 segments
       ├── Define segment criteria
       │
       Step 2: Content Creation
       ├── Generate email templates
       ├── Write compelling copy
       ├── Design CTAs
       │
       Step 3: Personalization
       ├── Add dynamic fields
       ├── Create variations
       ├── A/B test setup
       │
       Step 4: Scheduling
       ├── Set send times
       ├── Configure drip sequence
       ├── Set up triggers
       │
       Step 5: Tracking Setup
       ├── Add tracking pixels
       ├── UTM parameters
       ├── Conversion goals
       │
       Step 6: Preview & Test
       ├── Send test emails
       ├── Check rendering
       └── Launch campaign!
```

### 5. Response Returns to Marketer
```
   ↓
Result:
   ├── Email templates (HTML + plain text)
   ├── Personalization rules
   ├── Segment targeting
   ├── Send schedule
   ├── A/B test configuration
   └── Tracking setup
```

## 🎯 Data Flow Diagram

```
┌─────────┐
│MARKETER │ Campaign brief
└────┬────┘
     │
     ▼
┌──────────────────────────────────────────────┐
│     EmailAgent (agent.py)                    │
│                                              │
│  ┌───────────────────────────────────┐      │
│  │   LLM Router (GPT-4)              │      │
│  │   - Understands campaign goals    │      │
│  │   - Writes compelling copy        │      │
│  │   - Creates CTAs                  │      │
│  │   - Optimizes for conversion      │      │
│  └──────────┬────────────────────────┘      │
│             │                                │
│   ┌─────────┴──────────┐                    │
│   │                    │                    │
│   ▼                    ▼                    │
│ ┌─────────┐      ┌──────────┐              │
│ │ Memory  │      │ Prompt   │              │
│ │ Past    │      │ Brand    │              │
│ │ Campaigns│     │ Voice    │              │
│ └─────────┘      └──────────┘              │
│                                             │
│   ┌─────────────────────────────────┐      │
│   │        Tools (4)                │      │
│   │                                 │      │
│   │  📝 Template Generator          │      │
│   │     ↓ HTML templates            │      │
│   │     ↓ Brand styling             │      │
│   │     ↓ Responsive design         │      │
│   │                                 │      │
│   │  🎯 Personalization             │      │
│   │     ↓ Dynamic fields            │      │
│   │     ↓ Smart content             │      │
│   │     ↓ A/B variants              │      │
│   │                                 │      │
│   │  👥 Segmentation                │      │
│   │     ↓ Audience targeting        │      │
│   │     ↓ Behavior-based            │      │
│   │     ↓ Segment profiles          │      │
│   │                                 │      │
│   │  ⏰ Scheduler                   │      │
│   │     ↓ Optimal timing            │      │
│   │     ↓ Drip sequences            │      │
│   │     ↓ Timezone adjustment       │      │
│   └─────────────────────────────────┘      │
└──────────────────────────────────────────────┘
     │
     ▼
┌─────────┐
│MARKETER │ Ready-to-send campaign
└─────────┘
```

## 🚀 Usage Examples

### Welcome Email
```python
from projects.email_automation.agent import EmailAgent

agent = EmailAgent()
result = agent.run(
    campaign_type="welcome",
    brand={
        "name": "Acme Store",
        "colors": ["#FF5733", "#333333"],
        "tone": "friendly"
    },
    subscribers=new_subscribers
)
print(result)
```

**Flow:**
1. Request → EmailAgent
2. Agent → Template Generator (welcome template)
3. Agent → Personalization (first_name, welcome offer)
4. Agent → Scheduler (immediate send)
5. Result → Welcome email ready

### Drip Campaign
```python
from projects.email_automation.workflows.email_workflow import EmailWorkflow

workflow = EmailWorkflow()
campaign = workflow.drip_campaign_workflow(
    campaign_name="Onboarding Series",
    num_emails=4,
    topics=["Welcome", "Features", "Tips", "Upgrade"],
    subscribers=new_users
)
```

**Flow:**
1. Workflow creates 4-email series
2. Email 1 (Day 0): Welcome + intro
3. Email 2 (Day 3): Feature highlights
4. Email 3 (Day 7): Pro tips
5. Email 4 (Day 14): Upgrade offer
6. Result → Complete drip sequence

### Newsletter
```python
workflow = EmailWorkflow()
newsletter = workflow.newsletter_workflow(
    content_items=[article1, article2, article3],
    frequency="weekly",
    segments=["active_subscribers", "vip_customers"]
)
```

**Flow:**
1. Workflow receives content
2. Step 1: Segment audience (2 segments)
3. Step 2: Create newsletter template
4. Step 3: Personalize for each segment
5. Step 4: Schedule weekly send
6. Result → Recurring newsletter setup

## 🔧 Key Components

### agent.py
- **Purpose:** Main email agent
- **Responsibilities:**
  - Initialize LLM connection
  - Register email tools
  - Create email content
  - Coordinate campaign
- **Key Methods:**
  - `__init__()`: Setup
  - `run(campaign)`: Create campaign
  - `_optimize_subject()`: A/B test subjects

### tools/template_generator.py
- **Purpose:** Email template creation
- **Features:**
  - Pre-built templates
  - Custom HTML generation
  - Responsive design
  - Brand styling
- **Returns:** HTML + plain text

### tools/personalization.py
- **Purpose:** Dynamic content
- **Features:**
  - Merge fields
  - Smart content blocks
  - A/B test variants
  - Conditional content
- **Returns:** Personalized emails

### tools/segmentation.py
- **Purpose:** Audience targeting
- **Features:**
  - Behavior-based segments
  - Demographic segments
  - Engagement segments
  - RFM segments
- **Returns:** Segment definitions

### tools/scheduler.py
- **Purpose:** Campaign scheduling
- **Features:**
  - Optimal send time
  - Timezone adjustment
  - Drip sequences
  - Trigger-based
- **Returns:** Delivery schedule

### workflows/email_workflow.py
- **Purpose:** Campaign automation
- **Features:**
  - Full campaign workflow
  - Drip campaigns
  - Newsletters
  - Transactional emails
  - Re-engagement

## 💡 Campaign Types & When to Use

| Campaign Type | Purpose | Timing | Tools Used |
|--------------|---------|--------|------------|
| Welcome | First impression | Immediate | Template + Personalization |
| Newsletter | Regular updates | Weekly/Monthly | All 4 tools |
| Promotional | Drive sales | Scheduled | Template + Segmentation |
| Transactional | Order updates | Triggered | Template + Scheduler |
| Re-engagement | Win back | Behavior-based | Segmentation + Personalization |
| Drip | Onboarding | Sequential | All 4 tools |

## 📧 Email Template Structure

```
EMAIL TEMPLATE
├── HEADER
│   ├── Logo
│   ├── Navigation (optional)
│   └── Preheader text
│
├── HERO SECTION
│   ├── Main image/graphic
│   ├── Headline
│   └── Subheadline
│
├── CONTENT BLOCKS
│   ├── Text content
│   ├── Images
│   ├── Product listings
│   └── Social proof
│
├── CTA (Call-to-Action)
│   ├── Primary button
│   ├── Secondary button (optional)
│   └── Text link
│
└── FOOTER
    ├── Unsubscribe link
    ├── Social links
    ├── Contact info
    └── Legal text
```

## 🎯 Personalization Variables

```
BASIC PERSONALIZATION
├── {{first_name}}           → "John"
├── {{last_name}}            → "Smith"
├── {{email}}                → "john@example.com"
└── {{signup_date}}          → "Jan 15, 2024"

BEHAVIORAL PERSONALIZATION
├── {{last_purchase}}        → "Running Shoes"
├── {{purchase_date}}        → "2 weeks ago"
├── {{cart_items}}           → 3 items
└── {{browsing_history}}     → Categories viewed

SMART CONTENT
├── IF vip_customer
│   └── Show exclusive offer
├── IF new_subscriber
│   └── Show onboarding
└── IF inactive
    └── Show win-back offer

RECOMMENDATIONS
├── {{recommended_products}} → Based on history
├── {{similar_items}}        → Based on last view
└── {{trending_items}}       → Popular products
```

## ⏰ Drip Campaign Timing

```
ONBOARDING SEQUENCE (4 emails)
Day 0:  Welcome Email
        └── Introduce brand + value

Day 3:  Feature Highlight
        └── Show key features

Day 7:  Tips & Best Practices
        └── Help them succeed

Day 14: Upgrade/Conversion
        └── Special offer

RE-ENGAGEMENT SEQUENCE (3 emails)
Day 0:  "We miss you"
        └── Gentle reminder

Day 7:  Special offer
        └── 20% discount

Day 14: Last chance
        └── Final offer + survey
```

## 📊 A/B Testing Strategy

```
TEST ELEMENTS:

1. SUBJECT LINE
   ├── Version A: "Your exclusive offer inside"
   └── Version B: "20% off just for you"

2. CTA BUTTON
   ├── Version A: "Shop Now"
   └── Version B: "Get My Discount"

3. SEND TIME
   ├── Version A: 9 AM
   └── Version B: 2 PM

4. CONTENT LENGTH
   ├── Version A: Short & punchy
   └── Version B: Detailed & informative

TESTING PROCESS:
Split → 10% to A, 10% to B
Wait → 4 hours
Analyze → Which performed better?
Send Winner → Remaining 80%
```

## 🔍 Reflection & Self-Improvement

Email campaigns benefit greatly from quality checks:

```python
# Reflect on email campaign quality
reflection = agent.reflect(email_campaign, criteria=[
    "Subject line effectiveness",
    "Call-to-action clarity",
    "Personalization level",
    "Conversion potential",
    "Brand voice consistency"
])

print(f"Campaign Quality: {reflection['score']}/10")
```

### Email Reflection Example
```python
{
    "score": 7.5,
    "strengths": [
        "Clear and compelling CTA",
        "Good personalization with {{first_name}}",
        "Mobile-responsive design"
    ],
    "weaknesses": [
        "Subject line could be more specific",
        "Missing urgency element",
        "No secondary CTA"
    ],
    "improvements": [
        "Subject: Add specific benefit (e.g., 'Save 30%')",
        "Add: 'Limited time offer' for urgency",
        "Include: Text link CTA at bottom for accessibility"
    ]
}
```

### A/B Test with Reflection
```python
# Generate two variants and reflect on both
variant_a = agent.run("Write welcome email")
variant_b = agent.reflect(variant_a)['revised_output']

reflection_a = agent.reflect(variant_a)
reflection_b = agent.reflect(variant_b)

print(f"Variant A: {reflection_a['score']}/10")
print(f"Variant B: {reflection_b['score']}/10")

# Use better variant for A/B test
```

See [REFLECTION.md](../../REFLECTION.md) for complete guide.

## 🎓 Technical Details

- **LLM:** OpenAI GPT-4
- **Tools:** 4 (Template, Personalization, Segmentation, Scheduler)
- **Template Engine:** HTML + Jinja2
- **Email Provider:** SMTP / SendGrid / Mailgun (configurable)
- **Response Time:** 10-30 seconds per campaign
- **Personalization Depth:** Unlimited merge fields
- **Segmentation:** Up to 50 segments
- **A/B Testing:** Up to 5 variants
- **Scheduling:** Timezone-aware (all zones)
- **Reflection:** Campaign quality & conversion optimization supported
