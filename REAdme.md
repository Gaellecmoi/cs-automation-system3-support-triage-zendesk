# Multi-Channel Support Tickets Triage System

> AI-powered customer support automation for B2B SaaS e-commerce platforms

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Overview

This system automates support ticket triage for B2B SaaS companies in the e-commerce infrastructure space. It combines technical routing with intelligent business signal detection to optimize CS operations while protecting revenue.

**Key capabilities:**
- **Automated resolution** of 40% of P2/P3 tickets
- **Churn prevention** through sentiment-based risk detection
- **Revenue capture** via upsell signal identification
- **Intelligent routing** to specialized technical agents

Built as a proof-of-concept demonstrating production-grade CS automation logic for scale-up environments.

---

## 🏗️ Architecture

### Technical Routing Layer (3 Specialized Teams)

The system automatically routes tickets to specialized human support teams based on technical domain analysis:

**Integrations & API Team**  
Handles platform integrations (Shopify, WooCommerce, BigCommerce), webhook issues, authentication flows, and API errors. Specializes in connecting third-party services and troubleshooting connectivity problems.

**Data & Analytics Team**  
Manages tracking issues, event synchronization, data quality, performance optimization, and analytics pipeline problems. Experts in ensuring accurate data flow and measurement.

**Compliance & Operations Team**  
Covers payment processing (Stripe, PayPal), security, GDPR compliance, infrastructure, and operational workflows. Handles sensitive customer data and regulatory requirements.

### Intelligence Layers (2 Strategic Filters)

**Guardian** - Churn Prevention  
Analyzes ticket sentiment and account context to detect high-risk situations requiring immediate KAM intervention.

**Opportunity** - Revenue Expansion  
Identifies business intent signals (pricing requests, upgrade interest, expansion needs) and routes to Sales/AM.

### Processing Flow
```
Ticket Input (CSV)
    ↓
Technical Triage (P0/P1/P2/P3)
    ↓
Team Routing (Integrations & API / Data & Analytics / Compliance & Operations)
    ↓
Intelligence Analysis (parallel)
    ├─→ Guardian Layer → Churn risk? → Alert KAM
    └─→ Opportunity Layer → Revenue signal? → Alert Sales
    ↓
Action Execution
    ├─→ P2/P3: Generate draft response
    ├─→ P0/P1: Route to specialized team
    ├─→ Guardian alerts: Send email to KAM
    └─→ Opportunity alerts: Send email to Sales
    ↓
Output Generation
    ├─→ HTML Dashboard (visual report)
    ├─→ JSON Logs (API integration preview)
    └─→ Email Notifications (real-time alerts)
```

---

## 📋 Priority Classification System

The system uses industry-standard priority levels for ticket classification:

| Priority | Label | Description | SLA Target | Examples |
|----------|-------|-------------|------------|----------|
| **P0** | Critical | System outage, data loss, security breach, immediate revenue impact | Response: <30min<br>Resolution: <4h | "Orders not processing", "Payment system down", "Data breach detected" |
| **P1** | High | Major functionality broken, significant customer impact, churn risk | Response: <2h<br>Resolution: <24h | "Webhook failures", "Integration broken", "API timeout affecting multiple customers" |
| **P2** | Medium | Important issue with workaround available, moderate impact | Response: <8h<br>Resolution: <3 days | "Sync delays", "Configuration questions", "Performance degradation" |
| **P3** | Low | Minor issues, questions, feature requests, FAQ | Response: <24h<br>Resolution: Variable | "How to setup webhooks?", "Documentation request", "Minor UI bug" |

**Classification Logic:**
- Automated via Claude AI analyzing ticket content, customer context, and historical patterns
- Escalation triggers: specific keywords (e.g., "down", "critical", "emergency"), customer MRR, repeated issues
- Manual override available for edge cases

---

## ✨ Key Features

### 1. Intelligent Triage
- **4-level priority classification** (P0: system down → P3: FAQ)
- **Context-aware routing** based on technical domain
- **Automatic FAQ resolution** for P3 tickets

