from dotenv import load_dotenv
from pathlib import Path

# Load .env
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

import os
import logging
from anthropic import Anthropic

logger = logging.getLogger(__name__)

# Initialize Claude client
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def classify_priority(ticket):
    """
    Classify ticket priority using Claude AI
    Returns: P0, P1, P2, or P3
    """
    
    prompt = f"""Analyze this B2B SaaS support ticket and classify its priority level.

Ticket:
Subject: {ticket['subject']}
Description: {ticket['description']}
Channel: {ticket['channel']}

Priority classification criteria:

P0 (Critical) - ONLY if:
- Explicit mention of "system down", "outage", "all customers affected"
- Data loss or security breach mentioned
- Direct revenue impact stated (e.g., "cannot process payments")
- Use sparingly: ~3% of tickets

P1 (High) - If:
- Major feature completely broken (not just slow/delayed)
- Explicit churn threat or competitor mention
- Customer states "urgent" or "blocking our business"
- Repeated critical issue (e.g., "3rd time this fails")
- Target: ~30% of tickets

P2 (Medium) - If:
- Important functionality degraded but workaround exists
- Delays or performance issues (not complete failure)
- Configuration questions requiring expertise
- Integration issues affecting single customer
- Target: ~40% of tickets

P3 (Low) - If:
- "How to" questions or setup guidance
- Feature requests
- Minor bugs or cosmetic issues
- General inquiries
- Documentation requests
- Target: ~25% of tickets

IMPORTANT:
- Don't assume worst-case scenario
- "Not working" ≠ automatically P1 (could be user error = P3)
- Delays/slowness = P2, not P1
- If uncertain between two levels, choose the LOWER priority

Return ONLY: P0, P1, P2, or P3
No explanation."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=10,
            messages=[{"role": "user", "content": prompt}]
        )
        
        priority = response.content[0].text.strip()
        
        # Validate response
        if priority not in ['P0', 'P1', 'P2', 'P3']:
            logger.warning(f"Invalid priority '{priority}', defaulting to P2")
            priority = 'P2'
        
        return priority
        
    except Exception as e:
        logger.error(f"Error classifying priority: {e}")
        # Fallback: use actual_priority from CSV if available
        return ticket.get('actual_priority', 'P2')


def route_to_agent(ticket, agents):
    """
    Route ticket to appropriate agent based on technical domain
    Returns: agent name (Nexus, Cipher, or Sentinel)
    """
    
    # Build agent descriptions for Claude
    agent_descriptions = "\n".join([
        f"- {agent['name']}: {agent['description']}\n  Specialties: {', '.join(agent['specialties'])}"
        for agent in agents
    ])
    
    prompt = f"""Route this support ticket to the most appropriate technical agent.

Ticket:
Subject: {ticket['subject']}
Description: {ticket['description']}

Available agents:
{agent_descriptions}

Based on the ticket content, which agent should handle this?
Return ONLY the exact team name: "Integrations & API Team", "Data & Analytics Team", or "Compliance & Operations Team"
No explanation, just the name."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=10,
            messages=[{"role": "user", "content": prompt}]
        )
        
        agent_name = response.content[0].text.strip()
        
        # Validate response
        valid_agents = [agent['name'] for agent in agents]
        if agent_name not in valid_agents:
            logger.warning(f"Invalid agent '{agent_name}', defaulting to Integrations & API Team")
            agent_name = 'Integrations & API Team'
        return agent_name
        
    except Exception as e:
        logger.error(f"Error routing to agent: {e}")
        # Fallback to Integrations & API Team (most common case: integrations)
        return 'Integrations & API Team'