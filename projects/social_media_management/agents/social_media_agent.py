"""
Social Media Management Agent
Automates social media content creation and management.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from core.agents.base_agent import BaseAgent


class SocialMediaAgent(BaseAgent):
    """Agent for social media content creation and management."""
    
    SYSTEM_PROMPT = """You are a social media expert specializing in:
- Engaging content creation
- Platform-specific optimization
- Viral trends and hashtags
- Community engagement
- Brand voice consistency

Create content that resonates, drives engagement, and aligns with platform best practices."""

    def __init__(
        self,
        model: str = "gpt-4-turbo-preview",
        temperature: float = 0.8,
        enable_trending: bool = True
    ):
        super().__init__(
            name="SocialMediaAgent",
            model=model,
            temperature=temperature,
            system_prompt=self.SYSTEM_PROMPT
        )
        self.enable_trending = enable_trending
        
        # Platform character limits
        self.platform_limits = {
            "twitter": 280,
            "instagram": 2200,
            "linkedin": 3000,
            "facebook": 63206,
            "tiktok": 2200
        }

    def create_post(
        self,
        platform: str,
        content_type: str = "general",
        tone: str = "casual",
        include_hashtags: bool = True,
        include_emoji: bool = True
    ) -> Dict[str, Any]:
        """Create a social media post for specific platform."""
        
        char_limit = self.platform_limits.get(platform.lower(), 500)
        
        prompt = f"""Create a {platform} post:

Content Type: {content_type}
Tone: {tone}
Character Limit: {char_limit}
Include Hashtags: {include_hashtags}
Include Emoji: {include_emoji}

Platform-specific best practices:
{self._get_platform_guidelines(platform)}

Provide:
1. Main post text
2. Hashtags (if requested)
3. Emoji suggestions
4. Call-to-action
5. Best posting time recommendation"""
        
        post = self.run(prompt)
        
        return {
            "platform": platform,
            "content": post,
            "content_type": content_type,
            "created_at": datetime.now().isoformat()
        }

    def create_multi_platform_post(
        self,
        base_message: str,
        platforms: List[str],
        adapt_for_platform: bool = True
    ) -> Dict[str, Any]:
        """Create adapted versions of same post for multiple platforms."""
        
        prompt = f"""Adapt this message for multiple platforms:

Base Message: {base_message}

Platforms: {', '.join(platforms)}
Adapt content: {adapt_for_platform}

For each platform:
1. Adapt message length and style
2. Optimize formatting
3. Add platform-specific elements
4. Include appropriate hashtags
5. Maintain core message

Character limits:
{', '.join([f"{p}: {self.platform_limits.get(p, 'N/A')}" for p in platforms])}"""
        
        posts = self.run(prompt)
        
        return {
            "base_message": base_message,
            "platforms": platforms,
            "adapted_posts": posts
        }

    def generate_hashtags(
        self,
        topic: str,
        platform: str = "instagram",
        num_hashtags: int = 15,
        include_trending: bool = True
    ) -> Dict[str, Any]:
        """Generate optimized hashtags for topic."""
        
        prompt = f"""Generate {num_hashtags} hashtags for:

Topic: {topic}
Platform: {platform}
Include trending: {include_trending}

Provide mix of:
1. High-volume hashtags (competitive)
2. Medium-volume hashtags (targeted)
3. Niche hashtags (specific)
4. Branded hashtags

