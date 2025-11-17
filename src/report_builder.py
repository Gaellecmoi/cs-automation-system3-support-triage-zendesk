import os
import json
import logging
import webbrowser
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

def generate_html_dashboard(results, agents):
    """
    Generate comprehensive HTML dashboard
    Returns: path to generated HTML file
    """
    
    # Calculate metrics
    total = len(results)
    guardian_alerts = [r for r in results if r['guardian'].get('is_high_risk', False)]
    opportunity_alerts = [r for r in results if r['opportunity'].get('has_business_intent', False)]
    auto_resolved = [r for r in results if r.get('draft_response')]
    
    # Generate Zendesk API calls log
    zendesk_calls = generate_zendesk_api_calls(results)
    zendesk_path = OUTPUTS_DIR / "zendesk_api_calls.json"
    with open(zendesk_path, 'w') as f:
        json.dump(zendesk_calls, f, indent=2)
    
    # Generate Guardian alerts log
    guardian_log = [
        {
            'ticket_id': r['ticket_id'],
            'customer': r['customer_name'],
            'risk_score': r['guardian']['risk_score'],
            'evidence': r['guardian']['evidence'],
            'email_sent': r['guardian'].get('email_sent', False)
        }
        for r in guardian_alerts
    ]
    guardian_path = OUTPUTS_DIR / "guardian_alerts_log.json"
    with open(guardian_path, 'w') as f:
        json.dump(guardian_log, f, indent=2)
    
    # Generate Opportunity alerts log
    opportunity_log = [
        {
            'ticket_id': r['ticket_id'],
            'customer': r['customer_name'],
            'intent_type': r['opportunity']['intent_type'],
            'confidence': r['opportunity']['confidence'],
            'evidence': r['opportunity']['evidence'],
            'email_sent': r['opportunity'].get('email_sent', False)
        }
        for r in opportunity_alerts
    ]
    opportunity_path = OUTPUTS_DIR / "opportunity_alerts_log.json"
    with open(opportunity_path, 'w') as f:
        json.dump(opportunity_log, f, indent=2)
    
    # Build HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CS Automation - Support Triage Report</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .ticket-card {{ transition: all 0.3s ease; }}
        .ticket-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
    </style>
</head>
<body class="bg-gray-50">
    <div class="container mx-auto px-4 py-8 max-w-7xl">
        
        <!-- Header -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
            <h1 class="text-3xl font-bold text-gray-800 mb-2">Multi-Channel Support Triage System</h1>
            <p class="text-gray-600">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <!-- Summary Metrics -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div class="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
                <div class="text-blue-600 text-sm font-semibold">Total Tickets</div>
                <div class="text-3xl font-bold text-blue-700">{total}</div>
            </div>
            <div class="bg-green-50 border-l-4 border-green-500 p-4 rounded">
                <div class="text-green-600 text-sm font-semibold">Auto-Resolved</div>
                <div class="text-3xl font-bold text-green-700">{len(auto_resolved)}</div>
                <div class="text-green-600 text-xs">{len(auto_resolved)/total*100:.0f}% of total</div>
            </div>
            <div class="bg-red-50 border-l-4 border-red-500 p-4 rounded">
                <div class="text-red-600 text-sm font-semibold">Guardian Alerts</div>
                <div class="text-3xl font-bold text-red-700">{len(guardian_alerts)}</div>
                <div class="text-red-600 text-xs">{len(guardian_alerts)/total*100:.0f}% churn risk</div>
            </div>
            <div class="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded">
                <div class="text-yellow-600 text-sm font-semibold">Opportunity Alerts</div>
                <div class="text-3xl font-bold text-yellow-700">{len(opportunity_alerts)}</div>
                <div class="text-yellow-600 text-xs">{len(opportunity_alerts)/total*100:.0f}% revenue signals</div>
            </div>
        </div>
        
        <!-- Guardian Alerts Section -->
        {generate_guardian_section(guardian_alerts)}
        
        <!-- Opportunity Alerts Section -->
        {generate_opportunity_section(opportunity_alerts)}
        
        <!-- All Tickets -->
        {generate_tickets_section(results)}
        
        <!-- API Integration Preview -->
        {generate_api_preview_section(zendesk_calls[:3])}
        
    </div>
    
    <script>
        function toggleDetails(ticketId) {{
            const el = document.getElementById('details-' + ticketId);
            el.classList.toggle('hidden');
        }}
    </script>
