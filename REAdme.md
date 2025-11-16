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

### Technical Routing Layer (3 Specialized Agents)

**Nexus** - Integrations & APIs  
Handles platform integrations (Shopify, WooCommerce, BigCommerce), webhook issues, authentication, and API errors.

**Cipher** - Data & Analytics  
Manages tracking issues, event synchronization, data quality, performance optimization, and analytics pipeline problems.

**Sentinel** - Compliance & Operations  
Covers payment processing, security, GDPR compliance, infrastructure, and operational workflows.

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
Agent Routing (Nexus/Cipher/Sentinel)
    ↓
Intelligence Analysis (parallel)
    ├─→ Guardian Layer → Churn risk? → Alert KAM
    └─→ Opportunity Layer → Revenue signal? → Alert Sales
    ↓
Action Execution
    ├─→ P2/P3: Generate draft response
    ├─→ P0/P1: Route to agent
    ├─→ Guardian alerts: Send email to KAM
    └─→ Opportunity alerts: Send email to Sales
    ↓
Output Generation
    ├─→ HTML Dashboard (visual report)
    ├─→ JSON Logs (API integration preview)
    └─→ Email Notifications (real-time alerts)
```

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

## 🎬 Video Demo

[Watch 6-minute walkthrough on Loom](YOUR_LOOM_LINK_HERE)

Covers:
- System architecture explanation
- Live triage demonstration
- Dashboard walkthrough
- Email notification showcase
- Production deployment considerations

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
Head of Customer Success | CS Operations & Automation Specialist

- GitHub: [@gaellechevrier](https://github.com/gaellechevrier)
- LinkedIn: [Gaëlle Chevrier](https://linkedin.com/in/gaellechevrier)
- Email: gaelle.chevrier@gmail.com

**Related Projects:**
- [System 1: Data Quality Monitor](https://github.com/gaellechevrier/cs-automation-systeme1)
- [System 2: Campaign Insights Agent](https://github.com/gaellechevrier/cs-automation-systeme2)

---

## 🙏 Acknowledgments

- Claude AI: [Anthropic](https://anthropic.com)
- Inspiration: Real-world CS challenges at B2B SaaS scale-ups
- Test methodology: Industry best practices from CS Ops community

---

**Questions or feedback?** Open an issue or reach out on LinkedIn.