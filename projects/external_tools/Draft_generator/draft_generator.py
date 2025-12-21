"""Draft Generator - LLM-based text draft generation, reflection, and revision

Usage:
    # Generate a draft only
    python draft_generator.py "Write a blog post about AI safety"

    # Generate, reflect, and revise
    python draft_generator.py "Write a blog post about AI safety" --revise

This script uses the OpenAI client configured from the .env file in the Agentic-AI root.

Features:
- DraftWorkflow class that chains: generate -> reflect -> revise
- Individual functions also available for custom workflows
"""

from __future__ import annotations
import sys
import os
from pathlib import Path

# Add parent directories to path to import core utils
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv(REPO_ROOT / ".env")

# Initialize OpenAI client
CLIENT = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class DraftWorkflow:
    """A workflow class that chains draft generation, reflection, and revision."""

    def __init__(self, model: str = "gpt-4o-mini"):
        """Initialize the workflow with a default model.
        
        Args:
            model: The OpenAI model to use for all operations.
        """
        self.model = model
        self.client = CLIENT

    def generate_draft(self, topic: str) -> str:
        """Generate a draft text on the given topic using an LLM.

        Args:
            topic: The subject or prompt for the draft.

        Returns:
            The generated draft text.
        """
        prompt = f"""You are a professional writer. Write a clear, well-structured draft on the following topic:

Topic: {topic}

Provide a concise, informative draft with an introduction, key points, and a conclusion.
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=1.0,
        )
        return response.choices[0].message.content

    def reflect_on_draft(self, draft: str) -> str:
        """Reflect on and critique a draft to provide improvement suggestions.

        Args:
            draft: The draft text to review.

        Returns:
            Critical reflection and improvement suggestions.
        """
        prompt = f"""You are a professional editor. Review the following blog post draft for quality, accuracy, and engagement.

Draft to review:
---
{draft}
---

Please provide a critical reflection based on these criteria:
1. Clarity: Is the main argument easy to follow?
2. Tone: Is it appropriate for the target audience?
3. Gaps: Is there any crucial information missing?
4. Structure: Do the transitions between sections feel natural?

Be harsh but constructive. List specific improvements that would make this a 10/10 piece.
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=1.0,
        )
        return response.choices[0].message.content

    def revise_draft(self, original_draft: str, reflection: str) -> str:
        """Revise the draft based on reflection feedback.

        Args:
            original_draft: The original draft text.
            reflection: The reflection/critique feedback.

        Returns:
            The revised draft incorporating the feedback.
        """
        ### START CODE HERE ###

        # Define your prompt here. A multi-line f-string is typically used for this.
        prompt = f"""You are a professional writer tasked with revising a draft based on editorial feedback.

Original Draft:
---
{original_draft}
---

Editorial Feedback:
---
{reflection}
---

Please rewrite the draft incorporating all the feedback. Maintain the original intent but improve clarity, tone, structure, and completeness. Make this a polished, publication-ready piece.
"""

        # Get a response from the LLM by creating a chat with the client.
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,  # Lower temperature for more focused revision
        )

        ### END CODE HERE ###

        return response.choices[0].message.content

    def run_full_workflow(self, topic: str) -> dict:
        """Run the complete workflow: generate -> reflect -> revise.

        Args:
            topic: The topic to write about.

        Returns:
            Dictionary containing draft, reflection, and revised_draft.
        """
        print("Step 1/3: Generating initial draft...")
        draft = self.generate_draft(topic)
        
        print("Step 2/3: Reflecting on draft...")
        reflection = self.reflect_on_draft(draft)
        
        print("Step 3/3: Revising draft based on feedback...")
        revised_draft = self.revise_draft(draft, reflection)
        
        return {
            "draft": draft,
            "reflection": reflection,
            "revised_draft": revised_draft
        }


# Standalone functions for backward compatibility
def generate_draft(topic: str, model: str = "gpt-4o-mini") -> str:
    """Generate a draft text on the given topic using an LLM.

    Args:
        topic: The subject or prompt for the draft.
        model: The OpenAI model to use (default: gpt-4o-mini for cost efficiency).

    Returns:
        The generated draft text.
    """
    workflow = DraftWorkflow(model=model)
    return workflow.generate_draft(topic)


def reflect_on_draft(draft: str, model: str = "gpt-4o-mini") -> str:
    """Reflect on and critique a draft to provide improvement suggestions.

    Args:
        draft: The draft text to review.
        model: The OpenAI model to use (default: gpt-4o-mini).

    Returns:
        Critical reflection and improvement suggestions.
    """
    workflow = DraftWorkflow(model=model)
    return workflow.reflect_on_draft(draft)


def revise_draft(original_draft: str, reflection: str, model: str = "gpt-4o-mini") -> str:
    """Revise the draft based on reflection feedback.

    Args:
        original_draft: The original draft text.
        reflection: The reflection/critique feedback.
        model: The OpenAI model to use (default: gpt-4o-mini).

    Returns:
        The revised draft incorporating the feedback.
    """
    workflow = DraftWorkflow(model=model)
    return workflow.revise_draft(original_draft, reflection)


def main():
    """Demo runner: generate a draft and optionally run reflection/revision workflow."""
    if len(sys.argv) < 2:
        print("Usage: python draft_generator.py \"Your topic here\" [--reflect | --revise]")
        print("\nOptions:")
        print("  (no flag)   : Generate draft only")
        print("  --reflect   : Generate draft + reflection")
        print("  --revise    : Full workflow (generate + reflect + revise)")
        sys.exit(1)

    topic = sys.argv[1]
    use_reflection = "--reflect" in sys.argv
    use_revision = "--revise" in sys.argv

    workflow = DraftWorkflow()

    if use_revision:
        # Run full workflow
        print(f"Running full workflow for topic: {topic}\n")
        results = workflow.run_full_workflow(topic)
        
        print("\n" + "=" * 60)
        print("ORIGINAL DRAFT:")
        print("=" * 60)
        print(results["draft"])
        
        print("\n" + "=" * 60)
        print("REFLECTION:")
        print("=" * 60)
        print(results["reflection"])
        
        print("\n" + "=" * 60)
        print("REVISED DRAFT:")
        print("=" * 60)
        print(results["revised_draft"])
        print("=" * 60)
        
    elif use_reflection:
        # Generate and reflect only
        print(f"Generating draft for topic: {topic}\n")
        draft = workflow.generate_draft(topic)
        
        print("=" * 60)
        print("DRAFT:")
        print("=" * 60)
        print(draft)
        print("=" * 60)
        
        print("\nReflecting on draft...\n")
        reflection = workflow.reflect_on_draft(draft)
        
        print("=" * 60)
        print("REFLECTION:")
        print("=" * 60)
        print(reflection)
        print("=" * 60)
        
    else:
        # Generate only
        print(f"Generating draft for topic: {topic}\n")
        draft = workflow.generate_draft(topic)
        
        print("=" * 60)
        print("DRAFT:")
        print("=" * 60)
        print(draft)
        print("=" * 60)


if __name__ == "__main__":
    main()