### 2. Churn Prevention (Guardian)
- Sentiment analysis via Claude AI
- Account risk scoring (sentiment + history + MRR)
- Real-time email alerts to Key Account Managers
- Recommended actions based on risk profile

### 3. Revenue Signal Capture (Opportunity)
- Contextual business intent detection (not just keywords)
- Pricing request identification
- Upgrade/expansion signal capture
- Automatic Sales team notification

### 4. Production-Ready Integration Preview
- Zendesk API call simulation (see exact payloads)
- Custom field mapping for agent assignment
- Tag management for workflow automation
- External action logging (emails, webhooks)

---

## 📊 Demo Metrics

Based on 30-ticket test corpus representing realistic B2B SaaS support scenarios:

| Metric | Value | Impact |
|--------|-------|--------|
| **Auto-resolution rate** | 40% (12/30 tickets) | Reduced agent workload |
| **Guardian alerts triggered** | 9 tickets (30%) | Proactive churn prevention |
| **Opportunity signals captured** | 8 tickets (27%) | Revenue expansion pipeline |
| **Average processing time** | 3.5s per ticket | Real-time triage capability |
| **Technical routing accuracy** | 100% | Correct specialist assignment |

### Priority Calibration

The system's priority classification can be calibrated via prompt engineering to match your organization's risk tolerance and support SLA structure.

**Current calibration targets:**
- P0 (Critical): ~5-7% of tickets
- P1 (High): ~25-30% of tickets
- P2 (Medium): ~40-50% of tickets
- P3 (Low): ~15-25% of tickets

**Tuning the classification:**

The classification prompt in `src/triage_engine.py` includes explicit percentage targets:
```python
P0 (Critical) - ONLY if:
- Explicit mention of "system down", "outage"
- Use sparingly: ~3% of tickets

P1 (High) - If:
- Major feature completely broken
- Target: ~30% of tickets
```

**Adjusting for your organization:**

**More conservative (higher priorities):**
- Increase P1 target to 40-50%
- Lower threshold for "blocking" language
- Useful for: High-touch enterprise customers, early-stage startups

**More balanced (current default):**
- P1 target: 25-30%
- Requires explicit urgency signals
- Useful for: Scale-ups, mid-market B2B SaaS

**More aggressive (lower priorities):**
- P1 target: 15-20%
- Require multiple urgency signals (e.g., "urgent" + revenue impact)
- Useful for: High-volume support, freemium products

**Validation approach:**
1. Run system on 100 historical tickets
2. Compare AI classification vs. actual agent classification
3. Measure agreement rate (target: >85%)
4. Adjust prompt weights if systematic bias detected
5. Re-test and iterate

**Example adjustment:**
If system over-classifies as P1 (as seen in initial testing), add:
```
IMPORTANT: If uncertain between two levels, choose the LOWER priority
"Not working" ≠ automatically P1 (could be user error = P3)
```

This reduced P1 classification from 70% → 27% in our test dataset.

---

## 📁 Test Data Methodology

### Synthetic Dataset Approach

This proof-of-concept uses **100% synthetically generated support tickets** to demonstrate the system's capabilities while maintaining full data privacy and control.

**Why synthetic data:**
- **Privacy-first**: No real customer data used or required
- **Context precision**: Every ticket represents realistic B2B SaaS e-commerce scenarios
- **Quality control**: Consistent structure, relevant technical details, appropriate tone variations
- **Reproducibility**: Dataset generation process is documented and repeatable

**Generation process:**
1. **Domain expertise**: Tickets based on 10+ years of CS experience in B2B SaaS Marketing/Commerce Tech
2. **AI augmentation**: Claude AI used to generate natural language variations while maintaining technical accuracy
3. **Validation**: Each ticket manually reviewed for realism and business relevance
4. **Diversity**: 30 tickets covering:
   - 4 technical categories (integrations, payments, fulfillment, analytics)
   - 4 priority levels (P0: critical → P3: FAQ)
   - 3 sentiment types (neutral, frustrated, aggressive)
   - 2 business intent categories (churn risk, upsell opportunity)