Format: #hashtag
Include estimated reach tier for each."""
        
        hashtags = self.run(prompt)
        
        return {
            "topic": topic,
            "platform": platform,
            "hashtags": hashtags,
            "count": num_hashtags
        }

    def generate_content_calendar(
        self,
        duration_days: int = 30,
        posts_per_day: int = 1,
        themes: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Generate content calendar with post ideas."""
        
        if themes is None:
            themes = ["educational", "promotional", "engagement", "behind-the-scenes"]
        
        total_posts = duration_days * posts_per_day
        
        prompt = f"""Create a {duration_days}-day social media content calendar:

Posts per day: {posts_per_day}
Total posts: {total_posts}
Themes: {', '.join(themes)}

For each post provide:
1. Date and time
2. Platform(s)
3. Content type
4. Topic/theme
5. Brief description
6. Hashtag suggestions
7. Media needs (image/video)

Balance themes throughout the calendar."""
        
        calendar = self.run(prompt)
        
        return {
            "duration_days": duration_days,
            "posts_per_day": posts_per_day,
            "total_posts": total_posts,
            "calendar": calendar
        }

    def create_thread(
        self,
        topic: str,
        num_tweets: int = 5,
        include_hook: bool = True
    ) -> Dict[str, Any]:
        """Create a Twitter/X thread."""
        
        prompt = f"""Create a {num_tweets}-tweet thread on: {topic}

Include attention-grabbing hook: {include_hook}
Character limit per tweet: 280

Structure:
1. Hook tweet (if requested)
2. Main content tweets
3. Call-to-action conclusion

Number each tweet. Make it engaging and informative."""
        
        thread = self.run(prompt)
        
        return {
            "topic": topic,
            "num_tweets": num_tweets,
            "thread": thread
        }

    def analyze_engagement(
        self,
        posts: Optional[List[Dict]] = None,
        metrics: List[str] = None
    ) -> Dict[str, Any]:
        """Analyze engagement patterns and provide insights."""
        
        if metrics is None:
            metrics = ["likes", "comments", "shares", "reach"]
        
        prompt = f"""Analyze social media engagement:

Posts: {len(posts) if posts else "Sample dataset"}
Metrics: {', '.join(metrics)}

Provide insights on:
1. Best performing content types
2. Optimal posting times
3. Engagement patterns
4. Content recommendations
5. Hashtag effectiveness
6. Improvement opportunities"""
        
        analysis = self.run(prompt)
        
        return {
            "metrics": metrics,
            "analysis": analysis,
            "analyzed_at": datetime.now().isoformat()
        }

    def generate_caption(
        self,
        content_description: str,
        style: str = "engaging",
        max_length: Optional[int] = None
    ) -> Dict[str, Any]:
        """Generate caption for image/video content."""
        
        prompt = f"""Create a caption for:

Content: {content_description}
Style: {style}
Max length: {max_length if max_length else "flexible"}

Include:
1. Engaging opening
2. Context/story
3. Call-to-action
4. Hashtag suggestions
5. Emoji recommendations

Make it attention-grabbing and relevant."""
        
        caption = self.run(prompt)
        
        return {
            "content_description": content_description,
            "caption": caption,
            "style": style
        }

    def repurpose_content(
        self,
        original_content: str,
        from_platform: str,
        to_platform: str
    ) -> Dict[str, Any]:
        """Repurpose content from one platform to another."""
        
        prompt = f"""Repurpose this content:

Original: {original_content}
From: {from_platform}
To: {to_platform}

Adapt for {to_platform}:
1. Adjust length and format
2. Optimize style
3. Add platform-specific elements
4. Maintain core message
5. Update hashtags/mentions"""
        
        repurposed = self.run(prompt)
        
        return {
            "original": original_content,
            "from_platform": from_platform,
            "to_platform": to_platform,
            "repurposed_content": repurposed
        }

    def _get_platform_guidelines(self, platform: str) -> str:
        """Get platform-specific guidelines."""
        guidelines = {
            "twitter": "Short, punchy, use threads for longer content",
            "instagram": "Visual-first, story-driven captions, hashtags important",
            "linkedin": "Professional tone, thought leadership, industry insights",
            "facebook": "Conversational, community-focused, varied content types",
            "tiktok": "Trendy, entertaining, hook in first 3 seconds"
        }
        return guidelines.get(platform.lower(), "Engaging, authentic content")


def create_social_media_agent(**kwargs) -> SocialMediaAgent:
    """Factory function to create a SocialMediaAgent."""
    return SocialMediaAgent(**kwargs)
