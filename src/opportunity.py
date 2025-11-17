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

def detect_business_intent(ticket_text):
    """
    Detect commercial/revenue signals in ticket using Claude AI
    Returns dict with has_business_intent, intent_type, confidence, evidence
    """
    
    prompt = f"""Analyze this B2B SaaS support ticket for commercial intent signals.

Ticket content: {ticket_text}

Detect if customer is expressing interest in:
1. Pricing information (quote, devis, tarif, pricing, cost)
2. Upgrading plan/tier (upgrade, enterprise, premium, higher plan)
3. Additional capacity (more users, licenses, API calls, storage)
4. Custom/dedicated services (SLA, dedicated support, custom onboarding, white-label)

CRITICAL: Ignore technical uses of words like "quote" (e.g., "quote the error message").
Focus on genuine buying signals.

Respond with JSON:
{{
    "has_business_intent": true/false,
    "intent_type": "pricing_request" | "upgrade" | "expansion" | "custom_service" | null,
    "confidence": 0-10,
    "evidence": "exact phrase showing intent",
    "reasoning": "brief explanation"
}}

Examples:
- "Can we get a quote for 50 additional users?" → has_business_intent: true, confidence: 10
- "Please quote the exact error message" → has_business_intent: false, confidence: 0
- "Interested in enterprise plan features" → has_business_intent: true, confidence: 8
- "How do I upgrade my account?" → has_business_intent: true, confidence: 7

Only set has_business_intent to true if confidence >= 6

Return valid JSON only.
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
            logger.error(f"JSON parse error in Opportunity: {e}")
            logger.error(f"Raw response: {result_text[:200]}")
            # Return safe fallback
            return {
                'has_business_intent': False,
                'intent_type': None,
                'confidence': 0,
                'evidence': '',
                'reasoning': f'JSON parse error: {str(e)}'
            }
        
        # Ensure has_business_intent is boolean
        result['has_business_intent'] = result.get('confidence', 0) >= 6
        
        return result
        
    except Exception as e:
        logger.error(f"Error analyzing business intent: {e}")
        # Safe fallback
        return {
            'has_business_intent': False,
            'intent_type': None,
            'confidence': 0,
            'evidence': '',
            'reasoning': 'Analysis failed'
        }

def send_opportunity_alert(ticket, opportunity_result):
    """
    Send email alert to Sales/AM about revenue opportunity
    Returns: True if sent successfully, False otherwise
    """
    
    sales_email = os.environ.get("OPPORTUNITY_EMAIL")
    
    if not sales_email:
        logger.warning("OPPORTUNITY_EMAIL not configured, skipping email")
        return False
    
    intent_type_display = {
        'pricing_request': 'Pricing Inquiry',
        'upgrade': 'Upgrade Interest',
        'expansion': 'Capacity Expansion',
        'custom_service': 'Custom Service Request'
    }
    
    intent_display = intent_type_display.get(
        opportunity_result.get('intent_type'), 
        'Business Inquiry'
    )
    
    subject = f"💰 Opportunity Alert - {intent_display}: Ticket {ticket['ticket_id']}"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #2e7d32;">💰 Opportunity Alert - Revenue Signal Detected</h2>
        
        <div style="background: #e8f5e9; padding: 15px; border-left: 4px solid #4caf50; margin: 20px 0;">
            <h3 style="margin-top: 0;">Commercial Intent Identified</h3>
            <p>A support ticket contains a clear commercial signal that requires sales follow-up.</p>
        </div>
        
        <h3>Opportunity Details</h3>
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
                <td style="padding: 8px; background: #f5f5f5;"><strong>Current MRR:</strong></td>
                <td style="padding: 8px;">${ticket['mrr']:,}</td>
            </tr>
            <tr>
                <td style="padding: 8px; background: #f5f5f5;"><strong>Intent Type:</strong></td>
                <td style="padding: 8px; color: #2e7d32;"><strong>{intent_display}</strong></td>
            </tr>
            <tr>
                <td style="padding: 8px; background: #f5f5f5;"><strong>Confidence:</strong></td>
                <td style="padding: 8px;">{opportunity_result['confidence']}/10</td>
            </tr>
        </table>
        
        <h3>Customer Quote</h3>
        <div style="background: #fff3e0; padding: 15px; border-radius: 4px; border-left: 4px solid #ff9800;">
            <p style="font-style: italic; margin: 0;">"{opportunity_result['evidence']}"</p>
        </div>
        
        <h3>Full Ticket Context</h3>
        <div style="background: #f5f5f5; padding: 15px; border-radius: 4px;">
            <p><strong>Subject:</strong> {ticket['subject']}</p>
            <p><strong>Description:</strong></p>
            <p style="white-space: pre-wrap;">{ticket['description']}</p>
        </div>
        
        <h3>Analysis</h3>
        <div style="background: #e3f2fd; padding: 15px; border-radius: 4px;">
            <p>{opportunity_result['reasoning']}</p>
        </div>
        
        <h3>Recommended Action</h3>
        <div style="background: #e8f5e9; padding: 15px; border-left: 4px solid #4caf50; margin: 20px 0;">
            <p><strong>Timeline:</strong> Respond within 24 hours while intent is active</p>
            <p><strong>Approach:</strong> 
                {get_approach_recommendation(opportunity_result.get('intent_type'))}
            </p>
            <p><strong>Next Steps:</strong> Contact customer to understand requirements and provide customized proposal</p>
        </div>
        
        <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
        <p style="font-size: 12px; color: #777;">
            This alert was generated automatically by the CS Automation Opportunity system.<br>
            For questions, contact the CS Operations team.
        </p>
    </body>
    </html>
    """
    
    try:
        message = Mail(
                  from_email=sales_email,  # SendGrid verified sender
            to_emails=sales_email,    # Send to same email for demo
            subject=subject,
            html_content=html_content
        )
        
        response = sendgrid_client.send(message)
        
        if response.status_code in [200, 202]:
            logger.info(f"✉️  Opportunity alert sent to {sales_email}")
            return True
        else:
            logger.error(f"Failed to send Opportunity alert: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending Opportunity alert: {e}")
        return False


def get_approach_recommendation(intent_type):
    """Return tailored approach based on intent type"""
    approaches = {
        'pricing_request': 'Provide detailed pricing breakdown, highlight ROI and value proposition',
        'upgrade': 'Showcase enterprise features, offer demo of advanced capabilities, discuss migration path',
        'expansion': 'Present volume discount options, discuss scalability roadmap, flexible payment terms',
        'custom_service': 'Schedule technical consultation, gather detailed requirements, prepare custom proposal'
    }
    return approaches.get(intent_type, 'Understand specific needs and provide tailored solution')