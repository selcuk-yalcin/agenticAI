# Social Media Management Agent - Architecture

## 📊 Project Structure
```
social_media_management/
├── README.md                          # Project documentation
├── ARCHITECTURE.md                   # This file - how it works
├── __init__.py                       # Package initialization
├── agent.py                          # Main SocialMediaAgent class
├── tools/                            # Social media tools
│   ├── __init__.py
│   ├── content_generator.py         # Post creation
│   ├── hashtag_researcher.py        # Hashtag discovery
│   ├── image_generator.py           # Visual content
│   ├── scheduling_optimizer.py      # Best posting times
│   └── analytics_tracker.py         # Performance metrics
└── workflows/                        # Social workflows
    ├── __init__.py
    └── social_media_workflow.py     # Campaign automation
```

## 🔄 How It Works

### 1. Content Request Arrives
```
Social Media Manager: "Create a week of Instagram posts about our new product"
   + Product info
   + Brand guidelines
   + Target audience
   + Platforms (Instagram, Twitter, LinkedIn)
   ↓
```

### 2. Request Goes to SocialMediaAgent
```
social_media_management/agent.py
   ├── SocialMediaAgent.__init__()
   │   ├── Loads system prompt: "You are a social media expert"
   │   ├── Registers 5 tools: Content, Hashtags, Images, Scheduling, Analytics
   │   └── Connects to OpenAI API
   │
   └── SocialMediaAgent.run(campaign_request)
       ├── Understands campaign goals
       ├── Creates platform-specific content
       ├── Generates visuals
       ├── Researches hashtags
       ├── Schedules posts
       └── Returns complete campaign
```

### 3. Tools Are Called (Sequential & Parallel)

#### Step 1: Content Generation (Per Platform)
```
tools/content_generator.py
   └── ContentGeneratorTool.execute(topic, platform, brand_voice)
       │
       ├── INSTAGRAM POST
       │   ├── Character limit: 2,200
       │   ├── Style: Visual-first, emoji-rich
       │   ├── Structure:
       │   │   ├── Hook (first line)
       │   │   ├── Value/Story (middle)
       │   │   ├── Call-to-action
       │   │   └── Hashtags (up to 30)
       │   └── Output: Caption + image description
       │
       ├── TWITTER/X POST
       │   ├── Character limit: 280
       │   ├── Style: Concise, witty
       │   ├── Structure:
       │   │   ├── Hook (first 10 words)
       │   │   ├── Key message
       │   │   └── CTA or question
       │   └── Output: Tweet + thread (if needed)
       │
       ├── LINKEDIN POST
       │   ├── Character limit: 3,000
       │   ├── Style: Professional, insightful
       │   ├── Structure:
       │   │   ├── Attention-grabbing opener
       │   │   ├── Professional insights
       │   │   ├── Industry relevance
       │   │   └── Thought-provoking question
       │   └── Output: Post + article (optional)
       │
       ├── FACEBOOK POST
       │   ├── Character limit: 63,206
       │   ├── Style: Conversational, community
       │   ├── Structure:
       │   │   ├── Engaging story
       │   │   ├── Community focus
       │   │   └── Interactive element
       │   └── Output: Post + link preview
       │
       └── TIKTOK SCRIPT
           ├── Duration: 15-60 seconds
           ├── Style: Fast-paced, trendy
           ├── Structure:
           │   ├── Hook (0-3s)
           │   ├── Content (3-45s)
           │   └── CTA (45-60s)
           └── Output: Script + music suggestions
```

#### Step 2: Hashtag Research (Parallel)
```
tools/hashtag_researcher.py
   └── HashtagResearcherTool.execute(topic, platform)
       ├── Analyzes topic keywords
       ├── Finds trending hashtags
       │   ├── High volume (#fitness - 100M posts)
       │   ├── Medium volume (#homeworkout - 10M posts)
       │   └── Niche/branded (#YourBrand - 1K posts)
       ├── Checks hashtag difficulty
       ├── Recommends mix
       │   ├── 3-5 popular hashtags
       │   ├── 5-10 medium hashtags
       │   └── 5-10 niche hashtags
       └── Returns hashtag strategy
```

#### Step 3: Image Generation (Parallel)
```
tools/image_generator.py
   └── ImageGeneratorTool.execute(content, style, platform)
       ├── Generates image prompt
       │   ├── Based on content theme
       │   ├── Brand colors/style
       │   └── Platform dimensions
       ├── Platform-specific sizing
       │   ├── Instagram: 1080x1080 (square)
       │   ├── Twitter: 1200x675 (landscape)
       │   ├── LinkedIn: 1200x627 (landscape)
       │   ├── Facebook: 1200x630 (landscape)
       │   └── TikTok: 1080x1920 (vertical)
       ├── Creates image variations
       │   ├── With text overlay
       │   ├── Without text
       │   └── Multiple color schemes
       └── Returns image files + alt text
```