</body>
</html>"""
    
    # Save HTML
    html_path = OUTPUTS_DIR / "triage_report.html"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    # Open in browser
    webbrowser.open(f'file://{html_path.absolute()}')
    
    return html_path


def generate_guardian_section(alerts):
    """Generate Guardian alerts section HTML"""
    if not alerts:
        return '<div class="bg-white rounded-lg shadow-md p-6 mb-6"><h2 class="text-xl font-bold text-gray-800">🚨 Guardian Alerts</h2><p class="text-gray-600 mt-2">No high-risk tickets detected</p></div>'
    
    cards = ""
    for ticket in alerts:
        cards += f"""
        <div class="bg-red-50 border border-red-200 rounded-lg p-4 ticket-card">
            <h3 class="font-bold text-red-600 text-lg" style="color: #FF0000;">{ticket['ticket_id']}</h3>
            <p class="text-gray-700 mt-1"><strong>Customer:</strong> {ticket['customer_name']} (MRR: ${ticket['mrr']:,})</p>
            <p class="text-gray-700"><strong>Risk Score:</strong> <span class="text-red-600 font-bold">{ticket['guardian']['risk_score']}/10</span></p>
            <p class="text-gray-700"><strong>Evidence:</strong> "{ticket['guardian']['evidence']}"</p>
            <p class="text-gray-700"><strong>Action:</strong> ✉️ Email sent to KAM</p>
        </div>
        """
    
    return f"""
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 class="text-2xl font-bold text-gray-800 mb-4">🚨 Guardian Alerts - High-Risk Accounts</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            {cards}
        </div>
    </div>
    """


def generate_opportunity_section(alerts):
    """Generate Opportunity alerts section HTML"""
    if not alerts:
        return '<div class="bg-white rounded-lg shadow-md p-6 mb-6"><h2 class="text-xl font-bold text-gray-800">💰 Opportunity Alerts</h2><p class="text-gray-600 mt-2">No revenue signals detected</p></div>'
    
    cards = ""
    for ticket in alerts:
        intent_display = ticket['opportunity']['intent_type'].replace('_', ' ').title()
        cards += f"""
        <div class="bg-green-50 border border-green-200 rounded-lg p-4 ticket-card">
            <h3 class="font-bold text-green-600 text-lg" style="color: #00AA00;">{ticket['ticket_id']}</h3>
            <p class="text-gray-700 mt-1"><strong>Customer:</strong> {ticket['customer_name']} (MRR: ${ticket['mrr']:,})</p>
            <p class="text-gray-700"><strong>Intent:</strong> {intent_display}</p>
            <p class="text-gray-700"><strong>Confidence:</strong> {ticket['opportunity']['confidence']}/10</p>
            <p class="text-gray-700"><strong>Evidence:</strong> "{ticket['opportunity']['evidence']}"</p>
            <p class="text-gray-700"><strong>Action:</strong> ✉️ Email sent to Sales</p>
        </div>
        """
    
    return f"""
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 class="text-2xl font-bold text-gray-800 mb-4">💰 Opportunity Alerts - Revenue Signals</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            {cards}
        </div>
    </div>
    """


def generate_tickets_section(results):
    """Generate all tickets table"""
    rows = ""
    for ticket in results:
        priority_color = {
            'P0': 'bg-red-100 text-red-800',
            'P1': 'bg-orange-100 text-orange-800',
            'P2': 'bg-blue-100 text-blue-800',
            'P3': 'bg-green-100 text-green-800'
        }.get(ticket['assigned_priority'], 'bg-gray-100 text-gray-800')
        priority_label = {
            'P0': 'P0 - Critical',
            'P1': 'P1 - High',
            'P2': 'P2 - Medium',
            'P3': 'P3 - Low'

}.get(ticket['assigned_priority'], ticket['assigned_priority'])
        
        draft_status = "✅ Auto-resolved" if ticket.get('draft_response') else "👤 Routed to team"
        
        rows += f"""
        <tr class="border-b hover:bg-gray-50">
            <td class="px-4 py-3 font-mono text-sm">{ticket['ticket_id']}</td>
            <td class="px-4 py-3">{ticket['customer_name']}</td>
            <td class="px-4 py-3 text-sm">{ticket['subject'][:50]}...</td>
            <td class="px-4 py-3"><span class="px-2 py-1 rounded text-xs font-semibold {priority_color}">{priority_label}</span></td>
            <td class="px-4 py-3 text-sm">{ticket['assigned_agent']}</td>
            <td class="px-4 py-3 text-sm">{draft_status}</td>
            <td class="px-4 py-3"><button onclick="toggleDetails('{ticket['ticket_id']}')" class="text-blue-600 hover:underline text-sm">Details</button></td>
        </tr>
        <tr id="details-{ticket['ticket_id']}" class="hidden bg-gray-50">
            <td colspan="7" class="px-4 py-3">
                <div class="text-sm space-y-2">
                    <p><strong>Description:</strong> {ticket['description']}</p>
                    {f"<p><strong>Draft Response:</strong></p><div class='bg-white p-3 rounded border mt-1 whitespace-pre-wrap'>{ticket['draft_response']}</div>" if ticket.get('draft_response') else ""}
                </div>
            </td>
        </tr>
        """
    
    return f"""
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 class="text-2xl font-bold text-gray-800 mb-4">🎫 All Tickets</h2>
        <div class="overflow-x-auto">
            <table class="min-w-full">
                <thead class="bg-gray-100">
                    <tr>
                        <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Ticket ID</th>
                        <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Customer</th>
                        <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Subject</th>
                        <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Priority</th>
                        <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Agent</th>
                        <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Status</th>
                        <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
    </div>
    """


def generate_api_preview_section(sample_calls):
    """Generate Zendesk API integration preview"""
    examples = ""
    for call in sample_calls:
        examples += f"""
        <div class="bg-gray-50 rounded-lg p-4 mb-3">
            <h4 class="font-semibold text-gray-800 mb-2">Ticket {call['ticket_id']} - {call['action']}</h4>
            <pre class="bg-gray-800 text-green-400 p-3 rounded text-xs overflow-x-auto"><code>{json.dumps(call['api_payload'], indent=2)}</code></pre>
        </div>
        """
    
    return f"""
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 class="text-2xl font-bold text-gray-800 mb-2">🔌 API Integration Preview - Zendesk Calls</h2>
        <p class="text-gray-600 mb-4 text-sm">In production, the system would execute these API calls to update tickets in Zendesk.</p>
        {examples}
        <a href="zendesk_api_calls.json" class="inline-block mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 text-sm">📥 Download Full API Call Log (JSON)</a>
    </div>
    """


def generate_zendesk_api_calls(results):
    """Generate Zendesk API call log"""
    calls = []

       # Team name mapping for Zendesk
    team_mapping = {
        "Integrations & API Team": "integrations-api-team",
        "Data & Analytics Team": "data-analytics-team",
        "Compliance & Operations Team": "compliance-operations-team"
    }
    
    for ticket in results:
        action = "solve" if ticket.get('draft_response') else "assign"

        # Map team name to Zendesk queue ID
        assigned_team = team_mapping.get(ticket['assigned_agent'], "integrations-api-team")

        
        payload = {
            "ticket": {
                "id": ticket['ticket_id'],
                "status": "solved" if action == "solve" else "open",
                "priority": ticket['assigned_priority'].lower(),
                "assignee": assigned_team,  # <-- Utilise le mapping ici
                "tags": [
                    assigned_team,  # <-- Et ici aussi
                    ticket['assigned_priority'].lower()
                ],
                "custom_fields": []
            }
        }
        
        # Add Guardian custom fields if high risk
        if ticket['guardian'].get('is_high_risk'):
            payload['ticket']['tags'].append('churn-risk')
            payload['ticket']['custom_fields'].append({
                "id": 360001,
                "value": ticket['guardian']['risk_score']
            })
        
        # Add Opportunity custom fields if business intent
        if ticket['opportunity'].get('has_business_intent'):
            payload['ticket']['tags'].append('upsell-opportunity')
            payload['ticket']['custom_fields'].append({
                "id": 360002,
                "value": ticket['opportunity']['intent_type']
            })
        
        # Add comment if auto-resolved
        if action == "solve":
            payload['ticket']['comment'] = {
                "body": ticket['draft_response'],
                "public": True
            }
        
        calls.append({
            "ticket_id": ticket['ticket_id'],
            "action": action,
            "api_endpoint": f"PUT /api/v2/tickets/{ticket['ticket_id']}.json",
            "api_payload": payload
        })
    
    return calls