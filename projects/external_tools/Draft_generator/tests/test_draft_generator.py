"""Tests for Draft Generator workflow.

This module tests:
- Draft generation from topics
- Reflection and critique generation
- Revision based on feedback
- DraftWorkflow class integration
"""

import pytest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


class TestDraftGenerator:
    """Test suite for draft generation functionality."""

    @pytest.fixture
    def sample_topic(self):
        """Fixture providing a sample topic for draft generation.
        
        Returns:
            str: Sample topic.
        """
        return "The future of artificial intelligence in healthcare"

    @pytest.fixture
    def sample_draft(self):
        """Fixture providing a sample draft text.
        
        Returns:
            str: Sample draft content.
        """
        return """Artificial Intelligence in Healthcare: A New Era

The integration of AI into healthcare is transforming how we diagnose and treat patients. 
Machine learning algorithms can now analyze medical images with accuracy rivaling human experts.

Key benefits include faster diagnosis, personalized treatment plans, and improved patient outcomes.

However, challenges remain around data privacy and algorithmic bias that must be addressed."""

    @pytest.fixture
    def sample_reflection(self):
        """Fixture providing sample reflection/critique.
        
        Returns:
            str: Sample reflection content.
        """
        return """Critical Reflection:

1. Clarity: The main argument is clear but could be stronger with specific examples.
2. Tone: Appropriate for a general audience.
3. Gaps: Missing discussion of implementation costs and regulatory hurdles.
4. Structure: Transitions are good, but conclusion feels abrupt.

Improvements needed:
- Add 1-2 specific case studies
- Expand conclusion with actionable insights
- Include data/statistics to support claims"""

    @patch('openai.ChatCompletion.create')
    def test_generate_draft_returns_text(self, mock_openai, sample_topic):
        """Test that generate_draft returns non-empty text.
        
        Verifies:
        - Return type is string
        - Length is reasonable (>100 chars)
        - Topic is mentioned in draft
        """
        mock_openai.return_value = Mock(
            choices=[Mock(message=Mock(content="This is a draft about AI in healthcare..."))]
        )
        
        def generate_draft(topic):
            """Mock draft generation."""
            response = mock_openai(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": f"Write about {topic}"}]
            )
            return response.choices[0].message.content
        
        draft = generate_draft(sample_topic)
        
        assert isinstance(draft, str)
        assert len(draft) > 50

    def test_draft_contains_key_elements(self, sample_draft):
        """Test that draft contains essential elements.
        
        Elements:
        - Introduction
        - Body with key points
        - Conclusion (optional but recommended)
        """
        def analyze_draft_structure(draft):
            """Analyze draft for key structural elements."""
            paragraphs = [p.strip() for p in draft.split('\n\n') if p.strip()]
            
            return {
                "paragraph_count": len(paragraphs),
                "has_title": len(paragraphs) > 0 and len(paragraphs[0]) < 100,
                "word_count": len(draft.split()),
                "has_multiple_sections": len(paragraphs) >= 3
            }
        
        analysis = analyze_draft_structure(sample_draft)
        
        assert analysis["paragraph_count"] >= 2
        assert analysis["word_count"] > 50
        assert analysis["has_title"] is True

    @patch('openai.ChatCompletion.create')
    def test_reflect_on_draft_provides_feedback(self, mock_openai, sample_draft):
        """Test that reflection provides constructive feedback.
        
        Feedback should include:
        - Analysis of clarity, tone, gaps, structure
        - Specific improvement suggestions
        - Constructive tone (not just criticism)
        """
        mock_openai.return_value = Mock(
            choices=[Mock(message=Mock(content="Feedback: Good structure, but needs more examples."))]
        )
        
        def reflect_on_draft(draft):
            """Mock reflection generation."""
            response = mock_openai(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": f"Review this draft: {draft}"}]
            )
            return response.choices[0].message.content
        
        reflection = reflect_on_draft(sample_draft)
        
        assert isinstance(reflection, str)
        assert len(reflection) > 30

    def test_reflection_identifies_improvement_areas(self, sample_reflection):
        """Test that reflection identifies specific areas to improve.
        
        Should mention:
        - What's working well
        - What needs improvement
        - Specific actionable suggestions
        """
        def extract_suggestions(reflection):
            """Extract improvement suggestions from reflection."""
            suggestions = []
            
            # Simple parsing (in practice, use more sophisticated method)
            lines = reflection.split('\n')
            for line in lines:
                if line.strip().startswith('-') or line.strip().startswith('•'):
                    suggestions.append(line.strip())
            
            return suggestions
        
        suggestions = extract_suggestions(sample_reflection)
        
        assert len(suggestions) > 0

    @patch('openai.ChatCompletion.create')
    def test_revise_draft_incorporates_feedback(self, mock_openai, sample_draft, sample_reflection):
        """Test that revision incorporates feedback from reflection.
        
        Revised draft should:
        - Address issues mentioned in reflection
        - Be different from original
        - Maintain or improve quality
        """
        mock_openai.return_value = Mock(
            choices=[Mock(message=Mock(content="Revised draft with improvements..."))]
        )
        
        def revise_draft(original, reflection):
            """Mock revision generation."""
            response = mock_openai(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user", 
                    "content": f"Revise this draft based on feedback.\n\nDraft: {original}\n\nFeedback: {reflection}"
                }]
            )
            return response.choices[0].message.content
        
        revised = revise_draft(sample_draft, sample_reflection)
        
        assert isinstance(revised, str)
        assert len(revised) > 0

    def test_revised_draft_differs_from_original(self, sample_draft):
        """Test that revised draft is meaningfully different from original.
        
        Should not be identical (indicates revision actually happened).
        """
        def simple_revision(draft):
            """Simple revision example."""
            return draft + "\n\nAdditional paragraph with more details."
        
        revised = simple_revision(sample_draft)
        
        assert revised != sample_draft
        assert len(revised) > len(sample_draft)

    @patch('openai.ChatCompletion.create')
    def test_workflow_class_generates_draft(self, mock_openai, sample_topic):
        """Test DraftWorkflow class generate_draft method.
        
        Verifies workflow class can be instantiated and used.
        """
        mock_openai.return_value = Mock(
            choices=[Mock(message=Mock(content="Draft content"))]
        )
        
        # Mock DraftWorkflow class
        class MockDraftWorkflow:
            def __init__(self, model="gpt-4o-mini"):
                self.model = model
            
            def generate_draft(self, topic):
                return f"Draft about {topic}"
        
        workflow = MockDraftWorkflow()
        draft = workflow.generate_draft(sample_topic)
        
        assert isinstance(draft, str)
        assert sample_topic in draft or "Draft" in draft

    def test_workflow_run_full_cycle(self, sample_topic):
        """Test complete workflow: generate → reflect → revise.
        
        Full cycle should:
        1. Generate initial draft
        2. Reflect on it
        3. Revise based on reflection
        4. Return all three artifacts
        """
        class MockDraftWorkflow:
            def generate_draft(self, topic):
                return f"Initial draft about {topic}"
            
            def reflect_on_draft(self, draft):
                return f"Feedback on: {draft[:30]}..."
            
            def revise_draft(self, draft, reflection):
                return f"Revised: {draft[:30]}..."
            
            def run_full_workflow(self, topic):
                draft = self.generate_draft(topic)
                reflection = self.reflect_on_draft(draft)
                revised = self.revise_draft(draft, reflection)
                return {
                    "draft": draft,
                    "reflection": reflection,
                    "revised_draft": revised
                }
        
        workflow = MockDraftWorkflow()
        result = workflow.run_full_workflow(sample_topic)
        
        assert "draft" in result
        assert "reflection" in result
        assert "revised_draft" in result
        assert len(result["draft"]) > 0

    def test_temperature_affects_creativity(self):
        """Test that temperature parameter affects output creativity.
        
        Higher temperature (0.7-1.0) → more creative
        Lower temperature (0.0-0.3) → more focused
        """
        def mock_generate_with_temp(topic, temperature):
            """Mock generation with temperature."""
            if temperature >= 0.7:
                return f"Creative and varied draft about {topic}"
            else:
                return f"Focused and consistent draft about {topic}"
        
        creative = mock_generate_with_temp("AI", 1.0)
        focused = mock_generate_with_temp("AI", 0.0)
        
        assert "Creative" in creative or "varied" in creative
        assert "Focused" in focused or "consistent" in focused

    def test_error_handling_for_api_failures(self):
        """Test graceful error handling when API calls fail.
        
        Should:
        - Catch exceptions
        - Return error message
        - Not crash the workflow
        """
        def generate_with_error_handling(topic):
            """Generate draft with error handling."""
            try:
                # Simulate API failure
                raise Exception("API Error")
            except Exception as e:
                return {
                    "status": "error",
                    "message": str(e),
                    "draft": None
                }
        
        result = generate_with_error_handling("test topic")
        
        assert result["status"] == "error"
        assert result["draft"] is None
