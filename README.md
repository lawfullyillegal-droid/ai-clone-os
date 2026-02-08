# AI Clone OS
## ENS Legis Digital Clone - Incrimination Nation Campaign

**Multi-platform AI agent orchestration for campaign management, legal automation, surveillance logging, and content distribution**

---

## 🎯 Overview

This repository contains the **ENS Legis Digital Clone Operating System**, a comprehensive automation framework for running the Incrimination Nation campaign across multiple platforms. The system orchestrates AI agents to handle:

- **Email Management**: Automated categorization, template responses, and surveillance logging
- **Social Media**: Multi-platform content scheduling and engagement
- **Legal Automation**: Document assembly for FCRA complaints, preservation demands, and FOIA requests
- **Surveillance & Analytics**: Evidence logging, docket monitoring, and analytics tracking
- **Content Distribution**: YouTube uploads, blog posts, and merchandise promotions
- **Interactive Dashboard**: Web-based control panel for monitoring and operating the AI clone

---

## 📁 Repository Structure

```
ai-clone-os/
├── bots/                    # Agent implementations
│   ├── email_bot.py         # Email categorization & auto-response
│   ├── social_bot.py        # Multi-platform social posting (TODO)
│   ├── legal_bot.py         # Document assembly (TODO)
│   └── surveillance_bot.py  # Analytics & logging (TODO)
│
├── config/                  # Configuration files
│   ├── persona/             # ENS Legis master persona prompt
│   │   └── ens-legis-master-prompt.md
│   ├── email_config.json    # Email bot settings (TODO)
│   ├── social_config.json   # Social media credentials (TODO)
│   └── media_list.csv       # Known media outlet domains (TODO)
│
├── templates/               # Response templates
│   ├── email/               # Email templates
│   │   ├── FCRA-Initial-Guidance.txt
│   │   ├── Media-Inquiry-Response.txt
│   │   └── Thank-You-Patron.txt
│   ├── legal/               # Legal document templates (TODO)
│   │   ├── FCRA-Complaint-Template.docx
│   │   └── Preservation-Demand-Template.docx
│   └── dashboard.html       # Interactive dashboard UI
│
├── data/                    # Evidence & logs (gitignored)
│   ├── surveillance_log.json
│   └── evidence_ledger/
│
├── dashboard.py             # Interactive web dashboard (NEW)
├── deploy.sh                # Deployment script (NEW)
├── Dockerfile               # Docker container definition (NEW)
├── docker-compose.yml       # Docker Compose configuration (NEW)
├── .env.example             # Environment variables template (NEW)
├── DEPLOYMENT.md            # Deployment guide (NEW)
│
└── README.md                # This file
```

---

## 🚀 Quick Start

### Deploy with Interactive Dashboard (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/lawfullyillegal-droid/ai-clone-os.git
cd ai-clone-os

# 2. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 3. Deploy with Docker
./deploy.sh
```

Dashboard will be available at: **http://localhost:5000**

### Prerequisites

- **Docker** and **Docker Compose** (for dashboard deployment)
- Python 3.9+ (for local development)
- Gmail account with API access enabled (optional, for email features)
- Google Cloud Project with Gmail API enabled (optional)
- (Optional) Social media API credentials (Twitter, LinkedIn, Facebook)

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/lawfullyillegal-droid/ai-clone-os.git
cd ai-clone-os

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
python dashboard.py
```

### Configuration

#### Gmail API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project: "ENS-Legis-Clone-OS"
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download credentials as `credentials.json` and place in project root
6. Run first-time authentication:
   ```bash
   python scripts/setup_credentials.py
   ```

#### Environment Variables

```bash
export GMAIL_CREDENTIALS_PATH="./credentials.json"
export SURVEILLANCE_LOG_PATH="./data/surveillance_log.json"
```

---

## 🖥 Interactive Dashboard

**Status**: ✅ Implemented

A web-based control panel for monitoring and operating the AI Clone OS:

