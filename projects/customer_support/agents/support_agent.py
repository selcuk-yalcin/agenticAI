"""
Customer Support Agent
Handles customer inquiries and support tickets with AI assistance.
"""

from typing import Dict, Any, List, Optional
from core.agents.base_agent import BaseAgent


class SupportAgent(BaseAgent):
    """Agent for handling customer support inquiries and tickets."""
    
    SYSTEM_PROMPT = """You are a professional customer support agent with expertise in:
- Providing helpful, empathetic responses
- Troubleshooting common issues
- Escalating complex problems appropriately
- Maintaining positive customer relationships

Always be polite, clear, and solution-focused. If you don't know the answer, be honest and offer to escalate."""

    def __init__(
        self,
        model: str = "gpt-4-turbo-preview",
        temperature: float = 0.3,
        enable_sentiment_analysis: bool = True
    ):
        super().__init__(
            name="SupportAgent",
            model=model,
            temperature=temperature,
            system_prompt=self.SYSTEM_PROMPT
        )
        self.enable_sentiment_analysis = enable_sentiment_analysis

    def run(
        self,
        query: str,
        category: str = "general",
        tone: str = "helpful",
        **kwargs
    ) -> str:
        """
        Process a customer support query.
        
        Args:
            query: Customer question or issue
            category: Type of support (technical, billing, product, troubleshooting)
            tone: Response tone (helpful, empathetic, patient, informative)
            **kwargs: Additional parameters
            
        Returns:
            Support response
        """
        # Build context-aware prompt
        prompt = f"""Customer Support Query:
{query}

Category: {category}
Required Tone: {tone}

Provide a clear, helpful response that:
1. Acknowledges the customer's concern
2. Provides a solution or next steps
3. Maintains a {tone} tone
4. Offers additional help if needed"""

        # Add category-specific guidance
        if category == "technical":
            prompt += "\n\nProvide step-by-step troubleshooting instructions."
        elif category == "billing":
            prompt += "\n\nBe empathetic and clear about billing policies."
        elif category == "product":
            prompt += "\n\nProvide detailed product information and benefits."
        elif category == "troubleshooting":
            if kwargs.get("include_steps"):
                prompt += "\n\nProvide numbered step-by-step instructions."
        
        # Use parent class's _execute_with_tools for LLM call
        response, _ = self._execute_with_tools(prompt)
        
        return response

    def handle_inquiry(
        self,
        customer_message: str,
        customer_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle a customer support inquiry."""
        
        # Build context
        prompt = f"Customer inquiry: {customer_message}\n\n"
        if customer_id:
            prompt += f"Customer ID: {customer_id}\n"
        if context:
            prompt += f"Context: {context}\n"
        
        prompt += "\nProvide a helpful, professional response."
        
        # Get response
        response = self.run(prompt)
        
        result = {
            "response": response,
            "customer_id": customer_id,
            "requires_escalation": self._check_escalation(customer_message)
        }
        
        if self.enable_sentiment_analysis:
            result["sentiment"] = self._analyze_sentiment(customer_message)
        
        return result

    def analyze_ticket(
        self,
        ticket_id: str,
        message: str,
        priority: str = "medium"
    ) -> Dict[str, Any]:
        """Analyze and categorize a support ticket."""
        
        prompt = f"""Analyze this support ticket:
        
Ticket ID: {ticket_id}
Priority: {priority}
Message: {message}

Provide:
1. Category (technical, billing, account, product, other)
2. Urgency level (low, medium, high, critical)
3. Suggested action
4. Estimated resolution time"""
        
        analysis = self.run(prompt)
        
        return {
            "ticket_id": ticket_id,
            "analysis": analysis,
            "priority": priority,
            "requires_escalation": self._check_escalation(message)
        }

    def search_knowledge_base(
        self,
        query: str,
        max_results: int = 5
    ) -> Dict[str, Any]:
        """Search knowledge base for relevant articles."""
        
        prompt = f"""Search knowledge base for: {query}

Based on common support topics, suggest relevant help articles and solutions.
Provide practical, actionable guidance."""
        
        results = self.run(prompt)
        
        return {
            "query": query,
            "results": results,
            "result_count": max_results
        }

    def generate_response_template(
        self,
        scenario: str,
        tone: str = "professional"
    ) -> str:
        """Generate a response template for common scenarios."""
        
        prompt = f"""Create a response template for: {scenario}
        
Tone: {tone}
Include placeholders for customization like [CUSTOMER_NAME], [ISSUE], [SOLUTION].
Keep it friendly yet professional."""
        
        template = self.run(prompt)
        return template

    def _check_escalation(self, message: str) -> bool:
        """Check if message requires escalation to human agent."""
        escalation_keywords = [
            "legal", "lawyer", "sue", "complaint", "manager",
            "unacceptable", "terrible", "worst", "refund immediately"
        ]
        return any(keyword in message.lower() for keyword in escalation_keywords)

    def _analyze_sentiment(self, message: str) -> str:
        """Simple sentiment analysis."""
        negative_words = ["angry", "frustrated", "disappointed", "terrible", "awful"]
        positive_words = ["happy", "great", "excellent", "thank", "love"]
        
        msg_lower = message.lower()
        neg_count = sum(1 for word in negative_words if word in msg_lower)
        pos_count = sum(1 for word in positive_words if word in msg_lower)
        
        if neg_count > pos_count:
            return "negative"
        elif pos_count > neg_count:
            return "positive"
        return "neutral"


def create_support_agent(**kwargs) -> SupportAgent:
    """Factory function to create a SupportAgent."""
    return SupportAgent(**kwargs)