**Ticket structure:**
```csv
ticket_id,customer_name,subject,description,actual_priority,channel,timestamp,mrr
#1001,Acme Commerce,"Shopify webhook timeout","Our orders haven't synced...",P1,email,2025-11-14 09:23,5000
```

**Realism validation:**
- Technical terminology accuracy verified against Shopify/Stripe/Zendesk documentation
- Tone variations modeled on real B2B SaaS support patterns
- Business context (MRR, account history) based on industry benchmarks

**Limitations & Production Considerations:**
- Synthetic data cannot replicate 100% of real-world edge cases
- Production deployment would require training on actual historical ticket corpus
- Recommendation: A/B test system on 10% of live tickets before full rollout

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.9+
- SendGrid account (free tier) for email functionality
- Claude API key (Anthropic)

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/cs-automation-systeme3.git
cd cs-automation-systeme3

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys:
# ANTHROPIC_API_KEY=your_claude_key
# SENDGRID_API_KEY=your_sendgrid_key
# GUARDIAN_EMAIL=your_demo_email@example.com
# OPPORTUNITY_EMAIL=your_demo_email@example.com
```

### SendGrid Setup (5 minutes)

1. Create free account at [sendgrid.com](https://sendgrid.com)
2. Verify sender email address
3. Create API key (Settings → API Keys)
4. Add key to `.env` file

---

## 💻 Usage

### Run Full Triage
```bash
python src/main.py
```

**Output:**
- Terminal logs showing real-time processing
- `outputs/triage_report.html` (opens automatically in browser)
- `outputs/zendesk_api_calls.json` (Zendesk integration preview)
- `outputs/guardian_alerts_log.json` (churn prevention log)
- `outputs/opportunity_alerts_log.json` (revenue signal log)
- Real-time emails sent to configured addresses

### Process Custom Tickets
```bash
python src/main.py --input data/custom_tickets.csv
```

### Demo Mode (No Emails)
```bash
python src/main.py --demo-mode
```

Runs full triage but skips email sending (useful for testing).

---

## 📁 Project Structure
```
cs-automation-systeme3/
├── data/
│   ├── tickets_input.csv              # 30 test tickets (English)
│   ├── agents.json                    # Agent profiles & specialties
│   └── knowledge_base/
│       ├── shopify_faq.json           # FAQ for auto-responses
│       └── payments_faq.json
├── outputs/                           # Generated after each run
│   ├── triage_report.html
│   ├── zendesk_api_calls.json
│   ├── guardian_alerts_log.json
│   ├── opportunity_alerts_log.json
│   └── metrics_summary.json
├── src/
│   ├── main.py                        # Entry point
│   ├── triage_engine.py               # Core classification logic
│   ├── guardian.py                    # Churn prevention layer
│   ├── opportunity.py                 # Revenue signal detection
│   ├── response_generator.py          # P2/P3 auto-responses
│   └── report_builder.py              # HTML dashboard generation
├── .env.example                       # Environment template
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🔧 Technical Implementation Notes

### AI Model Usage

**Claude Sonnet 4.5 (Anthropic) for:**
1. **Technical triage** - Priority classification, agent routing
2. **Guardian sentiment analysis** - Contextual frustration/churn risk detection
3. **Opportunity intent detection** - Business signal identification (not keyword matching)
4. **Response generation** - P2/P3 draft creation using knowledge base

**Why Claude:**
- Superior contextual understanding vs. keyword-based systems
- Handles ambiguous/vague tickets effectively
- Generates human-quality draft responses
- Cost-effective for CS automation use cases

### Email Integration

**SendGrid implementation:**
- Separate templates for Guardian (churn) vs Opportunity (revenue)
- Fallback to HTML file generation if API unavailable
- Rate limiting: 100 emails/day (SendGrid free tier)
- Production recommendation: Upgrade to paid tier for scale

---

## 🏭 Production Deployment Considerations

### Zendesk Integration

The system generates automated draft responses for P2/P3 tickets. In production, these can be deployed in three modes:

