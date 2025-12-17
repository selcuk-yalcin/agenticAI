"""
Customer Support Workflow
Multi-step support ticket handling and resolution
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from ..agents.support_agent import SupportAgent


class SupportWorkflow:
    """Orchestrates customer support ticket lifecycle."""
    
    def __init__(self):
        self.agent = SupportAgent()
        self.ticket_history = []
    
    def full_ticket_lifecycle(
        self,
        ticket_id: str,
        customer_message: str,
        customer_id: str,
        priority: str = "medium"
    ) -> Dict[str, Any]:
        """
        Complete ticket handling from intake to resolution.
        
        Steps:
        1. Ticket intake and categorization
        2. Sentiment analysis
        3. Knowledge base search
        4. Response generation
        5. Escalation check
        6. Follow-up scheduling
        
        Args:
            ticket_id: Ticket identifier
            customer_message: Customer's inquiry
            customer_id: Customer identifier
            priority: Ticket priority
        
        Returns:
            Complete ticket handling result
        """
        print(f"Processing ticket {ticket_id}...")
        
        # Step 1: Categorize ticket
        print("Step 1: Analyzing ticket...")
        analysis = self.agent.analyze_ticket(
            ticket_id=ticket_id,
            message=customer_message,
            priority=priority
        )
        
        # Step 2: Search knowledge base
        print("Step 2: Searching knowledge base...")
        kb_results = self.agent.search_knowledge_base(
            query=customer_message
        )
        
        # Step 3: Generate response
        print("Step 3: Generating response...")
        response = self.agent.handle_inquiry(
            customer_message=customer_message,
            customer_id=customer_id,
            context={
                "ticket_id": ticket_id,
                "analysis": analysis,
                "kb_results": kb_results
            }
        )
        
        # Step 4: Check for escalation
        requires_escalation = response.get("requires_escalation", False)
        
        # Step 5: Create follow-up plan
        follow_up = self._create_follow_up_plan(
            ticket_id=ticket_id,
            resolved=not requires_escalation
        )
        
        result = {
            "ticket_id": ticket_id,
            "customer_id": customer_id,
            "priority": priority,
            "analysis": analysis,
            "kb_results": kb_results,
            "response": response,
            "requires_escalation": requires_escalation,
            "follow_up": follow_up,
            "timestamp": datetime.now().isoformat()
        }
        
        self.ticket_history.append(result)
        return result
    
    def batch_ticket_processing(
        self,
        tickets: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Process multiple tickets in batch.
        
        Args:
            tickets: List of ticket dictionaries
        
        Returns:
            Batch processing results
        """
        print(f"Processing {len(tickets)} tickets in batch...")
        
        results = []
        escalations = []
        
        for ticket in tickets:
            print(f"Processing ticket {ticket.get('ticket_id')}...")
            
            result = self.full_ticket_lifecycle(
                ticket_id=ticket["ticket_id"],
                customer_message=ticket["message"],
                customer_id=ticket["customer_id"],
                priority=ticket.get("priority", "medium")
            )
            
            results.append(result)
            
            if result["requires_escalation"]:
                escalations.append(result)
        
        return {
            "total_tickets": len(tickets),
            "processed": len(results),
            "escalations": len(escalations),
            "results": results,
            "escalated_tickets": escalations,
            "summary": self._generate_batch_summary(results)
        }
    
    def priority_routing(
        self,
        tickets: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Route tickets by priority and category.
        
        Args:
            tickets: List of tickets to route
        
        Returns:
            Routed tickets by priority and category
        """
        print("Routing tickets by priority...")
        
        routed = {
            "critical": [],
            "high": [],
            "medium": [],
            "low": []
        }
        
        categories = {}
        
        for ticket in tickets:
            # Analyze ticket
            analysis = self.agent.analyze_ticket(
                ticket_id=ticket["ticket_id"],
                message=ticket["message"],
                priority=ticket.get("priority", "medium")
            )
            
            priority = ticket.get("priority", "medium")
            routed[priority].append({
                "ticket": ticket,
                "analysis": analysis
            })
            
            # Category routing
            category = self._extract_category(analysis)
            if category not in categories:
                categories[category] = []
            categories[category].append(ticket)
        
        return {
            "by_priority": routed,
            "by_category": categories,
            "routing_summary": self._generate_routing_summary(routed, categories)
        }
    
    def customer_journey_analysis(
        self,
        customer_id: str,
        ticket_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze customer's support journey.
        
        Args:
            customer_id: Customer identifier
            ticket_history: List of customer's previous tickets
        
        Returns:
            Customer journey analysis
        """
        print(f"Analyzing journey for customer {customer_id}...")
        
        # Analyze patterns
        total_tickets = len(ticket_history)
        resolved = sum(1 for t in ticket_history if not t.get("requires_escalation"))
        avg_sentiment = self._calculate_avg_sentiment(ticket_history)
        
        # Generate insights
        journey_prompt = f"""Analyze customer support journey:

Customer ID: {customer_id}
Total Tickets: {total_tickets}
Resolved: {resolved}
Average Sentiment: {avg_sentiment}

Recent tickets: {ticket_history[-3:]}

Provide:
1. Customer satisfaction level
2. Common issues
3. Resolution patterns
4. Improvement recommendations
5. Proactive support opportunities"""
        
        insights = self.agent.run(journey_prompt)
        
        return {
            "customer_id": customer_id,
            "total_tickets": total_tickets,
            "resolved_tickets": resolved,
            "resolution_rate": resolved / total_tickets if total_tickets > 0 else 0,
            "avg_sentiment": avg_sentiment,
            "insights": insights
        }
    
    def knowledge_base_optimization(
        self,
        common_issues: List[str]
    ) -> Dict[str, Any]:
        """
        Generate knowledge base articles for common issues.
        
        Args:
            common_issues: List of common customer issues
        
        Returns:
            Suggested KB articles
        """
        print("Generating knowledge base articles...")
        
        articles = []
        for issue in common_issues:
            print(f"Creating article for: {issue}")
            
            article_prompt = f"""Create knowledge base article for: {issue}

Include:
1. Clear title
2. Problem description
3. Step-by-step solution
4. Troubleshooting tips
5. Related articles
6. Contact support option

Make it clear and actionable."""
            
            article = self.agent.run(article_prompt)
            
            articles.append({
                "issue": issue,
                "article": article
            })
        
        return {
            "total_articles": len(articles),
            "articles": articles
        }
    
    def escalation_workflow(
        self,
        ticket_id: str,
        reason: str,
        original_response: str
    ) -> Dict[str, Any]:
        """
        Handle ticket escalation to human agent.
        
        Args:
            ticket_id: Ticket to escalate
            reason: Escalation reason
            original_response: AI's original response
        
        Returns:
            Escalation details and handoff info
        """
        print(f"Escalating ticket {ticket_id}...")
        
        escalation_prompt = f"""Prepare ticket escalation:

Ticket ID: {ticket_id}
Reason: {reason}
AI Response: {original_response[:200]}

Provide:
1. Summary for human agent
2. Key context to retain
3. Customer sentiment
4. Urgency level
5. Recommended next steps
6. Background information"""
        
        handoff_info = self.agent.run(escalation_prompt)
        
        return {
            "ticket_id": ticket_id,
            "escalation_reason": reason,
            "escalated_at": datetime.now().isoformat(),
            "handoff_information": handoff_info,
            "priority": "high"
        }
    
    def _create_follow_up_plan(
        self,
        ticket_id: str,
        resolved: bool
    ) -> Dict[str, Any]:
        """Create follow-up plan for ticket."""
        if resolved:
            return {
                "action": "satisfaction_survey",
                "timing": "24_hours",
                "message": "We hope your issue was resolved. Please rate your experience."
            }
        else:
            return {
                "action": "status_update",
                "timing": "4_hours",
                "message": "We're working on your issue. An update will be provided shortly."
            }
    
    def _generate_batch_summary(
        self,
        results: List[Dict[str, Any]]
    ) -> str:
        """Generate summary of batch processing."""
        total = len(results)
        escalated = sum(1 for r in results if r["requires_escalation"])
        
        return f"Processed {total} tickets. {escalated} escalated, {total - escalated} resolved."
    
    def _generate_routing_summary(
        self,
        by_priority: Dict[str, List],
        by_category: Dict[str, List]
    ) -> str:
        """Generate routing summary."""
        priority_counts = {k: len(v) for k, v in by_priority.items()}
        category_counts = {k: len(v) for k, v in by_category.items()}
        
        return f"Priority distribution: {priority_counts}. Categories: {category_counts}"
    
    def _extract_category(self, analysis: Dict[str, Any]) -> str:
        """Extract category from ticket analysis."""
        analysis_text = str(analysis.get("analysis", ""))
        
        categories = ["technical", "billing", "account", "product"]
        for cat in categories:
            if cat in analysis_text.lower():
                return cat
        
        return "general"
    
    def _calculate_avg_sentiment(
        self,
        ticket_history: List[Dict[str, Any]]
    ) -> str:
        """Calculate average sentiment from ticket history."""
        sentiments = [t.get("response", {}).get("sentiment", "neutral") 
                     for t in ticket_history]
        
        positive = sentiments.count("positive")
        negative = sentiments.count("negative")
        
        if positive > negative:
            return "positive"
        elif negative > positive:
            return "negative"
        return "neutral"
    
    def get_ticket_history(self) -> List[Dict[str, Any]]:
        """Get all tickets processed in this session."""
        return self.ticket_history


def create_support_workflow() -> SupportWorkflow:
    """Factory function to create a SupportWorkflow."""
    return SupportWorkflow()
