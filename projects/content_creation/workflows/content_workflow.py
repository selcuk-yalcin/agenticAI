"""
Content Creation Workflow
End-to-end content production pipeline
"""

from typing import Dict, Any, List, Optional
from ..agents.content_writer_agent import ContentWriterAgent


class ContentWorkflow:
    """Orchestrates content creation from ideation to publication."""
    
    def __init__(self):
        self.agent = ContentWriterAgent()
        self.content_library = []
    
    def full_content_pipeline(
        self,
        topic: str,
        content_type: str = "blog_post",
        target_audience: str = "general"
    ) -> Dict[str, Any]:
        """
        Complete content creation pipeline.
        
        Steps:
        1. Keyword research
        2. Content outline
        3. Draft creation
        4. SEO optimization
        5. Final polish
        
        Args:
            topic: Content topic
            content_type: Type of content to create
            target_audience: Target audience description
        
        Returns:
            Complete content package
        """
        print(f"Starting content pipeline for: {topic}")
        
        # Step 1: Keyword research
        print("Step 1: Researching keywords...")
        keywords = self._research_keywords(topic)
        
        # Step 2: Create outline
        print("Step 2: Creating outline...")
        outline = self._create_outline(topic, content_type, target_audience)
        
        # Step 3: Draft content
        print("Step 3: Writing draft...")
        draft = self.agent.run(
            topic=topic,
            content_type=content_type,
            keywords=keywords,
            target_audience=target_audience
        )
        
        # Step 4: SEO optimization
        print("Step 4: Optimizing for SEO...")
        optimized = self._optimize_seo(draft, keywords)
        
        # Step 5: Final review
        print("Step 5: Final review...")
        final_content = self._final_review(optimized, content_type)
        
        result = {
            "topic": topic,
            "content_type": content_type,
            "keywords": keywords,
            "outline": outline,
            "draft": draft,
            "optimized_content": optimized,
            "final_content": final_content,
            "metadata": {
                "target_audience": target_audience,
                "word_count": len(final_content.split())
            }
        }
        
        self.content_library.append(result)
        return result
    
    def content_series(
        self,
        main_topic: str,
        num_posts: int = 5,
        content_type: str = "blog_post"
    ) -> Dict[str, Any]:
        """
        Create a series of related content pieces.
        
        Args:
            main_topic: Main topic for the series
            num_posts: Number of posts in series
            content_type: Type of content
        
        Returns:
            Complete content series
        """
        print(f"Creating {num_posts}-part content series on: {main_topic}")
        
        # Generate series outline
        series_outline = self.agent.create_blog_series(
            main_topic=main_topic,
            num_posts=num_posts
        )
        
        # Create each post
        series_content = []
        for i in range(num_posts):
            print(f"Creating post {i+1}/{num_posts}...")
            
            post_topic = f"{main_topic} - Part {i+1}"
            content = self.agent.run(
                topic=post_topic,
                content_type=content_type,
                optimize_seo=True
            )
            
            series_content.append({
                "post_number": i + 1,
                "topic": post_topic,
                "content": content
            })
        
        return {
            "main_topic": main_topic,
            "num_posts": num_posts,
            "series_outline": series_outline,
            "posts": series_content
        }
    
    def multi_format_content(
        self,
        topic: str,
        formats: List[str] = None
    ) -> Dict[str, Any]:
        """
        Create same topic in multiple formats.
        
        Args:
            topic: Content topic
            formats: List of formats (blog_post, article, social_post, etc.)
        
        Returns:
            Content in all requested formats
        """
        if formats is None:
            formats = ["blog_post", "article", "social_post"]
        
        print(f"Creating content in {len(formats)} formats...")
        
        content_versions = {}
        for format_type in formats:
            print(f"Creating {format_type}...")
            content = self.agent.run(
                topic=topic,
                content_type=format_type,
                optimize_seo=True
            )
            content_versions[format_type] = content
        
        return {
            "topic": topic,
            "formats": formats,
            "content_versions": content_versions
        }
    
    def content_update_workflow(
        self,
        existing_content: str,
        update_reason: str = "refresh"
    ) -> Dict[str, Any]:
        """
        Update existing content with new information.
        
        Args:
            existing_content: Current content
            update_reason: Why updating (refresh, new_info, seo)
        
        Returns:
            Updated content with changes
        """
        print("Updating existing content...")
        
        update_prompt = f"""Update this content:

Current Content: {existing_content[:500]}...

Update Reason: {update_reason}

Provide:
1. Updated content
2. Changes made
3. New information added
4. Removed outdated information
5. SEO improvements"""
        
        updated = self.agent.run(update_prompt)
        
        return {
            "original_content": existing_content,
            "update_reason": update_reason,
            "updated_content": updated,
            "changes_summary": self._summarize_changes(existing_content, updated)
        }
    
    def content_repurposing(
        self,
        source_content: str,
        target_platform: str
    ) -> Dict[str, Any]:
        """
        Repurpose content for different platform.
        
        Args:
            source_content: Original content
            target_platform: Target platform (linkedin, twitter, instagram, etc.)
        
        Returns:
            Repurposed content
        """
        print(f"Repurposing content for {target_platform}...")
        
        repurpose_prompt = f"""Repurpose this content for {target_platform}:

Original Content: {source_content[:300]}...

Adapt for {target_platform}:
1. Adjust length
2. Change tone/style
3. Add platform-specific elements
4. Optimize formatting
5. Include relevant hashtags/mentions"""
        
        repurposed = self.agent.run(repurpose_prompt)
        
        return {
            "source_content": source_content,
            "target_platform": target_platform,
            "repurposed_content": repurposed
        }
    
    def ab_testing_content(
        self,
        topic: str,
        test_element: str = "headline",
        num_variants: int = 2
    ) -> Dict[str, Any]:
        """
        Create A/B test variants for content.
        
        Args:
            topic: Content topic
            test_element: Element to test (headline, intro, cta)
            num_variants: Number of variants to create
        
        Returns:
            Multiple content variants
        """
        print(f"Creating {num_variants} A/B test variants...")
        
        variants = []
        for i in range(num_variants):
            print(f"Creating variant {i+1}...")
            
            variant_prompt = f"""Create content variant {i+1} for: {topic}

Test Element: {test_element}
Make this variant unique in {test_element}

Variant {i+1} should focus on: {self._get_variant_focus(i, test_element)}"""
            
            content = self.agent.run(variant_prompt)
            variants.append({
                "variant": chr(65 + i),  # A, B, C, etc.
                "focus": self._get_variant_focus(i, test_element),
                "content": content
            })
        
        return {
            "topic": topic,
            "test_element": test_element,
            "num_variants": num_variants,
            "variants": variants
        }
    
    def _research_keywords(self, topic: str) -> List[str]:
        """Research relevant keywords."""
        # Simulated - in production, use real keyword tool
        keywords = [topic.lower()]
        
        # Add variations
        words = topic.split()
        if len(words) > 1:
            keywords.extend([
                " ".join(words[:2]),
                f"{words[0]} tips",
                f"{words[0]} guide"
            ])
        
        return keywords[:5]
    
    def _create_outline(
        self,
        topic: str,
        content_type: str,
        target_audience: str
    ) -> str:
        """Create content outline."""
        outline_prompt = f"""Create outline for {content_type} on {topic}:

Target Audience: {target_audience}

Provide:
1. Introduction hook
2. Main points (3-5)
3. Supporting details for each
4. Conclusion/CTA
5. Estimated word count per section"""
        
        return self.agent.run(outline_prompt)
    
    def _optimize_seo(self, content: str, keywords: List[str]) -> str:
        """Optimize content for SEO."""
        # In production, use SEOOptimizerTool
        return content
    
    def _final_review(self, content: str, content_type: str) -> str:
        """Final content review and polish."""
        review_prompt = f"""Review and polish this {content_type}:

{content[:500]}...

Check:
1. Grammar and spelling
2. Flow and readability
3. Call-to-action strength
4. SEO optimization
5. Engagement level

Provide polished final version."""
        
        return self.agent.run(review_prompt)
    
    def _summarize_changes(self, original: str, updated: str) -> str:
        """Summarize changes between versions."""
        return "Content updated with new information and SEO improvements"
    
    def _get_variant_focus(self, variant_index: int, element: str) -> str:
        """Get focus for A/B test variant."""
        focuses = {
            "headline": ["curiosity-driven", "benefit-focused", "question-based"],
            "intro": ["story-led", "statistic-led", "problem-focused"],
            "cta": ["urgency", "value", "simplicity"]
        }
        
        element_focuses = focuses.get(element, ["standard"])
        return element_focuses[variant_index % len(element_focuses)]
    
    def get_content_library(self) -> List[Dict[str, Any]]:
        """Get all content created in this session."""
        return self.content_library


def create_content_workflow() -> ContentWorkflow:
    """Factory function to create a ContentWorkflow."""
    return ContentWorkflow()
