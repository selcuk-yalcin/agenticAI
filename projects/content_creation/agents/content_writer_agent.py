"""
Content Writer Agent
===================
Agent specialized in creating various types of content.
"""

from typing import Optional, List, Dict
from core.agents import BaseAgent
from projects.content_creation.tools import (
    keyword_research_tool,
    seo_optimizer_tool,
    get_content_tool_definitions
)


class ContentWriterAgent(BaseAgent):
    """
    Content writer agent for creating blog posts, articles, and marketing copy.
    
    Capabilities:
    - Blog post writing
    - Article creation
    - Marketing copy
    - SEO optimization
    - Keyword integration
    """
    
    SYSTEM_PROMPT = """You are an expert content writer specializing in creating engaging, high-quality content.

Your capabilities:
1. Write blog posts with proper structure (intro, body, conclusion)
2. Create SEO-optimized content
3. Integrate keywords naturally
4. Maintain consistent tone and style
5. Format content with proper headings and structure

Your process:
1. Understand the topic and target audience
2. Research keywords if needed
3. Create outline with clear sections
4. Write engaging introduction
5. Develop content with valuable information
6. Include call-to-action
7. Optimize for SEO

Guidelines:
- Use clear, concise language
- Include relevant keywords naturally
- Structure with H2, H3 headings
- Add meta descriptions
- Keep paragraphs short and readable
- Use active voice
- Provide actionable insights
"""
    
    def __init__(
        self,
        model: Optional[str] = None,
        temperature: float = 0.7,
        enable_seo: bool = True
    ):
        """
        Initialize content writer agent.
        
        Args:
            model: LLM model to use
            temperature: Sampling temperature (higher = more creative)
            enable_seo: Enable SEO optimization tools
        """
        super().__init__(
            name="ContentWriterAgent",
            system_prompt=self.SYSTEM_PROMPT,
            model=model,
            temperature=temperature
        )
        
        # Add content tools
        if enable_seo:
            tools = get_content_tool_definitions()
            self.add_tools(tools, {
                "keyword_research": keyword_research_tool,
                "seo_optimizer": seo_optimizer_tool
            })
    
    def run(self, topic: str, content_type: str = "blog_post", **kwargs):
        """
        Create content based on topic and type.
        
        Args:
            topic: Content topic
            content_type: Type of content (blog_post, article, landing_page, social_post)
            **kwargs: Additional parameters (word_count, keywords, tone, etc.)
            
        Returns:
            Generated content
        """
        # Build prompt based on content type
        if content_type == "blog_post":
            prompt = self._blog_post_prompt(topic, **kwargs)
        elif content_type == "article":
            prompt = self._article_prompt(topic, **kwargs)
        elif content_type == "landing_page":
            prompt = self._landing_page_prompt(topic, **kwargs)
        elif content_type == "social_post":
            prompt = self._social_post_prompt(topic, **kwargs)
        else:
            prompt = f"Create content about: {topic}"
        
        response, _ = self._execute_with_tools(prompt)
        return response
    
    def _blog_post_prompt(self, topic: str, **kwargs) -> str:
        """Generate blog post prompt."""
        word_count = kwargs.get("word_count", 1000)
        keywords = kwargs.get("keywords", [])
        tone = kwargs.get("tone", "professional")
        
        return f"""Write a comprehensive blog post about: {topic}

Requirements:
- Word count: ~{word_count} words
- Tone: {tone}
{f"- Target keywords: {', '.join(keywords)}" if keywords else ""}
- Structure: Introduction, Main sections with H2/H3 headings, Conclusion
- Include: Hook, valuable insights, examples, call-to-action
- SEO: Meta description (150-160 characters)

Format in Markdown with proper headings."""
    
    def _article_prompt(self, topic: str, **kwargs) -> str:
        """Generate article prompt."""
        word_count = kwargs.get("word_count", 1500)
        tone = kwargs.get("tone", "informative")
        
        return f"""Write an informative article about: {topic}

Requirements:
- Word count: ~{word_count} words
- Tone: {tone}
- Include: Introduction, multiple sections with data/facts, conclusion
- Use: Statistics, examples, expert insights
- Format: Markdown with headings

Make it comprehensive and well-researched."""
    
    def _landing_page_prompt(self, topic: str, **kwargs) -> str:
        """Generate landing page prompt."""
        return f"""Create landing page copy for: {topic}

Requirements:
- Compelling headline
- Subheadline explaining benefit
- Key features (3-5 bullet points)
- Social proof section
- Strong call-to-action
- Short paragraphs, scannable format

Focus on conversion and clarity."""
    
    def _social_post_prompt(self, topic: str, **kwargs) -> str:
        """Generate social media post prompt."""
        platform = kwargs.get("platform", "general")
        
        return f"""Create a social media post about: {topic}

Platform: {platform}
Requirements:
- Engaging hook in first line
- Clear message
- Call-to-action
- 1-3 relevant hashtags
- Appropriate length for platform

Make it shareable and engaging."""
    
    def create_blog_series(
        self,
        main_topic: str,
        num_posts: int = 3,
        word_count: int = 1000
    ) -> List[str]:
        """
        Create a series of related blog posts.
        
        Args:
            main_topic: Main topic for the series
            num_posts: Number of posts to create
            word_count: Word count per post
            
        Returns:
            List of blog posts
        """
        # Generate subtopics
        subtopics_prompt = f"""Generate {num_posts} specific subtopics for a blog series about: {main_topic}

Return as a simple numbered list."""
        
        self.messages.append({"role": "user", "content": subtopics_prompt})
        subtopics_response = self._execute_simple("")
        
        # Create posts for each subtopic
        posts = []
        for i in range(num_posts):
            post = self.run(
                topic=f"{main_topic} - Part {i+1}",
                content_type="blog_post",
                word_count=word_count
            )
            posts.append(post)
        
        return posts


def create_content_writer_agent(model: Optional[str] = None, **kwargs) -> ContentWriterAgent:
    """Create a content writer agent with default settings."""
    return ContentWriterAgent(model=model, **kwargs)
