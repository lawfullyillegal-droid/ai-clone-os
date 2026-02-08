# 🚀 Quick Start Guide - ENS Legis AI Clone OS Dashboard

## Get Started in 3 Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/lawfullyillegal-droid/ai-clone-os.git
cd ai-clone-os
```

### Step 2: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your favorite editor
nano .env  # or vim, code, etc.
```

**Minimum Configuration:**
```bash
FLASK_SECRET_KEY=your-random-secret-key
DASHBOARD_HOST=0.0.0.0
DASHBOARD_PORT=5000
```

### Step 3: Deploy

#### Option A: Docker (Recommended)

```bash
# One command to deploy everything
./deploy.sh
```

Dashboard will be available at: **http://localhost:5000**

#### Option B: Local Python

```bash
# Install dependencies
pip install -r requirements.txt

# Run dashboard
python dashboard.py
```

---

## 📸 Dashboard Preview

![ENS Legis Dashboard](https://github.com/user-attachments/assets/a4e3b379-dcc8-48c8-8ae1-7e630c3b8636)

---

## 🎛️ Dashboard Features

### Bot Control
- **Start Bot** - Begin automated email processing
- **Stop Bot** - Pause email processing
- **Process Now** - Manually trigger email check

### Monitoring
- **Real-time Status** - See bot health and activity
- **Surveillance Logs** - View all processed emails
- **Statistics** - Email volume and category breakdown

### Filters & Search
- Filter logs by category (Legal, Media, Supporter, etc.)
- Adjust result limits
- Export logs for analysis

---

## 🔧 Optional: Gmail API Setup

For full email processing functionality:

1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create project: "ENS-Legis-Clone-OS"
3. Enable **Gmail API**
4. Create **OAuth 2.0 credentials** (Desktop app)
5. Download as `credentials.json` → place in project root

**Note:** Dashboard works without Gmail API, but email features will be disabled.

---

## 📚 Useful Commands

### Docker Management
```bash
# View logs
docker-compose logs -f dashboard

# Restart services
docker-compose restart

# Stop services
docker-compose stop

# Remove everything
docker-compose down
```

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python -m unittest discover tests

# Start dashboard
python dashboard.py
```

---

## 🆘 Troubleshooting

### Dashboard won't start
```bash
# Check if port 5000 is in use
lsof -i :5000

# Use different port
DASHBOARD_PORT=8080 python dashboard.py
```

### Docker issues
```bash
# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Module not found errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 📖 Full Documentation

- **Complete Guide**: [DEPLOYMENT.md](./DEPLOYMENT.md)
- **Main README**: [README.md](./README.md)
- **GitHub Repo**: [lawfullyillegal-droid/ai-clone-os](https://github.com/lawfullyillegal-droid/ai-clone-os)

---

## 💡 Next Steps

1. ✅ Deploy the dashboard
2. 🔧 Configure Gmail API (optional)
3. 📊 Monitor email processing
4. 📝 Customize response templates
5. 🚀 Scale to production

---

**Questions?** Open an issue on GitHub or email travisryle@gmail.com