#### Step 4: Scheduling Optimization
```
tools/scheduling_optimizer.py
   └── SchedulingOptimizerTool.execute(posts, platform, audience)
       ├── Analyzes best posting times
       │   ├── Historical engagement data
       │   ├── Audience timezone
       │   └── Platform algorithms
       ├── Optimal times by platform
       │   ├── Instagram: 11 AM, 2 PM, 7 PM
       │   ├── Twitter: 9 AM, 12 PM, 5 PM
       │   ├── LinkedIn: 8 AM, 12 PM, 6 PM
       │   ├── Facebook: 1 PM, 3 PM, 7 PM
       │   └── TikTok: 6 AM, 10 AM, 7 PM, 9 PM
       ├── Creates posting schedule
       │   ├── Frequency: 1-3 posts/day
       │   ├── Spacing: Min 4 hours apart
       │   └── Weekend adjustments
       └── Returns schedule + rationale
```

#### Step 5: Analytics Tracking Setup
```
tools/analytics_tracker.py
   └── AnalyticsTrackerTool.execute(campaign)
       ├── Sets up tracking
       │   ├── UTM parameters
       │   ├── Link shorteners
       │   └── Conversion pixels
       ├── Defines KPIs
       │   ├── Reach & Impressions
       │   ├── Engagement rate
       │   ├── Click-through rate (CTR)
       │   └── Conversion rate
       ├── Creates dashboard
       │   ├── Real-time metrics
       │   ├── Comparison charts
       │   └── Performance alerts
       └── Returns tracking setup
```

### 4. Workflow Orchestration (Full Campaign)
```
workflows/social_media_workflow.py
   └── SocialMediaWorkflow.full_campaign_workflow()
       │
       Step 1: Campaign Planning
       ├── Define goals (reach, engagement, conversions)
       ├── Identify target audience
       ├── Select platforms
       │
       Step 2: Content Creation
       ├── Generate posts for each platform
       ├── Adapt messaging per platform
       ├── Create visual assets
       │
       Step 3: Hashtag Strategy
       ├── Research trending hashtags
       ├── Create branded hashtags
       ├── Build hashtag sets per post
       │
       Step 4: Visual Content
       ├── Generate images/graphics
       ├── Platform-specific sizing
       ├── A/B test variations
       │
       Step 5: Scheduling
       ├── Optimize posting times
       ├── Create content calendar
       ├── Set up auto-posting
       │
       Step 6: Analytics
       ├── Track performance
       ├── Monitor engagement
       └── Generate reports
```

### 5. Response Returns to Manager
```
   ↓
Result:
   ├── Content for each platform
   ├── Visual assets (images/videos)
   ├── Hashtag strategy
   ├── Posting schedule
   ├── Analytics dashboard
   └── Performance tracking
```

## 🎯 Data Flow Diagram

```
┌─────────┐
│SOCIAL   │ Campaign brief
│MEDIA MGR│
└────┬────┘
     │
     ▼
┌───────────────────────────────────────────────┐
│     SocialMediaAgent (agent.py)               │
│                                               │
│  ┌────────────────────────────────────┐      │
│  │   LLM Router (GPT-4)               │      │
│  │   - Creates engaging content       │      │
│  │   - Adapts to platform style       │      │
│  │   - Optimizes for algorithms       │      │
│  │   - Maximizes engagement           │      │
│  └──────────┬─────────────────────────┘      │
│             │                                 │
│   ┌─────────┴──────────┐                     │
│   │                    │                     │
│   ▼                    ▼                     │
│ ┌─────────┐      ┌──────────┐               │
│ │ Memory  │      │ Prompt   │               │
│ │ Past    │      │ Brand    │               │
│ │ Posts   │      │ Voice    │               │
│ └─────────┘      └──────────┘               │
│                                              │
│   ┌──────────────────────────────────┐      │
│   │        Tools (5)                 │      │
│   │                                  │      │
│   │  ✍️ Content Generator            │      │
│   │     ↓ Instagram captions         │      │
│   │     ↓ Tweets                     │      │
│   │     ↓ LinkedIn posts             │      │
│   │     ↓ Facebook updates           │      │
│   │     ↓ TikTok scripts             │      │
│   │                                  │      │
│   │  #️⃣ Hashtag Researcher           │      │
│   │     ↓ Trending tags              │      │
│   │     ↓ Niche tags                 │      │
│   │     ↓ Branded tags               │      │
│   │                                  │      │
│   │  🎨 Image Generator              │      │
│   │     ↓ Graphics                   │      │
│   │     ↓ Platform-sized             │      │
│   │     ↓ Brand-styled               │      │
│   │                                  │      │
│   │  ⏰ Scheduling Optimizer         │      │
│   │     ↓ Best times                 │      │
│   │     ↓ Content calendar           │      │
│   │     ↓ Auto-posting               │      │
│   │                                  │      │
│   │  📊 Analytics Tracker            │      │
│   │     ↓ Engagement metrics         │      │
│   │     ↓ Performance reports        │      │
│   │     ↓ ROI tracking               │      │
│   └──────────────────────────────────┘      │
└───────────────────────────────────────────────┘
     │
     ▼
┌─────────┐
│SOCIAL   │ Complete campaign
│MEDIA MGR│
└─────────┘
```