**Features**:
- Real-time bot status monitoring
- Start/Stop email bot with one click
- Surveillance log viewer with filtering
- Email processing statistics and charts
- Manual email processing trigger
- Configuration management interface

**Access**: http://localhost:5000 (after deployment)

**Usage**:
```bash
# Start dashboard with Docker
./deploy.sh

# Or run directly
python dashboard.py
```

For detailed deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md)

---

## 🤖 Components

### 1. Email Bot (`bots/email_bot.py`)

**Status**: ✅ Implemented

Automated email processing with:
- Categorization based on keywords and sender domains
- Template-based auto-responses
- Surveillance logging for all inbound inquiries
- SHA-256 hashing for evidence chain of custody

**Usage**:
```bash
python bots/email_bot.py
```

**Categories**:
- **Legal**: FCRA inquiries → `FCRA-Initial-Guidance` template
- **Media**: Journalist inquiries → `Media-Inquiry-Response` template
- **Supporter**: Patreon/support messages → `Thank-You-Patron` template
- **Vendor**: Billing/payment notifications
- **Unknown**: Requires manual review

### 2. Social Bot (`bots/social_bot.py`)

**Status**: 🚧 TODO

Multi-platform social media posting:
- Twitter/X, LinkedIn, Facebook integration
- Content calendar scheduling
- Cross-platform promotion
- Engagement tracking

### 3. Legal Bot (`bots/legal_bot.py`)

**Status**: 🚧 TODO

Automated legal document assembly:
- FCRA violation complaints (15 U.S.C. § 1681)
- FRCP 37(e) preservation demands
- FOIA records requests
- Evidence exhibit merging

### 4. Surveillance Bot (`bots/surveillance_bot.py`)

**Status**: 🚧 TODO

Analytics and anomaly detection:
- Webador (lawfully-illegal.com) traffic monitoring
- Suspicious access pattern detection
- Automated incident reporting
- Evidence hash verification

---

## 📋 ENS Legis Persona

All agents operate under the **ENS Legis** digital persona, defined in [`config/persona/ens-legis-master-prompt.md`](./config/persona/ens-legis-master-prompt.md).

**Key Identity Parameters**:
- **Entity**: ENS Legis (Campaign Coordinator)
- **Campaign**: Incrimination Nation
- **Principal**: Travis Ryle (ultimate authority)
- **Authority**: Routine operations autonomous, strategic decisions require principal review
- **Signature**: "ENS Legis, Campaign Coordinator, Incrimination Nation"

**Core Constraints**:
1. **No Fabrication**: All claims must be evidence-backed
2. **No Unauthorized Practice**: Legal information, not legal advice
3. **Privacy Protection**: Redact PII before public disclosure
4. **Transparency**: Disclose AI/automation nature
5. **Good Faith**: Every action serves campaign mission

---

## 🔐 Security & Privacy

### Credential Management

- **Never commit credentials to git**
- Store API keys in environment variables or secure vaults
- Use OAuth 2.0 for Google APIs
- Rotate credentials quarterly

### Evidence Chain of Custody

- All evidence SHA-256 hashed at collection
- Surveillance log entries cryptographically signed
- Redundant storage: GitHub + local + print archive for critical evidence

### PII Redaction

- Third-party PII redacted before public disclosure
- Litigation evidence under seal stays confidential
- GDPR/CCPA compliance in data handling

---

## 📊 Surveillance Log Format

All bot actions logged to `data/surveillance_log.json` in this format:

```json
{
  "incident_id": "SL-2026-0114-001",
  "timestamp": "2026-01-14T18:00:00Z",
  "source": "email|social|webador|github",
  "event_type": "inbound_email|suspicious_access|content_posted",
  "category": "Legal|Media|Supporter|Vendor",
  "details": {
    "from": "sender@example.com",
    "subject": "FCRA Inquiry",
    "action_taken": "auto_response_sent"
  },
  "evidence_hash": "a3f5b8c2d1e4f6"
}
```

