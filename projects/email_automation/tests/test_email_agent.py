"""Tests for Email Automation Agent.

This module tests:
- Email template generation and rendering
- Personalization and variable substitution
- Campaign scheduling and sending
- A/B testing and performance tracking
"""

import pytest
from unittest.mock import Mock, patch, MagicMock


class TestEmailAutomation:
    """Test suite for email automation functionality."""

    @pytest.fixture
    def sample_email_template(self):
        """Fixture providing a sample email template.
        
        Returns:
            dict: Email template with variables.
        """
        return {
            "template_id": "TPL-001",
            "name": "Welcome Email",
            "subject": "Welcome to {company_name}, {first_name}!",
            "body": """
Dear {first_name},

Welcome to {company_name}! We're thrilled to have you on board.

Here's what you can do next:
- Complete your profile
- Explore our features
- Join our community

Best regards,
The {company_name} Team
            """,
            "variables": ["first_name", "company_name"]
        }

    @pytest.fixture
    def sample_contact(self):
        """Fixture providing a sample contact.
        
        Returns:
            dict: Contact information.
        """
        return {
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "company": "Acme Corp",
            "segment": "new_customers"
        }

    @pytest.fixture
    def sample_campaign(self):
        """Fixture providing a sample email campaign.
        
        Returns:
            dict: Campaign configuration.
        """
        return {
            "campaign_id": "CAMP-001",
            "name": "New Customer Onboarding",
            "template_id": "TPL-001",
            "segment": "new_customers",
            "schedule": {
                "type": "immediate",
                "send_at": None
            },
            "ab_test": {
                "enabled": False,
                "variant_b_pct": 50
            }
        }

    def test_template_variable_substitution(self, sample_email_template, sample_contact):
        """Test substitution of variables in email templates.
        
        Variables:
        - {first_name} → Contact's first name
        - {company_name} → Company name
        - {custom_field} → Any custom field
        """
        def render_template(template, contact, company_name="Our Company"):
            """Render email template with contact data."""
            subject = template["subject"]
            body = template["body"]
            
            # Replace variables
            replacements = {
                "{first_name}": contact.get("first_name", ""),
                "{last_name}": contact.get("last_name", ""),
                "{company_name}": company_name
            }
            
            for var, value in replacements.items():
                subject = subject.replace(var, value)
                body = body.replace(var, value)
            
            return {
                "subject": subject,
                "body": body
            }
        
        rendered = render_template(sample_email_template, sample_contact, "TechStart")
        
        assert "John" in rendered["subject"]
        assert "TechStart" in rendered["subject"]
        assert "John" in rendered["body"]
        assert "{first_name}" not in rendered["body"]  # Variables replaced

    def test_contact_segmentation(self):
        """Test segmentation of contacts for targeted campaigns.
        
        Segments:
        - New customers
        - Active users
        - Inactive users
        - VIP customers
        """
        def segment_contacts(contacts, segment_type):
            """Filter contacts by segment."""
            if segment_type == "new_customers":
                return [c for c in contacts if c.get("segment") == "new_customers"]
            elif segment_type == "active":
                return [c for c in contacts if c.get("last_login_days", 999) <= 7]
            elif segment_type == "vip":
                return [c for c in contacts if c.get("lifetime_value", 0) > 1000]
            
            return contacts
        
        contacts = [
            {"email": "new@test.com", "segment": "new_customers"},
            {"email": "active@test.com", "last_login_days": 3},
            {"email": "vip@test.com", "lifetime_value": 2000}
        ]
        
        new_customers = segment_contacts(contacts, "new_customers")
        vip_customers = segment_contacts(contacts, "vip")
        
        assert len(new_customers) == 1
        assert len(vip_customers) == 1

    def test_email_validation(self):
        """Test validation of email addresses.
        
        Validation checks:
        - Valid format (user@domain.com)
        - Not in blacklist
        - Not a disposable email
        """
        import re
        
        def validate_email(email):
            """Validate email address."""
            # Basic regex validation
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            
            if not re.match(pattern, email):
                return {"valid": False, "reason": "Invalid format"}
            
            # Check for disposable domains (simplified)
            disposable_domains = ["tempmail.com", "throwaway.com"]
            domain = email.split("@")[1]
            
            if domain in disposable_domains:
                return {"valid": False, "reason": "Disposable email"}
            
            return {"valid": True}
        
        valid = validate_email("john@example.com")
        invalid = validate_email("not-an-email")
        disposable = validate_email("temp@tempmail.com")
        
        assert valid["valid"] is True
        assert invalid["valid"] is False
        assert disposable["valid"] is False

    @patch('smtplib.SMTP')
    def test_send_email_via_smtp(self, mock_smtp):
        """Test sending email via SMTP.
        
        SMTP configuration:
        - Server and port
        - Authentication
        - TLS encryption
        """
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        def send_email(to_email, subject, body, smtp_config):
            """Send email via SMTP."""
            import smtplib
            from email.mime.text import MIMEText
            
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = smtp_config['from_email']
            msg['To'] = to_email
            
            with smtplib.SMTP(smtp_config['host'], smtp_config['port']) as server:
                server.starttls()
                server.login(smtp_config['username'], smtp_config['password'])
                server.send_message(msg)
            
            return {"status": "sent"}
        
        smtp_config = {
            "host": "smtp.example.com",
            "port": 587,
            "username": "user",
            "password": "pass",
            "from_email": "noreply@example.com"
        }
        
        result = send_email("john@example.com", "Test", "Body", smtp_config)
        
        assert result["status"] == "sent"
        mock_server.starttls.assert_called_once()

    def test_campaign_scheduling(self, sample_campaign):
        """Test scheduling of email campaigns.
        
        Schedule types:
        - Immediate: Send now
        - Scheduled: Send at specific time
        - Recurring: Send at regular intervals
        """
        from datetime import datetime, timedelta
        
        def schedule_campaign(campaign):
            """Schedule campaign for sending."""
            schedule = campaign.get("schedule", {})
            schedule_type = schedule.get("type", "immediate")
            
            if schedule_type == "immediate":
                return {
                    "send_at": datetime.now().isoformat(),
                    "status": "queued"
                }
            elif schedule_type == "scheduled":
                send_at = schedule.get("send_at")
                return {
                    "send_at": send_at,
                    "status": "scheduled"
                }
            elif schedule_type == "recurring":
                # Schedule next occurrence
                interval = schedule.get("interval_days", 7)
                next_send = datetime.now() + timedelta(days=interval)
                return {
                    "send_at": next_send.isoformat(),
                    "status": "recurring",
                    "interval_days": interval
                }
            
            return {"status": "invalid"}
        
        result = schedule_campaign(sample_campaign)
        
        assert result["status"] == "queued"
        assert "send_at" in result

    def test_ab_test_variant_selection(self):
        """Test A/B test variant selection for contacts.
        
        A/B testing:
        - Split contacts into variants (A/B)
        - Random but consistent assignment
        - Track performance by variant
        """
        import hashlib
        
        def assign_variant(contact_email, variant_b_pct=50):
            """Assign A/B test variant based on email hash."""
            # Hash email for consistent assignment
            hash_val = int(hashlib.md5(contact_email.encode()).hexdigest(), 16)
            
            # Use hash to determine variant
            if (hash_val % 100) < variant_b_pct:
                return "B"
            else:
                return "A"
        
        variant1 = assign_variant("john@example.com", variant_b_pct=50)
        variant2 = assign_variant("john@example.com", variant_b_pct=50)
        variant3 = assign_variant("jane@example.com", variant_b_pct=50)
        
        assert variant1 in ["A", "B"]
        assert variant1 == variant2  # Consistent for same email
        # Different emails might get different variants

    def test_email_open_tracking(self):
        """Test tracking of email opens.
        
        Open tracking:
        - Embed tracking pixel
        - Record timestamp when pixel loaded
        - Calculate open rate
        """
        def add_tracking_pixel(email_body, tracking_id):
            """Add invisible tracking pixel to email."""
            pixel_url = f"https://track.example.com/pixel/{tracking_id}.png"
            pixel_html = f'<img src="{pixel_url}" width="1" height="1" alt="" />'
            
            # Add pixel at end of email
            tracked_body = email_body + pixel_html
            
            return tracked_body
        
        def calculate_open_rate(total_sent, total_opens):
            """Calculate email open rate."""
            if total_sent == 0:
                return 0
            
            return (total_opens / total_sent) * 100
        
        body = "<p>Hello!</p>"
        tracked = add_tracking_pixel(body, "TRK-123")
        
        assert "track.example.com" in tracked
        assert "TRK-123" in tracked
        
        open_rate = calculate_open_rate(total_sent=100, total_opens=25)
        assert open_rate == 25.0

    def test_click_tracking(self):
        """Test tracking of link clicks in emails.
        
        Click tracking:
        - Replace links with tracking URLs
        - Redirect through tracking server
        - Record click events
        """
        import re
        
        def add_click_tracking(email_body, campaign_id):
            """Replace links with tracking URLs."""
            # Find all URLs in email
            url_pattern = r'href="(https?://[^"]+)"'
            
            def replace_url(match):
                original_url = match.group(1)
                tracking_url = f"https://track.example.com/click/{campaign_id}?url={original_url}"
                return f'href="{tracking_url}"'
            
            tracked_body = re.sub(url_pattern, replace_url, email_body)
            
            return tracked_body
        
        body = '<a href="https://example.com/product">Click here</a>'
        tracked = add_click_tracking(body, "CAMP-001")
        
        assert "track.example.com" in tracked
        assert "CAMP-001" in tracked

    def test_unsubscribe_link_required(self):
        """Test that unsubscribe link is included in emails.
        
        Unsubscribe requirements:
        - Link must be clearly visible
        - One-click unsubscribe
        - Compliance with CAN-SPAM, GDPR
        """
        def validate_unsubscribe_link(email_body):
            """Validate that email contains unsubscribe link."""
            unsubscribe_keywords = ["unsubscribe", "opt-out", "manage preferences"]
            
            body_lower = email_body.lower()
            has_unsubscribe = any(keyword in body_lower for keyword in unsubscribe_keywords)
            
            return {
                "has_unsubscribe": has_unsubscribe,
                "compliant": has_unsubscribe
            }
        
        valid_email = "Click here to unsubscribe"
        invalid_email = "Just marketing content"
        
        result_valid = validate_unsubscribe_link(valid_email)
        result_invalid = validate_unsubscribe_link(invalid_email)
        
        assert result_valid["compliant"] is True
        assert result_invalid["compliant"] is False

    @patch('openai.ChatCompletion.create')
    def test_email_subject_line_generation(self, mock_openai):
        """Test generation of compelling subject lines using LLM.
        
        Subject line best practices:
        - Personalized
        - Clear value proposition
        - Sense of urgency (optional)
        - 50 characters or less
        """
        mock_openai.return_value = Mock(
            choices=[Mock(message=Mock(content="Unlock Your Exclusive Offer, John!"))]
        )
        
        def generate_subject_line(campaign_type, contact_name):
            """Generate email subject line using LLM."""
            response = mock_openai(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user",
                    "content": f"Generate compelling email subject for {campaign_type} campaign, personalized for {contact_name}"
                }]
            )
            
            subject = response.choices[0].message.content
            
            # Ensure subject is within character limit
            if len(subject) > 50:
                subject = subject[:47] + "..."
            
            return subject
        
        subject = generate_subject_line("promotional", "John")
        
        assert isinstance(subject, str)
        assert len(subject) <= 50

    def test_bounce_handling(self):
        """Test handling of email bounces.
        
        Bounce types:
        - Hard bounce: Invalid email, remove from list
        - Soft bounce: Temporary issue, retry later
        """
        def process_bounce(bounce_event):
            """Process email bounce notification."""
            bounce_type = bounce_event.get("type", "soft")
            email = bounce_event.get("email")
            
            if bounce_type == "hard":
                action = "remove_from_list"
                retry = False
            elif bounce_type == "soft":
                action = "retry_later"
                retry = True
            else:
                action = "none"
                retry = False
            
            return {
                "email": email,
                "action": action,
                "retry": retry
            }
        
        hard_bounce = process_bounce({"type": "hard", "email": "invalid@test.com"})
        soft_bounce = process_bounce({"type": "soft", "email": "temp@test.com"})
        
        assert hard_bounce["action"] == "remove_from_list"
        assert soft_bounce["retry"] is True

    def test_email_performance_metrics(self):
        """Test calculation of email campaign performance metrics.
        
        Metrics:
        - Open rate
        - Click-through rate (CTR)
        - Conversion rate
        - Unsubscribe rate
        """
        def calculate_campaign_metrics(stats):
            """Calculate campaign performance metrics."""
            sent = stats["sent"]
            
            if sent == 0:
                return {}
            
            metrics = {
                "open_rate": (stats["opens"] / sent) * 100,
                "click_rate": (stats["clicks"] / sent) * 100,
                "conversion_rate": (stats["conversions"] / sent) * 100,
                "unsubscribe_rate": (stats["unsubscribes"] / sent) * 100
            }
            
            return metrics
        
        stats = {
            "sent": 1000,
            "opens": 250,
            "clicks": 50,
            "conversions": 10,
            "unsubscribes": 5
        }
        
        metrics = calculate_campaign_metrics(stats)
        
        assert metrics["open_rate"] == 25.0
        assert metrics["click_rate"] == 5.0
        assert metrics["conversion_rate"] == 1.0