**Option A: Internal Draft (Recommended for initial deployment)**
```json
{
  "ticket": {
    "comment": {
      "body": "[AI-generated draft - Please review before sending]\n\n{draft_text}",
      "public": false,
      "author_id": "automation_bot"
    }
  }
}
```
- Agent sees the draft as internal note
- Reviews and edits before sending to customer
- Provides human oversight and quality control
- Recommended for first 30-60 days of system use

**Option B: Auto-Send for FAQ (P3 only)**
```json
{
  "ticket": {
    "status": "solved",
    "comment": {
      "body": "{draft_text}",
      "public": true,
      "author_id": "automation_bot"
    }
  }
}
```
- Response sent directly to customer
- Ticket automatically marked as solved
- Use only for simple FAQ-type tickets (P3)
- Requires high confidence threshold (e.g., 95%+ match with knowledge base)

**Option C: Zendesk Answer Bot Integration**
- Leverage Zendesk's native "Answer Bot" feature
- System feeds drafts as suggested responses
- Agent approves/rejects with one click
- Tracks acceptance rate for continuous improvement

---

### ⚠️ Production Safety & Quality Control

**Critical consideration for automated responses:**

All AI-generated draft responses are created as **internal notes (non-public)** by default. A human agent must explicitly review and approve before any response is sent to the customer.

**Why human oversight is essential:**
- AI can misinterpret ambiguous or poorly-written tickets
- Edge cases and exceptions require human judgment
- Sensitive customer data must be handled appropriately
- Brand voice and tone must remain consistent
- Legal/compliance requirements may apply

**Quality thresholds for auto-send:**

Before enabling auto-send (Option B) for any ticket category, validate:

| Metric | Minimum Threshold | Measurement Period |
|--------|-------------------|-------------------|
| **Draft accuracy** | 95%+ match with agent-approved response | 30 days |
| **Customer satisfaction** | No degradation vs. human-only baseline | 60 days |
| **Escalation rate** | <2% of auto-resolved tickets reopened | 30 days |
| **Agent edit rate** | <10% of drafts require significant changes | 30 days |

**Confidence scoring:**

Each draft should include a confidence score based on:
- FAQ knowledge base match accuracy (exact vs. partial)
- Sentiment analysis (neutral/positive only for auto-send)
- Ticket complexity (word count, technical terms, multiple issues)
- Customer history (new vs. established, past satisfaction)

**Example implementation:**
```python
if (priority == 'P3' and 
    faq_match_confidence > 0.95 and
    sentiment in ['neutral', 'positive'] and
    ticket_complexity < 0.3 and
    customer_satisfaction_history > 4.0):
    
    mark_as_auto_send_candidate()  # Still requires 1-click agent approval
else:
    route_to_agent_queue_with_draft()
```

**Compliance note:**  
Certain industries (healthcare, finance, legal) may prohibit or restrict automated customer communications. Always consult legal/compliance teams before deploying auto-send features.

**Implementation Strategy:**
1. **Week 1-4:** Option A (all drafts as internal notes)
2. **Week 5-8:** Measure draft quality (agent edit rate, customer satisfaction)
3. **Week 9+:** Enable Option B for P3 tickets with >95% accuracy
4. **Ongoing:** Collect feedback loop data to improve draft quality

This proof-of-concept simulates Zendesk API integration. For production deployment:

**Architecture:**
```
Zendesk Webhook → AWS Lambda/Cloud Function → Triage System → Zendesk API
```

**Required components:**
1. **Webhook listener** - Trigger on ticket creation/update
2. **Authentication** - Zendesk API token + OAuth
3. **Custom fields** - Map agent IDs, risk scores, intent flags
4. **Error handling** - Retry logic, dead letter queue
5. **Monitoring** - CloudWatch/Datadog for system health

**API calls implemented** (see `outputs/zendesk_api_calls.json`):
- `PUT /api/v2/tickets/{id}.json` - Update priority, assignment, tags
- `POST /api/v2/tickets/{id}/comments.json` - Add auto-responses
- Custom fields: `guardian_risk_score`, `opportunity_intent`, `agent_id`

