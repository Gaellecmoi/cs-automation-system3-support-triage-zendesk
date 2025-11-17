from dotenv import load_dotenv
from pathlib import Path

# Load .env
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

import os
import logging
from anthropic import Anthropic
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = logging.getLogger(__name__)

# Initialize clients
claude_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
sendgrid_client = SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))

def analyze_churn_risk(ticket_text, customer_mrr, ticket_priority):
    """
    Analyze ticket for churn risk using sentiment analysis
    Returns dict with risk_score, is_high_risk, evidence, reasoning
    """
    
    prompt = f"""Analyze this B2B SaaS support ticket for customer churn risk.

Ticket content: {ticket_text}

Customer context:
- Monthly Recurring Revenue (MRR): ${customer_mrr}
- Ticket Priority: {ticket_priority}

Detect churn risk signals:
1. Frustrated or aggressive tone
2. Mentions of competitors or alternatives
3. Repeated issues (phrases like "3rd time", "again", "still not fixed")
4. Threats to cancel or escalate
5. Language indicating lost trust ("unacceptable", "disappointed")

Respond with this EXACT JSON format:

{{
    "risk_score": 7,
    "is_high_risk": true,
    "sentiment": "frustrated",
    "evidence": "third incident this month evaluating alternatives",
    "reasoning": "Customer mentions repeated issues and competitor consideration"
}}

Rules:
- risk_score: number 0-10
- is_high_risk: true if risk_score >= 7, false otherwise
- sentiment: "neutral" or "frustrated" or "angry"
- evidence: ONE continuous string, NO quotes inside, max 50 chars
- reasoning: brief explanation, max 100 chars

Scoring:
- 0-3: Low risk (neutral tone, first issue)
- 4-6: Medium risk (frustrated but not threatening)
- 7-8: High risk (repeated issues, considering alternatives)
- 9-10: Critical risk (explicit churn threat)

CRITICAL: Return ONLY valid JSON. No markdown. No extra text.
"""

    try:
        response = claude_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        
        import json
        result_text = response.content[0].text.strip()
        
        # Remove markdown code blocks if present
        if result_text.startswith("```"):
            result_text = result_text.split("```")[1]
            if result_text.startswith("json"):
                result_text = result_text[4:]
        result_text = result_text.strip()
        
        # Try to parse JSON
        try:
            result = json.loads(result_text)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error in Guardian: {e}")
            logger.error(f"Raw response: {result_text[:200]}")
            # Return safe fallback
            return {
                'risk_score': 5,
                'is_high_risk': False,
                'sentiment': 'neutral',
                'evidence': '',
                'reasoning': f'JSON parse error: {str(e)}'
            }
        
        # Ensure is_high_risk is boolean
        result['is_high_risk'] = result.get('risk_score', 0) >= 7
        
        return result
        
    except Exception as e:
        logger.error(f"Error analyzing churn risk: {e}")
        # Safe fallback
        return {
            'risk_score': 0,
            'is_high_risk': False,
            'sentiment': 'neutral',
            'evidence': '',
            'reasoning': 'Analysis failed'
        }


def send_guardian_alert(ticket, guardian_result):
    """
    Send email alert to KAM about high churn risk ticket
    Returns: True if sent successfully, False otherwise
    """
    
    kam_email = os.environ.get("GUARDIAN_EMAIL")
    
    if not kam_email:
        logger.warning("GUARDIAN_EMAIL not configured, skipping email")
        return False
    
    subject = f"🚨 Guardian Alert - High Churn Risk: Ticket {ticket['ticket_id']}"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #d32f2f;">🚨 Guardian Alert - High Churn Risk</h2>
        
        <div style="background: #fff3e0; padding: 15px; border-left: 4px solid #ff9800; margin: 20px 0;">
            <h3 style="margin-top: 0;">Critical Account Alert</h3>
            <p>Our CS automation system has flagged a high-risk situation requiring immediate attention.</p>
        </div>
        
        <h3>Ticket Details</h3>
        <table style="border-collapse: collapse; width: 100%;">
            <tr>
                <td style="padding: 8px; background: #f5f5f5;"><strong>Ticket ID:</strong></td>
                <td style="padding: 8px;">{ticket['ticket_id']}</td>
            </tr>
            <tr>
                <td style="padding: 8px; background: #f5f5f5;"><strong>Customer:</strong></td>
                <td style="padding: 8px;">{ticket['customer_name']}</td>
            </tr>
            <tr>
                <td style="padding: 8px; background: #f5f5f5;"><strong>MRR:</strong></td>
                <td style="padding: 8px;">${ticket['mrr']:,}</td>
            </tr>
            <tr>
                <td style="padding: 8px; background: #f5f5f5;"><strong>Risk Score:</strong></td>
                <td style="padding: 8px; color: #d32f2f;"><strong>{guardian_result['risk_score']}/10</strong></td>
            </tr>
            <tr>
                <td style="padding: 8px; background: #f5f5f5;"><strong>Sentiment:</strong></td>
                <td style="padding: 8px;">{guardian_result['sentiment'].title()}</td>
            </tr>
        </table>
        
        <h3>Risk Signals Detected</h3>
        <div style="background: #ffebee; padding: 15px; border-radius: 4px;">
            <p><strong>Evidence:</strong> "{guardian_result['evidence']}"</p>
            <p><strong>Assessment:</strong> {guardian_result['reasoning']}</p>
        </div>
        
        <h3>Ticket Content</h3>
        <div style="background: #f5f5f5; padding: 15px; border-radius: 4px;">
            <p><strong>Subject:</strong> {ticket['subject']}</p>
            <p><strong>Description:</strong></p>
            <p style="white-space: pre-wrap;">{ticket['description']}</p>
        </div>
        
        <h3>Recommended Action</h3>
        <div style="background: #e8f5e9; padding: 15px; border-left: 4px solid #4caf50; margin: 20px 0;">
            <p><strong>Priority:</strong> Immediate outreach within 2 hours</p>
            <p><strong>Approach:</strong> Acknowledge frustration, provide executive-level attention, offer concrete resolution timeline</p>
            <p><strong>Technical Context:</strong> Issue being handled by technical team (check ticket for assignment)</p>
        </div>
        
        <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
        <p style="font-size: 12px; color: #777;">
            This alert was generated automatically by the CS Automation Guardian system.<br>
            For questions, contact the CS Operations team.
        </p>
    </body>
    </html>
    """
    
    try:
        message = Mail(
            from_email=kam_email,  # SendGrid verified sender
            to_emails=kam_email,    # Send to same email for demo
            subject=subject,
            html_content=html_content
        )
        
        response = sendgrid_client.send(message)
        
        if response.status_code in [200, 202]:
            logger.info(f"✉️  Guardian alert sent to {kam_email}")
            return True
        else:
            logger.error(f"Failed to send Guardian alert: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending Guardian alert: {e}")
        return False