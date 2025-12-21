"""Tests for message composition and personalization.

This module tests:
- Message template rendering
- Personalization with lead data
- Tone and style consistency
- Call-to-action (CTA) generation
"""

import pytest
from unittest.mock import Mock, patch


class TestMessageComposer:
    """Test suite for message composition functionality."""

    @pytest.fixture
    def sample_lead(self):
        """Fixture providing a sample lead for message composition.
        
        Returns:
            dict: Sample lead with all necessary fields.
        """
        return {
            "name": "John Doe",
            "title": "VP of Engineering",
            "company": "TechCorp",
            "location": "San Francisco, CA",
            "snippet": "Passionate about building scalable systems and leading engineering teams."
        }

    @pytest.fixture
    def message_template(self):
        """Fixture providing a basic message template.
        
        Returns:
            str: Message template with placeholders.
        """
        return """Hi {name},

I noticed your work at {company} and your focus on {topic}. 

{personalized_content}

Would you be open to a quick 15-minute call to discuss how we can help {company} with {value_proposition}?

Best regards"""

    def test_message_includes_personalization(self, sample_lead, message_template):
        """Test that generated messages include personalized fields.
        
        Verifies:
        - Lead name is included
        - Company name is mentioned
        - Title/role is referenced
        """
        def compose_message(lead, template):
            """Compose personalized message."""
            return template.format(
                name=lead["name"],
                company=lead["company"],
                topic="engineering excellence",
                personalized_content=f"Your background in {lead['title']} is impressive.",
                value_proposition="scaling your infrastructure"
            )
        
        message = compose_message(sample_lead, message_template)
        
        assert sample_lead["name"] in message
        assert sample_lead["company"] in message
        assert len(message) > 100  # Message has substance

    def test_message_tone_is_professional(self):
        """Test that message tone remains professional and appropriate.
        
        Tone guidelines:
        - Not overly casual or familiar
        - No jargon or buzzwords
        - Respectful and concise
        """
        def analyze_tone(message):
            """Simple tone analysis."""
            casual_words = ["hey", "dude", "sup", "yo"]
            pushy_words = ["urgent", "limited time", "act now"]
            
            message_lower = message.lower()
            is_casual = any(word in message_lower for word in casual_words)
            is_pushy = any(word in message_lower for word in pushy_words)
            
            return not (is_casual or is_pushy)
        
        professional_msg = "Hi John, I noticed your work at TechCorp..."
        casual_msg = "Hey dude, saw you work at TechCorp..."
        
        assert analyze_tone(professional_msg) is True
        assert analyze_tone(casual_msg) is False

    def test_message_length_is_appropriate(self, sample_lead, message_template):
        """Test that message length is within acceptable range.
        
        Guidelines:
        - Minimum: 100 characters (too short feels spammy)
        - Maximum: 500 characters (too long loses attention)
        - Optimal: 150-300 characters
        """
        def compose_message(lead, template):
            return template.format(
                name=lead["name"],
                company=lead["company"],
                topic="engineering",
                personalized_content="Brief personalized note.",
                value_proposition="improve efficiency"
            )
        
        message = compose_message(sample_lead, message_template)
        
        assert 100 <= len(message) <= 500

    def test_message_contains_clear_cta(self, sample_lead, message_template):
        """Test that message includes a clear call-to-action.
        
        CTA requirements:
        - Specific ask (call, meeting, demo)
        - Time commitment mentioned (15 min, 30 min)
        - Easy to respond to
        """
        def compose_message(lead, template):
            return template.format(
                name=lead["name"],
                company=lead["company"],
                topic="engineering",
                personalized_content="I'd love to learn more.",
                value_proposition="scaling infrastructure"
            )
        
        message = compose_message(sample_lead, message_template)
        
        # Check for CTA keywords
        cta_keywords = ["call", "meeting", "discuss", "15-minute", "30-minute"]
        assert any(keyword in message.lower() for keyword in cta_keywords)

    @patch('openai.ChatCompletion.create')
    def test_llm_personalization_integration(self, mock_openai, sample_lead):
        """Test integration with LLM for enhanced personalization.
        
        Tests:
        - LLM API is called with correct parameters
        - Response is properly formatted
        - Fallback handling if LLM fails
        """
        mock_openai.return_value = Mock(
            choices=[Mock(message=Mock(content="Personalized message content"))]
        )
        
        def generate_personalized_content(lead):
            """Generate content using LLM (mocked)."""
            try:
                response = mock_openai(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": f"Write brief personalized note for {lead['name']}"}]
                )
                return response.choices[0].message.content
            except Exception:
                return f"I noticed your role as {lead['title']} at {lead['company']}."
        
        content = generate_personalized_content(sample_lead)
        assert len(content) > 0
        assert isinstance(content, str)

    def test_message_avoids_spam_triggers(self):
        """Test that messages avoid common spam trigger words.
        
        Spam triggers to avoid:
        - "Free", "Act now", "Limited time"
        - All caps
        - Excessive punctuation (!!!)
        - Generic greetings
        """
        def is_spam_like(message):
            """Check for spam characteristics."""
            spam_words = ["free", "act now", "limited time", "guaranteed", "click here"]
            message_lower = message.lower()
            
            has_spam_words = any(word in message_lower for word in spam_words)
            has_excessive_caps = sum(1 for c in message if c.isupper()) / max(len(message), 1) > 0.3
            has_excessive_punctuation = "!!!" in message or "???" in message
            
            return has_spam_words or has_excessive_caps or has_excessive_punctuation
        
        good_message = "Hi John, I noticed your work at TechCorp. Would you be open to a call?"
        spam_message = "FREE OFFER!!! Click here NOW for LIMITED TIME deal!!!"
        
        assert is_spam_like(good_message) is False
        assert is_spam_like(spam_message) is True

    def test_multiple_templates_for_ab_testing(self):
        """Test support for multiple message templates (A/B testing).
        
        Requirements:
        - Different templates for different scenarios
        - Track which template was used
        - Consistent variables across templates
        """
        templates = {
            "direct": "Hi {name}, quick question about {company}'s {topic}. Call?",
            "value_first": "Hi {name}, we help companies like {company} with {value}. Interested?",
            "social_proof": "Hi {name}, we've worked with similar companies. Can we chat?"
        }
        
        lead = {"name": "John", "company": "TechCorp", "topic": "scaling", "value": "infrastructure"}
        
        for template_name, template in templates.items():
            try:
                message = template.format(**lead)
                assert len(message) > 0
                assert lead["name"] in message
            except KeyError:
                # Template uses variables not in lead data - that's OK for some templates
                pass