### Scalability

**Current PoC:** 30 tickets in ~105 seconds (local execution)

**Production targets:**
- **Volume:** 1,000-5,000 tickets/day for typical B2B SaaS scale-up
- **Latency:** <5s per ticket (including Claude API calls)
- **Architecture:** Containerized (Docker) + queue-based (SQS/RabbitMQ)
- **Caching:** Agent profiles, knowledge base, FAQ responses

**Estimated costs (1,000 tickets/day):**
- Claude API: ~$15-30/month (based on token usage)
- SendGrid: $15/month (Essentials plan, 50k emails)
- Infrastructure: $20-50/month (AWS Lambda + RDS)  
**Total:** ~$50-95/month

---

## 🎯 Business Impact

### For CS Teams
- **40% reduction in P2/P3 handling time** → agents focus on complex issues
- **Consistent triage quality** → eliminates human routing errors
- **24/7 availability** → instant ticket processing outside business hours

### For Account Management
- **Proactive churn prevention** → intervene before customers leave
- **Context-rich alerts** → KAMs arrive prepared with full situation
- **Prioritized outreach** → focus on highest-risk accounts first

### For Sales/Revenue
- **Zero missed upsell signals** → every pricing request captured
- **Faster response times** → strike while intent is hot
- **Data-driven expansion** → track commercial signals over time

---

## 🔮 Future Enhancements

### Phase 2 (Next Iteration)
- [ ] Slack integration for alerts (alternative to email)
- [ ] Multi-language support (French, German, Spanish tickets)
- [ ] Customer health score integration (Vitally, ChurnZero APIs)
- [ ] A/B testing framework for response templates

### Phase 3 (Advanced)
- [ ] Predictive escalation (forecast P2→P0 upgrades)
- [ ] Agent performance analytics (resolution time by agent)
- [ ] Self-learning system (feedback loop from agent corrections)
- [ ] Voice-to-text ticket processing (phone support integration)

---

## 📝 Data & Privacy

**Test Data:**
- All customer names, companies, and details are fictional
- No real customer data used in development

**Production Recommendations:**
- GDPR compliance: anonymize/pseudonymize PII before processing
- Data retention: automatically purge logs after 30 days
- Access control: restrict Guardian/Opportunity alerts to authorized roles
- Audit trail: log all automated actions for compliance review

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 👤 Author

**Gaëlle Chevrier**  
Head of Customer Success | Business×Tech×Ops mindset for scalable growth | B2B SaaS Marketing/Commerce Tech | E-commerce ops → CS automation | Remote EU 🇫🇷🇬🇧

Trilingual professional (business-operational-technical) with 20+ years of experience in B2B SaaS Marketing/Commerce Tech, specializing in CS automation and AI-powered workflows.

- **GitHub:** [@gaellecmoi](https://github.com/gaellecmoi)
- **LinkedIn:** [Gaëlle Chevrier](https://www.linkedin.com/in/gchevrier/)
- **Portfolio:** [Notion Portfolio](https://www.notion.so/Portfolio-Ga-lle-Chevrier-2a9b25e936d580d39c47f3a21b230615)
- **Email:** gaelle.chevrier@gmail.com

**Related Projects:**
- [System 1: Data Quality Monitor](https://github.com/gaellechevrier/cs-automation-systeme1)
- [System 2: Campaign Insights Agent](https://github.com/gaellechevrier/cs-automation-systeme2)

---

## 🎬 Video Demo

[Watch 6-minute walkthrough on Loom](YOUR_LOOM_LINK_HERE)

Covers:
- System architecture explanation
- Live triage demonstration
- Dashboard walkthrough
- Email notification showcase
- Production deployment considerations

---

## 🙏 Acknowledgments

- Claude AI: [Anthropic](https://anthropic.com)
- Inspiration: Real-world CS challenges at B2B SaaS scale-ups
- Test methodology: Industry best practices from CS Ops community

---

**Questions or feedback?** Open an issue or reach out on LinkedIn.