## 🚀 Usage Examples

### Single Instagram Post
```python
from projects.social_media_management.agent import SocialMediaAgent

agent = SocialMediaAgent()
result = agent.run(
    platform="instagram",
    content_type="product_announcement",
    product_info="New eco-friendly water bottle",
    brand_voice="energetic and eco-conscious"
)
print(result)
```

**Flow:**
1. Request → SocialMediaAgent
2. Agent → Content Generator (Instagram caption)
3. Agent → Hashtag Researcher (eco, sustainable, etc.)
4. Agent → Image Generator (product photo with branding)
5. Result → Complete Instagram post ready

### Multi-Platform Campaign
```python
from projects.social_media_management.workflows.social_media_workflow import SocialMediaWorkflow

workflow = SocialMediaWorkflow()
campaign = workflow.full_campaign_workflow(
    campaign_name="Summer Sale 2024",
    platforms=["instagram", "twitter", "linkedin"],
    duration_days=7,
    posts_per_day=2
)
```

**Flow:**
1. Workflow plans 7-day campaign
2. Creates 14 posts per platform (7 days × 2 posts)
3. For each post:
   - Generate platform-specific content
   - Research hashtags
   - Create images
   - Schedule optimal time
4. Result → 42 posts ready across 3 platforms

### Content Repurposing
```python
workflow = SocialMediaWorkflow()
repurposed = workflow.content_repurposing_workflow(
    source_content=blog_post,
    target_platforms=["instagram", "twitter", "linkedin", "tiktok"]
)
```

**Flow:**
1. Receives blog post (1500 words)
2. Extracts key points
3. Adapts for Instagram: Carousel with 5 key takeaways
4. Adapts for Twitter: Thread with 7 tweets
5. Adapts for LinkedIn: Professional insights post
6. Adapts for TikTok: 60-second video script
7. Result → 1 blog → 4 social posts

## 🔧 Key Components

### agent.py
- **Purpose:** Main social media agent
- **Responsibilities:**
  - Initialize LLM connection
  - Register social tools
  - Create platform-specific content
  - Coordinate campaigns
- **Key Methods:**
  - `__init__()`: Setup
  - `run(campaign)`: Create content
  - `_adapt_platform()`: Platform optimization

### tools/content_generator.py
- **Purpose:** Create social posts
- **Features:**
  - Platform-specific formats
  - Character limits
  - Engagement optimization
  - Brand voice consistency
- **Returns:** Post content

### tools/hashtag_researcher.py
- **Purpose:** Hashtag strategy
- **Features:**
  - Trending hashtag discovery
  - Volume & difficulty analysis
  - Mix recommendations
  - Branded hashtag creation
- **Returns:** Hashtag sets

### tools/image_generator.py
- **Purpose:** Visual content
- **Features:**
  - AI image generation
  - Platform-specific sizing
  - Brand styling
  - Text overlays
- **Returns:** Image files

### tools/scheduling_optimizer.py
- **Purpose:** Post timing
- **Features:**
  - Best time analysis
  - Timezone adjustment
  - Frequency optimization
  - Content calendar
- **Returns:** Schedule

### tools/analytics_tracker.py
- **Purpose:** Performance monitoring
- **Features:**
  - Engagement tracking
  - Reach metrics
  - Conversion tracking
  - ROI calculation
- **Returns:** Analytics dashboard

### workflows/social_media_workflow.py
- **Purpose:** Campaign automation
- **Features:**
  - Full campaigns
  - Content repurposing
  - Viral content creation
  - Influencer collaboration
  - Crisis management

## 💡 Platform-Specific Best Practices

