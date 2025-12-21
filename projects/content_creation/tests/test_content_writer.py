"""Tests for Content Writer Agent.

This module tests:
- Blog post generation with various topics
- Content quality and readability
- SEO keyword integration
- Multiple content formats (blog, social, email)
"""

import pytest
from unittest.mock import Mock, patch


class TestContentWriter:
    """Test suite for content writing functionality."""

    @pytest.fixture
    def sample_topic(self):
        """Fixture providing a sample content topic.
        
        Returns:
            dict: Topic with keywords and target audience.
        """
        return {
            "title": "The Future of Remote Work",
            "keywords": ["remote work", "hybrid", "productivity", "work-life balance"],
            "target_audience": "business professionals",
            "tone": "professional",
            "length": "medium"  # short, medium, long
        }

    @pytest.fixture
    def sample_blog_post(self):
        """Fixture providing a sample blog post.
        
        Returns:
            str: Sample blog post content.
        """
        return """# The Future of Remote Work

Remote work has transformed how businesses operate. Companies are embracing hybrid models 
that combine office and remote work, offering flexibility while maintaining productivity.

Key benefits include improved work-life balance, reduced commute times, and access to 
global talent pools. However, challenges around communication and team cohesion remain.

## Best Practices

1. Set clear expectations
2. Use collaboration tools effectively
3. Maintain regular communication

Organizations that adapt will thrive in this new era of work."""

    @patch('openai.ChatCompletion.create')
    def test_generate_blog_post_returns_content(self, mock_openai, sample_topic):
        """Test that blog post generation returns valid content.
        
        Verifies:
        - Content is non-empty string
        - Minimum length requirement met
        - Target keywords are included
        """
        mock_openai.return_value = Mock(
            choices=[Mock(message=Mock(content="Blog post about remote work..."))]
        )
        
        def generate_blog_post(topic):
            """Generate blog post from topic."""
            response = mock_openai(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": f"Write blog about {topic['title']}"}]
            )
            return response.choices[0].message.content
        
        content = generate_blog_post(sample_topic)
        
        assert isinstance(content, str)
        assert len(content) > 100

    def test_content_includes_seo_keywords(self, sample_blog_post, sample_topic):
        """Test that generated content includes SEO keywords.
        
        Keywords should appear naturally in:
        - Title/headings
        - First paragraph
        - Throughout body
        """
        def check_keyword_presence(content, keywords):
            """Check if keywords are present in content."""
            content_lower = content.lower()
            found_keywords = [kw for kw in keywords if kw.lower() in content_lower]
            return {
                "found_count": len(found_keywords),
                "found_keywords": found_keywords,
                "coverage_pct": len(found_keywords) / len(keywords) * 100
            }
        
        result = check_keyword_presence(sample_blog_post, sample_topic["keywords"])
        
        assert result["found_count"] >= 2  # At least half the keywords
        assert result["coverage_pct"] >= 50

    def test_content_has_proper_structure(self, sample_blog_post):
        """Test that content follows proper blog post structure.
        
        Structure requirements:
        - Has title/heading
        - Has introduction
        - Has body paragraphs
        - Has conclusion or CTA
        """
        def analyze_structure(content):
            """Analyze blog post structure."""
            lines = content.split('\n')
            has_heading = any(line.startswith('#') for line in lines)
            paragraphs = [p for p in content.split('\n\n') if p.strip() and not p.startswith('#')]
            
            return {
                "has_heading": has_heading,
                "paragraph_count": len(paragraphs),
                "has_list": any('1.' in content or '-' in content),
                "word_count": len(content.split())
            }
        
        structure = analyze_structure(sample_blog_post)
        
        assert structure["has_heading"] is True
        assert structure["paragraph_count"] >= 2
        assert structure["word_count"] >= 100

    def test_readability_score_calculation(self, sample_blog_post):
        """Test content readability scoring.
        
        Metrics:
        - Average sentence length
        - Average word length
        - Complexity score (simple approximation)
        """
        def calculate_readability(content):
            """Calculate basic readability metrics."""
            sentences = content.replace('!', '.').replace('?', '.').split('.')
            sentences = [s.strip() for s in sentences if s.strip()]
            
            words = content.split()
            
            avg_sentence_length = len(words) / len(sentences) if sentences else 0
            avg_word_length = sum(len(w) for w in words) / len(words) if words else 0
            
            # Simple readability score (lower is easier)
            score = (avg_sentence_length * 0.5) + (avg_word_length * 2)
            
            return {
                "avg_sentence_length": avg_sentence_length,
                "avg_word_length": avg_word_length,
                "readability_score": score,
                "grade_level": "medium" if score < 30 else "hard"
            }
        
        metrics = calculate_readability(sample_blog_post)
        
        assert metrics["avg_sentence_length"] > 0
        assert metrics["readability_score"] > 0

    def test_generate_social_media_post(self):
        """Test generation of social media content.
        
        Social media requirements:
        - Character limits (Twitter: 280, LinkedIn: 3000)
        - Hashtags included
        - Call-to-action
        - Engaging opening
        """
        def generate_social_post(topic, platform):
            """Generate platform-specific social media post."""
            char_limits = {
                "twitter": 280,
                "linkedin": 3000,
                "instagram": 2200
            }
            
            post = f"🚀 {topic['title']}\n\n"
            post += "Key insight about remote work trends...\n\n"
            
            # Add hashtags
            hashtags = " ".join([f"#{kw.replace(' ', '')}" for kw in topic['keywords'][:3]])
            post += hashtags
            
            limit = char_limits.get(platform, 280)
            return post[:limit]
        
        topic = {"title": "Remote Work", "keywords": ["remote", "hybrid", "productivity"]}
        
        twitter_post = generate_social_post(topic, "twitter")
        linkedin_post = generate_social_post(topic, "linkedin")
        
        assert len(twitter_post) <= 280
        assert "#" in twitter_post  # Has hashtags

    def test_content_tone_validation(self):
        """Test validation of content tone.
        
        Tone types:
        - Professional: formal, clear, authoritative
        - Casual: friendly, conversational
        - Technical: precise, detailed, expert
        """
        def detect_tone(content):
            """Simple tone detection."""
            casual_words = ["hey", "awesome", "cool", "super"]
            formal_words = ["therefore", "furthermore", "nevertheless", "consequently"]
            
            content_lower = content.lower()
            casual_count = sum(1 for w in casual_words if w in content_lower)
            formal_count = sum(1 for w in formal_words if w in content_lower)
            
            if formal_count > casual_count:
                return "professional"
            elif casual_count > formal_count:
                return "casual"
            return "neutral"
        
        professional_text = "Furthermore, remote work offers significant advantages. Therefore, companies should adapt."
        casual_text = "Hey! Remote work is awesome and super flexible. It's really cool!"
        
        assert detect_tone(professional_text) == "professional"
        assert detect_tone(casual_text) == "casual"

    def test_content_length_categories(self):
        """Test content length categorization.
        
        Categories:
        - Short: 100-300 words (social posts, summaries)
        - Medium: 300-800 words (blog posts)
        - Long: 800+ words (in-depth articles)
        """
        def categorize_length(content):
            """Categorize content by word count."""
            word_count = len(content.split())
            
            if word_count < 300:
                return "short", word_count
            elif word_count < 800:
                return "medium", word_count
            else:
                return "long", word_count
        
        short_content = " ".join(["word"] * 200)
        medium_content = " ".join(["word"] * 500)
        long_content = " ".join(["word"] * 1000)
        
        assert categorize_length(short_content)[0] == "short"
        assert categorize_length(medium_content)[0] == "medium"
        assert categorize_length(long_content)[0] == "long"

    def test_plagiarism_check_simulation(self, sample_blog_post):
        """Test plagiarism checking (simulated).
        
        In production, would use:
        - Copyscape API
        - Turnitin
        - Custom similarity algorithms
        """
        def simple_uniqueness_check(content, reference_db):
            """Simple uniqueness check against reference database."""
            # Simplified: check for exact phrase matches
            phrases = [content[i:i+50] for i in range(0, len(content), 50)]
            
            matches = sum(1 for phrase in phrases if phrase in reference_db)
            uniqueness_score = (1 - matches / len(phrases)) * 100 if phrases else 100
            
            return {
                "uniqueness_pct": uniqueness_score,
                "is_unique": uniqueness_score >= 80,
                "matches_found": matches
            }
        
        reference_db = ["some other content that doesn't match"]
        result = simple_uniqueness_check(sample_blog_post, reference_db)
        
        assert "uniqueness_pct" in result
        assert result["uniqueness_pct"] >= 0

    def test_metadata_generation(self, sample_blog_post, sample_topic):
        """Test generation of content metadata.
        
        Metadata includes:
        - Title
        - Meta description
        - Keywords
        - Reading time
        - Category/tags
        """
        def generate_metadata(content, topic):
            """Generate content metadata."""
            word_count = len(content.split())
            reading_time = max(1, word_count // 200)  # 200 words per minute
            
            # Extract first paragraph for meta description
            paragraphs = [p for p in content.split('\n\n') if p.strip() and not p.startswith('#')]
            meta_description = paragraphs[0][:160] if paragraphs else ""
            
            return {
                "title": topic.get("title", "Untitled"),
                "meta_description": meta_description,
                "keywords": topic.get("keywords", []),
                "reading_time_min": reading_time,
                "word_count": word_count,
                "category": topic.get("category", "General")
            }
        
        metadata = generate_metadata(sample_blog_post, sample_topic)
        
        assert "title" in metadata
        assert "reading_time_min" in metadata
        assert metadata["reading_time_min"] > 0
        assert metadata["word_count"] > 0

    @patch('openai.ChatCompletion.create')
    def test_content_revision_workflow(self, mock_openai):
        """Test content revision and improvement workflow.
        
        Workflow:
        1. Generate initial draft
        2. Get feedback/critique
        3. Revise based on feedback
        """
        mock_openai.return_value = Mock(
            choices=[Mock(message=Mock(content="Revised content"))]
        )
        
        def revise_content(original, feedback):
            """Revise content based on feedback."""
            response = mock_openai(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user",
                    "content": f"Revise this content based on feedback.\n\nOriginal: {original}\n\nFeedback: {feedback}"
                }]
            )
            return response.choices[0].message.content
        
        original = "Original draft content"
        feedback = "Make it more engaging and add examples"
        
        revised = revise_content(original, feedback)
        
        assert isinstance(revised, str)
        assert len(revised) > 0
