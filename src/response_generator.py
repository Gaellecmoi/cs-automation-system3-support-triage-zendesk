from dotenv import load_dotenv
from pathlib import Path

# Load .env
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

import os
import json
import logging
from pathlib import Path
from anthropic import Anthropic

logger = logging.getLogger(__name__)

# Initialize Claude client
claude_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "data" / "knowledge_base"

def load_knowledge_base():
    """Load all FAQ files from knowledge base"""
    kb = {}
    
    # Load Shopify FAQ
    shopify_path = KNOWLEDGE_BASE_DIR / "shopify_faq.json"
    if shopify_path.exists():
        with open(shopify_path, 'r') as f:
            kb['shopify'] = json.load(f)
    
    # Load Payments FAQ
    payments_path = KNOWLEDGE_BASE_DIR / "payments_faq.json"
    if payments_path.exists():
        with open(payments_path, 'r') as f:
            kb['payments'] = json.load(f)
    
    return kb


def generate_draft_response(ticket, assigned_agent):
    """
    Generate draft response for P2/P3 tickets using knowledge base
    Returns: draft response text or None
    """
    
    # Load knowledge base
    kb = load_knowledge_base()
    
    # Build knowledge base context for Claude
    kb_context = "Available knowledge base articles:\n\n"
    
    for category, articles in kb.items():
        kb_context += f"{category.upper()} FAQ:\n"
        for key, article in articles.items():
            kb_context += f"- {article['question']}\n"
    
    prompt = f"""Generate a professional support response for this ticket.

Ticket:
Subject: {ticket['subject']}
Description: {ticket['description']}
Customer: {ticket['customer_name']}
Assigned Agent: {assigned_agent}

{kb_context}

Instructions:
1. Address the customer by name
2. Acknowledge their issue clearly
3. If the issue matches a knowledge base article, provide a helpful answer based on that content
4. Use professional but friendly B2B tone
5. Sign off with the agent name
6. If you cannot fully resolve, explain next steps

Generate the complete email response (including greeting and signature).
Keep it concise (200-300 words).
"""

    try:
        response = claude_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=600,
            messages=[{"role": "user", "content": prompt}]
        )
        
        draft = response.content[0].text.strip()
        return draft
        
    except Exception as e:
        logger.error(f"Error generating draft response: {e}")
        return None