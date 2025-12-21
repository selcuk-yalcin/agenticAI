"""Tests for Customer Support Agent.

This module tests:
- Ticket classification and routing
- Automated response generation
- Sentiment analysis
- Escalation decision making
"""

import pytest
from unittest.mock import Mock, patch


class TestSupportAgent:
    """Test suite for customer support functionality."""

    @pytest.fixture
    def sample_ticket(self):
        """Fixture providing a sample support ticket.
        
        Returns:
            dict: Support ticket with customer info and issue.
        """
        return {
            "ticket_id": "TKT-12345",
            "customer_name": "John Doe",
            "customer_email": "john@example.com",
            "subject": "Unable to login to account",
            "message": "I've been trying to login for the past hour but keep getting an error message. Very frustrated!",
            "priority": "medium",
            "category": "technical",
            "timestamp": "2024-01-15T10:30:00Z"
        }

    @pytest.fixture
    def sample_response_templates(self):
        """Fixture providing response templates.
        
        Returns:
            dict: Response templates by category.
        """
        return {
            "login_issue": """Dear {customer_name},

Thank you for contacting support. I understand you're experiencing login difficulties.

Please try the following steps:
1. Clear your browser cache and cookies
2. Reset your password using the "Forgot Password" link
3. Try using a different browser

If the issue persists, please let us know.

Best regards,
Support Team""",
            "billing_question": """Dear {customer_name},

Thank you for your billing inquiry.

I'd be happy to help you with your billing question. Could you please provide more details about your specific concern?

Best regards,
Support Team"""
        }

    def test_ticket_classification(self, sample_ticket):
        """Test automatic ticket classification.
        
        Categories:
        - Technical (login, bugs, errors)
        - Billing (payments, invoices, refunds)
        - General (questions, feedback)
        """
        def classify_ticket(ticket):
            """Classify ticket based on content."""
            message = ticket["message"].lower()
            subject = ticket["subject"].lower()
            combined = message + " " + subject
            
            # Simple keyword-based classification
            if any(word in combined for word in ["login", "password", "error", "bug"]):
                return "technical"
            elif any(word in combined for word in ["payment", "billing", "invoice", "refund"]):
                return "billing"
            else:
                return "general"
        
        category = classify_ticket(sample_ticket)
        
        assert category in ["technical", "billing", "general"]
        assert category == "technical"  # Based on "login" in subject

    def test_priority_assignment(self, sample_ticket):
        """Test automatic priority assignment.
        
        Priority levels:
        - Low: General questions, non-urgent
        - Medium: Technical issues, billing questions
        - High: Service outages, urgent problems
        - Critical: Security issues, data loss
        """
        def assign_priority(ticket):
            """Assign priority based on content and keywords."""
            message = ticket["message"].lower()
            
            urgent_keywords = ["urgent", "critical", "emergency", "immediately"]
            high_keywords = ["can't", "unable", "broken", "not working", "frustrated"]
            
            if any(word in message for word in urgent_keywords):
                return "critical"
            elif any(word in message for word in high_keywords):
                return "high"
            elif ticket.get("category") == "technical":
                return "medium"
            else:
                return "low"
        
        priority = assign_priority(sample_ticket)
        
        assert priority in ["low", "medium", "high", "critical"]
        assert priority in ["medium", "high"]  # Has "unable" and "frustrated"

    def test_sentiment_analysis(self, sample_ticket):
        """Test sentiment analysis of customer messages.
        
        Sentiments:
        - Positive: happy, satisfied, thank you
        - Neutral: informational, questions
        - Negative: frustrated, angry, disappointed
        """
        def analyze_sentiment(message):
            """Simple sentiment analysis."""
            message_lower = message.lower()
            
            positive_words = ["thank", "happy", "great", "excellent", "love", "satisfied"]
            negative_words = ["frustrated", "angry", "terrible", "horrible", "disappointed", "upset"]
            
            positive_score = sum(1 for word in positive_words if word in message_lower)
            negative_score = sum(1 for word in negative_words if word in message_lower)
            
            if negative_score > positive_score:
                sentiment = "negative"
            elif positive_score > negative_score:
                sentiment = "positive"
            else:
                sentiment = "neutral"
            
            return {
                "sentiment": sentiment,
                "positive_score": positive_score,
                "negative_score": negative_score,
                "confidence": abs(positive_score - negative_score) / max(positive_score + negative_score, 1)
            }
        
        result = analyze_sentiment(sample_ticket["message"])
        
        assert result["sentiment"] in ["positive", "neutral", "negative"]
        assert result["sentiment"] == "negative"  # Contains "frustrated"

    @patch('openai.ChatCompletion.create')
    def test_automated_response_generation(self, mock_openai, sample_ticket):
        """Test generation of automated responses.
        
        Response should:
        - Address customer by name
        - Acknowledge the issue
        - Provide solution or next steps
        - Be empathetic and professional
        """
        mock_openai.return_value = Mock(
            choices=[Mock(message=Mock(content="Thank you for contacting us. We'll help you resolve the login issue."))]
        )
        
        def generate_response(ticket):
            """Generate automated response."""
            response = mock_openai(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user",
                    "content": f"Generate a support response for: {ticket['message']}"
                }]
            )
            return response.choices[0].message.content
        
        response = generate_response(sample_ticket)
        
        assert isinstance(response, str)
        assert len(response) > 20

    def test_template_selection(self, sample_ticket, sample_response_templates):
        """Test selection of appropriate response template.
        
        Template selection based on:
        - Ticket category
        - Issue type
        - Customer history
        """
        def select_template(ticket, templates):
            """Select appropriate template."""
            message = ticket["message"].lower()
            
            if "login" in message or "password" in message:
                return templates.get("login_issue")
            elif "billing" in message or "payment" in message:
                return templates.get("billing_question")
            
            return None
        
        template = select_template(sample_ticket, sample_response_templates)
        
        assert template is not None
        assert "{customer_name}" in template

    def test_template_personalization(self, sample_ticket, sample_response_templates):
        """Test personalization of response templates.
        
        Personalization includes:
        - Customer name
        - Specific issue details
        - Account information
        """
        def personalize_template(template, ticket):
            """Personalize template with ticket data."""
            if not template:
                return ""
            
            personalized = template.format(
                customer_name=ticket.get("customer_name", "Customer"),
                ticket_id=ticket.get("ticket_id", "N/A")
            )
            return personalized
        
        template = sample_response_templates["login_issue"]
        response = personalize_template(template, sample_ticket)
        
        assert sample_ticket["customer_name"] in response
        assert "{customer_name}" not in response  # Template variables filled

    def test_escalation_decision(self, sample_ticket):
        """Test decision logic for ticket escalation.
        
        Escalation triggers:
        - High/critical priority
        - Multiple failed resolution attempts
        - Negative sentiment
        - VIP customer
        """
        def should_escalate(ticket, attempt_count=1):
            """Determine if ticket should be escalated."""
            priority = ticket.get("priority", "low")
            
            # Escalate if critical/high priority
            if priority in ["critical", "high"]:
                return True, "High priority ticket"
            
            # Escalate after 3 failed attempts
            if attempt_count >= 3:
                return True, "Multiple resolution attempts failed"
            
            # Check for angry customer
            message = ticket["message"].lower()
            if any(word in message for word in ["angry", "lawsuit", "complain", "manager"]):
                return True, "Customer requesting escalation"
            
            return False, None
        
        should_esc, reason = should_escalate(sample_ticket)
        
        assert isinstance(should_esc, bool)
        if should_esc:
            assert reason is not None

    def test_response_time_calculation(self, sample_ticket):
        """Test calculation of response time SLA.
        
        SLA targets:
        - Critical: 1 hour
        - High: 4 hours
        - Medium: 24 hours
        - Low: 48 hours
        """
        def calculate_sla_deadline(ticket, current_time="2024-01-15T11:00:00Z"):
            """Calculate SLA deadline based on priority."""
            from datetime import datetime, timedelta
            
            priority = ticket.get("priority", "low")
            ticket_time = datetime.fromisoformat(ticket["timestamp"].replace('Z', '+00:00'))
            current = datetime.fromisoformat(current_time.replace('Z', '+00:00'))
            
            sla_hours = {
                "critical": 1,
                "high": 4,
                "medium": 24,
                "low": 48
            }
            
            hours = sla_hours.get(priority, 48)
            deadline = ticket_time + timedelta(hours=hours)
            time_remaining = (deadline - current).total_seconds() / 3600  # hours
            
            return {
                "deadline": deadline.isoformat(),
                "hours_remaining": time_remaining,
                "is_overdue": time_remaining < 0
            }
        
        sla = calculate_sla_deadline(sample_ticket)
        
        assert "deadline" in sla
        assert "hours_remaining" in sla
        assert isinstance(sla["is_overdue"], bool)

    def test_canned_response_matching(self):
        """Test matching of canned responses to common issues.
        
        Common issues:
        - Password reset
        - Account locked
        - Feature request
        - Bug report
        """
        canned_responses = {
            "password_reset": "Please use the password reset link sent to your email.",
            "account_locked": "Your account has been locked due to multiple failed login attempts.",
            "feature_request": "Thank you for your suggestion. We'll consider it for future updates.",
            "bug_report": "Thank you for reporting this issue. Our team will investigate."
        }
        
        def match_canned_response(message, responses):
            """Match message to canned response."""
            message_lower = message.lower()
            
            if "password" in message_lower and "reset" in message_lower:
                return responses["password_reset"]
            elif "locked" in message_lower or "blocked" in message_lower:
                return responses["account_locked"]
            elif "suggest" in message_lower or "feature" in message_lower:
                return responses["feature_request"]
            elif "bug" in message_lower or "error" in message_lower:
                return responses["bug_report"]
            
            return None
        
        message = "I need to reset my password"
        response = match_canned_response(message, canned_responses)
        
        assert response is not None
        assert "password reset" in response.lower()

    def test_customer_satisfaction_prediction(self, sample_ticket):
        """Test prediction of customer satisfaction.
        
        Factors:
        - Response time
        - Resolution quality
        - Number of interactions
        - Sentiment trend
        """
        def predict_satisfaction(ticket, response_time_hours, interaction_count):
            """Predict customer satisfaction score (1-5)."""
            priority = ticket.get("priority", "low")
            
            # Start with base score
            score = 5.0
            
            # Deduct for slow response
            if priority == "critical" and response_time_hours > 1:
                score -= 2
            elif priority == "high" and response_time_hours > 4:
                score -= 1.5
            
            # Deduct for multiple interactions
            if interaction_count > 3:
                score -= 1
            
            # Check sentiment
            message = ticket["message"].lower()
            if any(word in message for word in ["frustrated", "angry"]):
                score -= 0.5
            
            return {
                "predicted_score": max(1, min(5, score)),  # Clamp to 1-5
                "confidence": 0.7,  # Simplified
                "factors": {
                    "response_time": response_time_hours,
                    "interactions": interaction_count
                }
            }
        
        result = predict_satisfaction(sample_ticket, response_time_hours=2, interaction_count=1)
        
        assert 1 <= result["predicted_score"] <= 5
        assert "confidence" in result
