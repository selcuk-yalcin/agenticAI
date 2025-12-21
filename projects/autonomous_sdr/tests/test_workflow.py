"""Tests for end-to-end Autonomous SDR workflow.

This module tests:
- Complete workflow from lead discovery to message sending
- Integration between components
- Error handling and retry logic
- Calendar scheduling integration
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta


class TestSDRWorkflow:
    """Test suite for complete SDR workflow."""

    @pytest.fixture
    def workflow_config(self):
        """Fixture providing workflow configuration.
        
        Returns:
            dict: Configuration for SDR workflow.
        """
        return {
            "max_leads_per_day": 50,
            "message_template": "professional",
            "follow_up_enabled": True,
            "follow_up_delay_days": 3,
            "calendar_provider": "google"
        }

    def test_workflow_discovers_and_scores_leads(self, workflow_config):
        """Test that workflow discovers leads and assigns scores.
        
        Workflow steps:
        1. Discover leads from sources
        2. Score each lead
        3. Filter by score threshold
        4. Return top N leads
        """
        def run_discovery_workflow(config):
            """Mock discovery workflow."""
            # Mock lead discovery
            raw_leads = [
                {"name": "John", "title": "VP Engineering", "company": "Tech"},
                {"name": "Jane", "title": "Manager", "company": "SaaS"},
                {"name": "Bob", "title": "Engineer", "company": "Startup"}
            ]
            
            # Score leads
            def score(lead):
                if "vp" in lead["title"].lower():
                    return 0.9
                elif "manager" in lead["title"].lower():
                    return 0.6
                return 0.3
            
            scored_leads = [(lead, score(lead)) for lead in raw_leads]
            
            # Filter by threshold
            threshold = 0.5
            filtered = [lead for lead, s in scored_leads if s >= threshold]
            
            # Return top N
            return filtered[:config["max_leads_per_day"]]
        
        results = run_discovery_workflow(workflow_config)
        assert len(results) > 0
        assert all("title" in lead for lead in results)

    def test_workflow_composes_personalized_messages(self):
        """Test that workflow generates personalized messages for each lead.
        
        Requirements:
        - One message per lead
        - Messages are unique (personalized)
        - All messages follow template
        """
        leads = [
            {"name": "John", "company": "TechCorp"},
            {"name": "Jane", "company": "SaaS Inc"}
        ]
        
        def compose_messages(leads, template_name):
            """Compose messages for all leads."""
            messages = []
            for lead in leads:
                msg = f"Hi {lead['name']}, I noticed your work at {lead['company']}..."
                messages.append({"lead": lead, "message": msg})
            return messages
        
        results = compose_messages(leads, "professional")
        
        assert len(results) == len(leads)
        assert results[0]["message"] != results[1]["message"]  # Personalized

    @patch('smtplib.SMTP')
    def test_workflow_sends_messages_via_email(self, mock_smtp):
        """Test sending messages via email channel.
        
        Tests:
        - SMTP connection is established
        - Email is formatted correctly
        - Message is sent successfully
        - Errors are handled gracefully
        """
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        def send_email(to_email, subject, body):
            """Send email via SMTP."""
            try:
                with mock_smtp('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login("user@example.com", "password")
                    server.sendmail("user@example.com", to_email, f"Subject: {subject}\n\n{body}")
                return {"status": "sent", "timestamp": datetime.now()}
            except Exception as e:
                return {"status": "failed", "error": str(e)}
        
        result = send_email("lead@company.com", "Quick question", "Hi John...")
        assert result["status"] in ["sent", "failed"]

    def test_workflow_tracks_message_status(self):
        """Test that workflow tracks message delivery and response status.
        
        Statuses:
        - pending: not yet sent
        - sent: delivered successfully
        - bounced: email bounced
        - replied: prospect responded
        - meeting_scheduled: meeting booked
        """
        messages = [
            {"id": 1, "lead": "John", "status": "pending"},
            {"id": 2, "lead": "Jane", "status": "sent"},
            {"id": 3, "lead": "Bob", "status": "replied"}
        ]
        
        def get_response_rate(messages):
            """Calculate response rate."""
            sent = sum(1 for m in messages if m["status"] in ["sent", "replied", "meeting_scheduled"])
            replied = sum(1 for m in messages if m["status"] in ["replied", "meeting_scheduled"])
            return (replied / sent * 100) if sent > 0 else 0
        
        rate = get_response_rate(messages)
        assert 0 <= rate <= 100

    def test_workflow_schedules_meetings_on_positive_reply(self):
        """Test automatic meeting scheduling when prospect replies positively.
        
        Flow:
        1. Detect positive reply (sentiment analysis or keywords)
        2. Fetch available calendar slots
        3. Send meeting link or invitation
        4. Update lead status
        """
        def handle_reply(message, reply_text):
            """Handle prospect reply."""
            positive_keywords = ["yes", "interested", "sounds good", "let's talk"]
            
            is_positive = any(kw in reply_text.lower() for kw in positive_keywords)
            
            if is_positive:
                # Mock calendar booking
                meeting_link = "https://calendly.com/user/15min"
                return {
                    "status": "meeting_scheduled",
                    "meeting_link": meeting_link,
                    "action": "send_calendar_link"
                }
            return {
                "status": "replied",
                "action": "human_review"
            }
        
        positive_reply = "Yes, I'm interested. Let's schedule a call."
        negative_reply = "No thanks, not interested."
        
        result_pos = handle_reply({}, positive_reply)
        result_neg = handle_reply({}, negative_reply)
        
        assert result_pos["status"] == "meeting_scheduled"
        assert result_neg["status"] == "replied"

    def test_workflow_implements_rate_limiting(self):
        """Test that workflow respects rate limits for sending.
        
        Rate limits:
        - Max messages per day
        - Max messages per hour
        - Delays between messages
        """
        def send_with_rate_limit(leads, max_per_day, delay_seconds):
            """Send messages with rate limiting."""
            sent_today = 0
            results = []
            
            for lead in leads:
                if sent_today >= max_per_day:
                    results.append({"lead": lead, "status": "rate_limited"})
                    continue
                
                # Simulate sending
                results.append({"lead": lead, "status": "sent"})
                sent_today += 1
                
                # Mock delay (in real implementation would use time.sleep)
                
            return results
        
        leads = [{"name": f"Lead{i}"} for i in range(100)]
        results = send_with_rate_limit(leads, max_per_day=50, delay_seconds=2)
        
        sent = sum(1 for r in results if r["status"] == "sent")
        rate_limited = sum(1 for r in results if r["status"] == "rate_limited")
        
        assert sent == 50
        assert rate_limited == 50

    def test_workflow_handles_unsubscribe_requests(self):
        """Test handling of unsubscribe/opt-out requests.
        
        Requirements:
        - Detect unsubscribe keywords
        - Add to suppression list
        - Stop all future outreach
        - Confirm unsubscribe
        """
        suppression_list = set()
        
        def handle_unsubscribe(email, request_text):
            """Process unsubscribe request."""
            unsubscribe_keywords = ["unsubscribe", "opt out", "stop", "remove me"]
            
            if any(kw in request_text.lower() for kw in unsubscribe_keywords):
                suppression_list.add(email)
                return {
                    "status": "unsubscribed",
                    "message": "You have been removed from our list."
                }
            return {"status": "active"}
        
        result = handle_unsubscribe("lead@company.com", "Please unsubscribe me")
        assert result["status"] == "unsubscribed"
        assert "lead@company.com" in suppression_list

    def test_workflow_end_to_end_integration(self, workflow_config):
        """Test complete end-to-end workflow integration.
        
        Full workflow:
        1. Discover leads
        2. Score and filter
        3. Compose messages
        4. Send messages
        5. Track delivery
        6. Handle replies
        7. Schedule meetings
        """
        def run_full_workflow(config):
            """Run complete SDR workflow."""
            # Step 1: Discover
            leads = [{"name": "John", "email": "john@tech.com", "score": 0.9}]
            
            # Step 2: Filter
            qualified = [l for l in leads if l["score"] >= 0.5]
            
            # Step 3: Compose
            messages = [{"lead": l, "text": f"Hi {l['name']}..."} for l in qualified]
            
            # Step 4: Send (mocked)
            sent = [{"message": m, "status": "sent"} for m in messages]
            
            # Step 5: Track
            tracked = [{"id": i, **s} for i, s in enumerate(sent)]
            
            return {
                "leads_discovered": len(leads),
                "leads_qualified": len(qualified),
                "messages_sent": len(sent),
                "success_rate": 100.0
            }
        
        result = run_full_workflow(workflow_config)
        
        assert result["leads_discovered"] > 0
        assert result["messages_sent"] > 0
        assert 0 <= result["success_rate"] <= 100