---

## 🎓 Deployment

### Development (Local)

```bash
# Run email bot once
python bots/email_bot.py

# Run as scheduled job (every 15 minutes)
watch -n 900 python bots/email_bot.py
```

### Production (Server)

**Option 1: Systemd Service** (Linux)

```bash
# Create service file: /etc/systemd/system/ens-legis-email.service
sudo systemctl enable ens-legis-email
sudo systemctl start ens-legis-email
```

**Option 2: Docker** (Cross-platform)

```bash
docker build -t ens-legis-clone .
docker run -d --env-file .env ens-legis-clone
```

**Option 3: Cloud Functions** (Serverless)

- Deploy to Google Cloud Functions
- Trigger on Pub/Sub schedule (every 15 min)
- Auto-scale based on email volume

---

## 🛠 Development

### Adding a New Bot

1. Create new file in `bots/` directory
2. Implement core methods: `__init__()`, `process()`, `log_action()`
3. Reference ENS Legis persona prompt for tone/authority
4. Log all actions to surveillance database
5. Add tests and documentation

### Adding a New Template

1. Create template file in `templates/email/` or `templates/legal/`
2. Use placeholder syntax: `{{recipient_name}}`, `{{case_number}}`
3. Test template rendering with sample data
4. Update bot configuration to reference new template

---

## 📝 Task Ticket Format

All agents accept standardized JSON task tickets:

```json
{
  "task_id": "TASK-2026-0114-001",
  "type": "email_response|social_post|legal_doc|surveillance_alert",
  "priority": "low|medium|high|urgent",
  "payload": {
    "to": "example@example.com",
    "template": "FCRA-Initial-Guidance",
    "variables": {"recipient_name": "John Doe"},
    "attachments": ["FCRA-Violation-Checklist.pdf"]
  },
  "requires_approval": false,
  "log_to": "surveillance_db"
}
```

---

## 🔗 Platform Integrations

### Currently Integrated
- ✅ Gmail (via Gmail API)

### Planned Integrations
- 🚧 Twitter/X API
- 🚧 LinkedIn API
- 🚧 Facebook Graph API
- 🚧 YouTube Data API
- 🚧 Webador CMS
- 🚧 Printful API
- 🚧 Patreon API
- 🚧 Stripe Webhooks
- 🚧 Google Analytics
- 🚧 GitHub API (already using for repo hosting)

---

## 📚 Additional Resources

- **Campaign Website**: [lawfully-illegal.com](https://lawfully-illegal.com)
- **ENS Legis Persona Prompt**: [`config/persona/ens-legis-master-prompt.md`](./config/persona/ens-legis-master-prompt.md)
- **FCRA Reference**: [15 U.S.C. § 1681](https://www.law.cornell.edu/uscode/text/15/chapter-41/subchapter-III)
- **FRCP 37(e)**: [Federal Rules of Civil Procedure](https://www.law.cornell.edu/rules/frcp/rule_37)

---

## ⚠ Legal Disclaimers

1. **Not Legal Advice**: This system provides legal information, not legal advice. Always consult licensed attorneys for specific legal matters.
2. **Automation Disclosure**: All communications clearly disclose ENS Legis is an AI/automation system.
3. **Evidence Integrity**: Maintain proper chain of custody for all evidence; this system is a tool, not a replacement for legal standards.
4. **Compliance**: User responsible for ensuring all bot actions comply with platform ToS, GDPR, CCPA, and applicable laws.

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🙌 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Follow existing code style and ENS Legis persona constraints
4. Add tests for new functionality
5. Update documentation
6. Submit pull request

---

## 📞 Contact

**Principal**: Travis Ryle  
**Email**: travisryle@gmail.com  
**Campaign**: Incrimination Nation  
**Website**: [lawfully-illegal.com](https://lawfully-illegal.com)

---

**Last Updated**: 2026-01-14  
**Version**: 1.0.0  
**Status**: Active Development