| Platform | Best Content | Optimal Length | Best Time | Hashtags |
|----------|-------------|----------------|-----------|----------|
| Instagram | Visual stories, lifestyle | 125-150 chars | 11AM, 2PM, 7PM | 20-30 |
| Twitter/X | News, quick updates | 71-100 chars | 9AM, 12PM, 5PM | 1-2 |
| LinkedIn | Professional insights | 1,200-1,900 chars | 8AM, 12PM, 6PM | 3-5 |
| Facebook | Community stories | 40-80 chars | 1PM, 3PM, 7PM | 1-3 |
| TikTok | Trendy, entertaining | 15-60 seconds | 6AM, 10AM, 7PM | 3-5 |

## 📝 Content Templates

```
PRODUCT ANNOUNCEMENT
Instagram:
   🎉 [Hook with emoji]
   Introducing [Product Name]!
   
   [Benefits - 3 bullet points]
   • Benefit 1
   • Benefit 2
   • Benefit 3
   
   [CTA] Tap link in bio to shop!
   
   #hashtag1 #hashtag2 ... (20-30 tags)

Twitter:
   🚀 Big news! [Product Name] is here.
   
   [One key benefit] → [CTA link]
   
   #hashtag1 #hashtag2

LinkedIn:
   We're excited to announce [Product Name]!
   
   [Professional context - 2-3 paragraphs]
   
   [Industry relevance]
   
   What do you think? Share your thoughts below. 👇
```

## 📊 Engagement Optimization

```
HOOK STRATEGIES (First 3 seconds/words)
├── Question: "Ever wondered...?"
├── Surprising fact: "Did you know...?"
├── Bold statement: "This changes everything"
├── Personal story: "Last week I..."
└── FOMO: "Don't miss out on..."

CONTENT STRUCTURE
├── Hook (capture attention)
├── Value (provide insight/entertainment)
├── Engagement (ask question, poll)
└── CTA (clear next step)

ENGAGEMENT BOOSTERS
├── Ask questions
├── Use polls/quizzes
├── Respond to comments quickly
├── Tag relevant accounts
├── Use trending audio (TikTok/Reels)
└── Post consistently
```

## 🔍 Reflection & Self-Improvement

Social media engagement depends on content quality:

```python
# Reflect on social post quality
reflection = agent.reflect(social_post, criteria=[
    "Engagement potential",
    "Platform appropriateness",
    "Hashtag strategy",
    "Visual appeal description",
    "Call-to-action effectiveness",
    "Brand voice consistency"
])

print(f"Post Quality: {reflection['score']}/10")
print(f"Engagement Prediction: {reflection['strengths']}")
```

### Social Media Reflection Example
```python
{
    "score": 8.0,
    "strengths": [
        "Strong hook with question",
        "Good hashtag mix (popular + niche)",
        "Clear CTA for engagement",
        "On-brand voice and tone"
    ],
    "weaknesses": [
        "Could be more concise (currently 180 chars)",
        "Missing trending hashtag",
        "No mention of tagging relevant accounts"
    ],
    "improvements": [
        "Reduce to 120-150 chars for better mobile readability",
        "Add trending #MondayMotivation",
        "Suggest: 'Tag a friend who needs this!'",
        "Include: '@[influencer]' for potential reshare"
    ]
}
```

### Platform-Specific Quality Checks
```python
# Instagram post with auto-improvement
instagram_post = agent.run_with_reflection(
    "Create motivational post about fitness",
    platform="instagram",
    auto_improve=True,
    max_iterations=2
)

# Ensures optimal format for Instagram:
# - Engaging first line (hook)
# - Proper hashtag count (20-30)
# - Emoji usage
# - Call-to-action
```

### Batch Quality Control
```python
# Generate week of posts with quality threshold
posts = []
for topic in weekly_topics:
    result = agent.run_with_reflection(
        topic,
        auto_improve=True
    )
    
    # Only publish if quality score >= 8.0
    if result['reflection']['score'] >= 8.0:
        posts.append(result['output'])
    else:
        print(f"⚠️ Low quality ({result['reflection']['score']}): {topic}")
```

See [REFLECTION.md](../../REFLECTION.md) for complete guide.

## 🎓 Technical Details

- **LLM:** OpenAI GPT-4
- **Tools:** 5 (Content, Hashtags, Images, Scheduling, Analytics)
- **Platforms:** Instagram, Twitter, LinkedIn, Facebook, TikTok
- **Image Generation:** DALL-E or Stable Diffusion
- **Response Time:** 15-45 seconds per post
- **Batch Processing:** Up to 100 posts
- **Scheduling:** Timezone-aware (all zones)
- **Analytics:** Real-time tracking
- **A/B Testing:** Supported for all content types
- **Reflection:** Engagement & platform optimization supported
