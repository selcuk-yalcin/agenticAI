# Content Creation Project

AI-powered content writing agent for creating engaging, SEO-optimized content.

## Overview

The ContentWriterAgent specializes in creating various types of content including blog posts, articles, landing pages, and social media posts with built-in SEO optimization.

## Features

- **Blog Post Writing:** Create comprehensive blog posts with proper structure
- **Article Creation:** Generate informative, well-researched articles
- **Landing Pages:** Write conversion-focused landing page copy
- **Social Media Posts:** Create engaging social media content
- **SEO Optimization:** Built-in keyword research and optimization
- **Content Series:** Generate related content series

## Agent

### ContentWriterAgent

Creates high-quality content with SEO optimization.

**Capabilities:**
- Multiple content types
- Keyword integration
- SEO optimization
- Tone customization
- Structured formatting

## Tools

### keyword_research
Research relevant keywords for a topic (simulated - integrate with real API in production).

### seo_optimizer
Analyze content and provide SEO optimization suggestions.

## Usage

### Basic Blog Post

```python
from projects.content_creation import ContentWriterAgent

agent = ContentWriterAgent()

blog_post = agent.run(
    topic="Introduction to Machine Learning",
    content_type="blog_post",
    word_count=1200,
    tone="professional"
)

print(blog_post)
```

### With Keywords

```python
agent = ContentWriterAgent()

article = agent.run(
    topic="Best Practices for Remote Work",
    content_type="article",
    word_count=1500,
    keywords=["remote work", "productivity", "work from home"],
    tone="informative"
)
```

### Landing Page Copy

```python
agent = ContentWriterAgent()

landing_page = agent.run(
    topic="Project Management Software",
    content_type="landing_page"
)
```

### Social Media Post

```python
agent = ContentWriterAgent()

social_post = agent.run(
    topic="New Product Launch",
    content_type="social_post",
    platform="linkedin"
)
```

### Blog Series

```python
agent = ContentWriterAgent()

series = agent.create_blog_series(
    main_topic="Digital Marketing Fundamentals",
    num_posts=5,
    word_count=1000
)

for i, post in enumerate(series, 1):
    print(f"Post {i}:\n{post}\n")
```

## Content Types

### blog_post
- Full blog post with introduction, main sections, conclusion
- 800-2000 words typically
- SEO-optimized with headings
- Includes meta description

### article
- Comprehensive informative article
- 1000-2500 words typically
- Data and fact-driven
- Multiple sections

### landing_page
- Conversion-focused copy
- Headline, benefits, features, CTA
- Short and scannable
- Persuasive tone

### social_post
- Platform-appropriate content
- Engaging hook
- Clear message
- Call-to-action and hashtags

## Configuration

```python
# Higher temperature for more creative content
agent = ContentWriterAgent(
    model="gpt-4-turbo-preview",
    temperature=0.8,  # Default: 0.7
    enable_seo=True
)
```

## Parameters

### Common Parameters

- **topic:** Main subject of the content
- **content_type:** Type of content to create
- **word_count:** Target word count
- **keywords:** List of target keywords
- **tone:** Writing tone (professional, casual, informative, persuasive)
- **platform:** For social posts (linkedin, twitter, facebook)

## Best Practices

1. **Be Specific:** Provide clear topic and requirements
2. **Use Keywords:** Supply target keywords for SEO
3. **Define Tone:** Specify desired tone for consistent voice
4. **Review Output:** Always review and edit generated content
5. **Test SEO:** Use SEO tools to verify optimization

## Integration

### Save Content

```python
from core.utils import save_markdown

content = agent.run(topic="...", content_type="blog_post")
filepath = save_markdown(content, "blog_post", "./outputs/content")
```

### With Research

```python
from projects.research import ResearchAgent
from projects.content_creation import ContentWriterAgent

# Research first
researcher = ResearchAgent()
research = researcher.run("Latest AI trends")

# Then create content
writer = ContentWriterAgent()
article = writer.run(
    topic="Latest AI Trends 2024",
    content_type="article",
    word_count=1500
)
```

## Examples

See `examples/` directory for detailed usage examples.

## Notes

- Keyword research tool is simulated - integrate with real SEO APIs in production
- Always review and edit AI-generated content
- Adjust temperature for creativity vs consistency balance
- Consider brand voice guidelines when generating content

## Dependencies

- OpenAI API (required)
- Temperature 0.7 recommended for creative content
- SEO tools optional but recommended for production

## Future Enhancements

- Integration with real SEO APIs (SEMrush, Ahrefs)
- Plagiarism checking
- Readability scoring
- Content scheduling
- Multi-language support
