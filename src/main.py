import os
import sys
import pandas as pd
import json
import logging
from pathlib import Path
from dotenv import load_dotenv

# Import our modules (we'll create them next)
from triage_engine import classify_priority, route_to_agent
from guardian import analyze_churn_risk, send_guardian_alert
from opportunity import detect_business_intent, send_opportunity_alert
from response_generator import generate_draft_response
from report_builder import generate_html_dashboard

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load .env from project root (one level up from src/)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

def load_tickets(csv_path):
    """Load tickets from CSV file"""
    logger.info(f"Loading tickets from {csv_path}")
    df = pd.read_csv(csv_path)
    logger.info(f"Loaded {len(df)} tickets")
    return df

def load_agents():
    """Load agent profiles"""
    agents_path = DATA_DIR / "agents.json"
    with open(agents_path, 'r') as f:
        agents = json.load(f)
    logger.info(f"Loaded {len(agents)} agents")
    return agents

def process_ticket(ticket, agents):
    """Process a single ticket through the triage system"""
    ticket_id = ticket['ticket_id']
    logger.info(f"\n{'='*60}")
    logger.info(f"Processing {ticket_id}: {ticket['subject']}")
    
    result = {
        'ticket_id': ticket_id,
        'customer_name': ticket['customer_name'],
        'subject': ticket['subject'],
        'description': ticket['description'],
        'channel': ticket['channel'],
        'mrr': ticket['mrr'],
        'timestamp': ticket['timestamp']
    }
    
    # Step 1: Classify priority
    priority = classify_priority(ticket)
    result['assigned_priority'] = priority
    logger.info(f"✓ Priority: {priority}")
    
    # Step 2: Route to agent
    assigned_agent = route_to_agent(ticket, agents)
    result['assigned_agent'] = assigned_agent
    logger.info(f"✓ Routed to: {assigned_agent}")
    
    # Step 3: Guardian check (churn risk detection)
    guardian_result = analyze_churn_risk(
        ticket_text=ticket['description'],
        customer_mrr=ticket['mrr'],
        ticket_priority=priority
    )
    result['guardian'] = guardian_result
    
    if guardian_result['is_high_risk']:
        logger.warning(f"⚠ Guardian Alert: Risk score {guardian_result['risk_score']}/10")
        # Send email alert
        email_sent = send_guardian_alert(ticket, guardian_result)
        result['guardian']['email_sent'] = email_sent
    
    # Step 4: Opportunity check (revenue signal detection)
    opportunity_result = detect_business_intent(ticket['description'])
    result['opportunity'] = opportunity_result
    
    if opportunity_result['has_business_intent']:
        logger.info(f"💰 Opportunity detected: {opportunity_result['intent_type']}")
        # Send email alert
        email_sent = send_opportunity_alert(ticket, opportunity_result)
        result['opportunity']['email_sent'] = email_sent
    
    # Step 5: Generate draft response for P2/P3
    if priority in ['P2', 'P3']:
        draft = generate_draft_response(ticket, assigned_agent)
        result['draft_response'] = draft
        if draft:
            logger.info(f"✓ Draft response generated ({len(draft)} chars)")
    
    return result

def main():
    """Main execution"""
    logger.info("="*60)
    logger.info("CS AUTOMATION - SUPPORT TRIAGE SYSTEM")
    logger.info("="*60)
    
    # Create outputs directory if needed
    OUTPUTS_DIR.mkdir(exist_ok=True)
    
    # Load data
    tickets_df = load_tickets(DATA_DIR / "tickets_input.csv")
    agents = load_agents()
    
    # Process all tickets
    results = []
    for idx, ticket in tickets_df.iterrows():
        result = process_ticket(ticket, agents)
        results.append(result)
    
    logger.info(f"\n{'='*60}")
    logger.info(f"PROCESSING COMPLETE")
    logger.info(f"{'='*60}")
    logger.info(f"Total tickets processed: {len(results)}")
    
    # Generate outputs
    logger.info("\nGenerating outputs...")
    
    # 1. Generate HTML dashboard
    html_path = generate_html_dashboard(results, agents)
    logger.info(f"✓ Dashboard: {html_path}")
    
    # 2. Save results as JSON
    results_path = OUTPUTS_DIR / "triage_results.json"
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    logger.info(f"✓ Results JSON: {results_path}")
    
    # 3. Generate metrics summary
    metrics = generate_metrics(results)
    metrics_path = OUTPUTS_DIR / "metrics_summary.json"
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    logger.info(f"✓ Metrics: {metrics_path}")
    
    logger.info("\n✅ All done!")

def generate_metrics(results):
    """Calculate summary metrics"""
    total = len(results)
    guardian_alerts = sum(1 for r in results if r['guardian'].get('is_high_risk', False))
    opportunity_alerts = sum(1 for r in results if r['opportunity'].get('has_business_intent', False))
    auto_resolved = sum(1 for r in results if r.get('draft_response') is not None)
    
    return {
        'total_tickets': total,
        'guardian_alerts': guardian_alerts,
        'opportunity_alerts': opportunity_alerts,
        'auto_resolved': auto_resolved,
        'auto_resolved_rate': f"{(auto_resolved/total*100):.1f}%"
    }

if __name__ == "__main__":
    main()