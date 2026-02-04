# ENS Legis AI Clone OS - Deployment Guide

## 🚀 Quick Start with Docker

The easiest way to deploy the AI Clone OS with the interactive dashboard is using Docker:

```bash
# 1. Clone the repository
git clone https://github.com/lawfullyillegal-droid/ai-clone-os.git
cd ai-clone-os

# 2. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 3. Run deployment script
./deploy.sh
```

The dashboard will be available at: **http://localhost:5000**

---

## 📋 Prerequisites

### Required
- **Docker** (v20.10+) - [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose** (v2.0+) - [Install Docker Compose](https://docs.docker.com/compose/install/)

### Optional (for full functionality)
- **Gmail API Credentials** - For email automation
  - Follow setup instructions below
- **Social Media API Keys** - For future social distribution features

---

## 🔧 Configuration

### 1. Environment Variables

Copy the example environment file and customize:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```bash
# Flask Configuration
FLASK_SECRET_KEY=your-random-secret-key-here
DASHBOARD_HOST=0.0.0.0
DASHBOARD_PORT=5000

# Gmail API (optional but recommended)
GMAIL_CREDENTIALS_PATH=./credentials.json
EMAIL_ADDRESS=your-email@gmail.com

# Other settings...
```

### 2. Gmail API Setup (Optional)

For email automation functionality:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project: "ENS-Legis-Clone-OS"
3. Enable **Gmail API**
4. Create **OAuth 2.0 credentials** (Desktop app)
5. Download credentials as `credentials.json`
6. Place `credentials.json` in the project root

**Note:** The dashboard works without Gmail API, but email processing features will be disabled.

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f dashboard

# Stop services
docker-compose stop

# Restart services
docker-compose restart

# Remove all containers
docker-compose down
```

### Using Docker directly

```bash
# Build image
docker build -t ens-legis-dashboard .

# Run container
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/config:/app/config \
  --name ens-legis-dashboard \
  ens-legis-dashboard
```

---

## 💻 Local Development

For development without Docker:

```bash
# Install dependencies
pip install -r requirements.txt

# Run dashboard
python dashboard.py
```

Dashboard will be available at: http://localhost:5000

---

## 🌐 Production Deployment

### Cloud Platforms

#### Google Cloud Run

```bash
# Build and deploy
gcloud run deploy ens-legis-dashboard \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### AWS ECS / Fargate

```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker tag ens-legis-dashboard:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/ens-legis-dashboard:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/ens-legis-dashboard:latest

# Deploy to ECS (use AWS Console or Terraform)
```

#### Heroku

```bash
# Login and create app
heroku login
heroku create ens-legis-dashboard

# Deploy
git push heroku main
```

### VPS / Dedicated Server

```bash
# Install Docker on server
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Clone and deploy
git clone https://github.com/lawfullyillegal-droid/ai-clone-os.git
cd ai-clone-os
./deploy.sh
```

**Production Checklist:**
- ✅ Set strong `FLASK_SECRET_KEY`
- ✅ Set `FLASK_DEBUG=false`
- ✅ Configure SSL/TLS (use Caddy, Nginx, or Cloudflare)
- ✅ Set up backup for `data/` directory
- ✅ Configure firewall rules
- ✅ Set up monitoring and alerts

---

## 📊 Dashboard Features

### Bot Control Panel
- **Start/Stop** - Control email bot operation
- **Process Now** - Manually trigger email processing
- **Real-time Status** - Monitor bot health and activity

### Surveillance Log Viewer
- **Filter by Category** - Legal, Media, Supporter, Vendor, Unknown
- **Real-time Updates** - Auto-refresh every 5 seconds
- **Search & Export** - Find specific logs and export data

### Statistics Dashboard
- **Email Volume** - Total emails processed
- **Category Breakdown** - Distribution by type
- **Activity Timeline** - Historical trends

### Configuration Management
- **Bot Settings** - Adjust check intervals and limits
- **Template Management** - Update response templates
- **API Configuration** - Manage integrations

---

## 🔐 Security Considerations

### API Keys & Credentials
- Never commit `.env` or `credentials.json` to version control
- Use environment variables in production
- Rotate credentials regularly (quarterly)

### Network Security
- Use HTTPS in production (required for OAuth)
- Restrict dashboard access with firewall rules
- Consider adding authentication middleware

### Data Protection
- Surveillance logs contain sensitive data
- Implement data retention policies
- Back up `data/` directory regularly
- Consider encryption at rest for sensitive logs

---

## 🐛 Troubleshooting

### Dashboard won't start

```bash
# Check logs
docker-compose logs dashboard

# Common issues:
# - Port 5000 already in use: Change DASHBOARD_PORT in .env
# - Permission denied: Run with sudo or fix Docker permissions
```

### Gmail API not working

```bash
# Verify credentials file exists
ls -la credentials.json

# Check environment variable
echo $GMAIL_CREDENTIALS_PATH

# Re-authenticate (if token expired)
# Follow OAuth flow in dashboard
```

### Container keeps restarting

```bash
# Check container status
docker-compose ps

# View detailed logs
docker-compose logs -f dashboard

# Restart from scratch
docker-compose down
docker-compose up --build -d
```

---

## 📈 Monitoring & Maintenance

### Health Checks

The Docker container includes a health check:

```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' ens-legis-dashboard
```

### Log Management

```bash
# View live logs
docker-compose logs -f

# View last 100 lines
docker-compose logs --tail=100

# Export logs to file
docker-compose logs > logs.txt
```

### Updates

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up --build -d
```

---

## 🆘 Support

- **GitHub Issues**: [Report bugs](https://github.com/lawfullyillegal-droid/ai-clone-os/issues)
- **Documentation**: [Full README](../README.md)
- **Email**: travisryle@gmail.com
- **Campaign Website**: [lawfully-illegal.com](https://lawfully-illegal.com)

---

## 📜 License

This project is licensed under the MIT License - see LICENSE file for details.
