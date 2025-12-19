"""
Email Automation Agent
Automates email composition, personalization, and campaign management.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from core.agents.base_agent import BaseAgent


class EmailAgent(BaseAgent):
    """Agent for automated email creation and management."""
    
    SYSTEM_PROMPT = """You are an expert email marketing specialist with expertise in:
- Compelling subject lines and copy
- Email personalization
- Marketing automation
- Conversion optimization
- Email best practices

Create emails that are engaging, clear, and drive action. Follow email marketing best practices."""

    def __init__(
        self,
        model: str = "gpt-4-turbo-preview",
        temperature: float = 0.7,
        enable_personalization: bool = True
    ):
        super().__init__(
            name="EmailAgent",
            model=model,
            temperature=temperature,
            system_prompt=self.SYSTEM_PROMPT
        )
        self.enable_personalization = enable_personalization

    def run(self, prompt: str) -> str:
        """
        Run the email agent with a prompt.
        
        Args:
            prompt: The prompt for email generation
            
        Returns:
            Generated email content
        """
        response, _ = self._execute_with_tools(prompt)
        return response

    def compose_email(
        self,
        email_type: str = "marketing",
        subject_style: str = "engaging",
        tone: str = "professional",
        purpose: Optional[str] = None
    ) -> Dict[str, Any]:
        """Compose an email."""
        
        prompt = f"""Create a {email_type} email:

Type: {email_type}
Subject Style: {subject_style}
Tone: {tone}
Purpose: {purpose if purpose else "General communication"}

Provide:
1. Subject line (attention-grabbing)
2. Preview text
3. Email body (well-structured)
4. Call-to-action
5. Closing

Format for professional email delivery."""
        
        email_content = self.run(prompt)
        
        return {
            "type": email_type,
            "content": email_content,
            "metadata": {
                "tone": tone,
                "purpose": purpose,
                "created_at": datetime.now().isoformat()
            }
        }

    def compose_personalized_email(
        self,
        recipient_name: str,
        recipient_segment: Optional[str] = None,
        occasion: Optional[str] = None,
        include_recommendations: bool = False
    ) -> Dict[str, Any]:
        """Create personalized email for recipient."""
        
        if not self.enable_personalization:
            return self.compose_email()
        
        prompt = f"""Create a personalized email:

Recipient: {recipient_name}
Segment: {recipient_segment if recipient_segment else "General"}
Occasion: {occasion if occasion else "General communication"}
Include product recommendations: {include_recommendations}

Personalize based on:
- Recipient name and segment
- Past interactions (implied)
- Relevant content for their interests
- Timing and occasion

Make it feel personal, not automated."""
        
        email_content = self.run(prompt)
        
        return {
            "recipient": recipient_name,
            "content": email_content,
            "personalized": True,
            "segment": recipient_segment
        }

    def create_email_sequence(
        self,
        campaign_type: str,
        num_emails: int = 3,
        interval_days: int = 3
    ) -> Dict[str, Any]:
        """Create an email sequence/drip campaign."""
        
        prompt = f"""Create a {num_emails}-email sequence for {campaign_type}:

Campaign Type: {campaign_type}
Number of Emails: {num_emails}
Interval: Every {interval_days} days

For each email provide:
1. Email number and timing
2. Subject line
3. Key message/theme
4. Main content outline
5. Call-to-action
6. How it builds on previous emails

Ensure the sequence tells a cohesive story."""
        
        sequence = self.run(prompt)
        
        return {
            "campaign_type": campaign_type,
            "num_emails": num_emails,
            "interval_days": interval_days,
            "sequence": sequence
        }

    def generate_ab_variants(
        self,
        base_email: str,
        test_element: str = "subject_line",
        num_variants: int = 2
    ) -> Dict[str, Any]:
        """Generate A/B test variants of email elements."""
        
        prompt = f"""Create {num_variants} A/B test variants for: {test_element}

Base email: {base_email}

Test element: {test_element}
Variants needed: {num_variants}

For each variant:
1. The modified element
2. Hypothesis/reasoning
3. Expected impact
4. Target metric

Keep other elements consistent."""
        
        variants = self.run(prompt)
        
        return {
            "test_element": test_element,
            "num_variants": num_variants,
            "variants": variants
        }

    def optimize_subject_line(
        self,
        subject: str,
        goal: str = "higher_open_rate"
    ) -> Dict[str, Any]:
        """Optimize email subject line."""
        
        prompt = f"""Optimize this subject line:

Current: {subject}
Goal: {goal}

Provide:
1. Analysis of current subject
2. 3 improved alternatives
3. Why each would perform better
4. Best practices applied

Focus on {goal}."""
        
        optimization = self.run(prompt)
        
        return {
            "original": subject,
            "optimization": optimization,
            "goal": goal
        }

    def create_transactional_email(
        self,
        transaction_type: str,
        order_details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create transactional email (order confirmation, shipping, etc)."""
        
        prompt = f"""Create transactional email for: {transaction_type}

Type: {transaction_type}
Details: {order_details if order_details else "Standard transaction"}

Include:
1. Clear subject line
2. Transaction confirmation
3. Key details (order #, items, amount)
4. Next steps
5. Support information

Keep it clear, factual, and helpful."""
        
        email = self.run(prompt)
        
        return {
            "type": transaction_type,
            "content": email,
            "transactional": True
        }

    def generate_newsletter(
        self,
        topics: List[str],
        tone: str = "informative",
        include_sections: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Generate newsletter content."""
        
        if include_sections is None:
            include_sections = ["intro", "main_content", "updates", "cta"]
        
        prompt = f"""Create newsletter:

Topics: {', '.join(topics)}
Tone: {tone}
Sections: {', '.join(include_sections)}

Structure:
1. Engaging introduction
2. Main content for each topic
3. Company updates
4. Call-to-action
5. Footer content

Make it scannable with clear headers."""
        
        newsletter = self.run(prompt)
        
        return {
            "topics": topics,
            "content": newsletter,
            "sections": include_sections
        }


def create_email_agent(**kwargs) -> EmailAgent:
    """Factory function to create an EmailAgent."""
    return EmailAgent(**kwargs)
