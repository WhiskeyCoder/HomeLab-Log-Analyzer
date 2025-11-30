# 📦 Setup Guide

This guide will walk you through setting up the Home Lab Log Analyzer from scratch.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Methods](#installation-methods)
  - [Method 1: Docker Compose (Recommended)](#method-1-docker-compose-recommended)
  - [Method 2: Standalone Python](#method-2-standalone-python)
- [LM Studio Setup](#lm-studio-setup)
- [N8N Integration](#n8n-integration)
- [Email Configuration](#email-configuration)
- [First Run](#first-run)

---

## Prerequisites

### Required

- **Docker & Docker Compose**: For running the analyzer
  ```bash
  # Check if installed
  docker --version
  docker-compose --version
  ```

- **LM Studio**: For running the local LLM
  - Download from [lmstudio.ai](https://lmstudio.ai/)
  - Supports Windows, macOS, and Linux

### Optional

- **N8N**: For automation (can use cron instead)
- **SMTP Server**: For email delivery (Gmail, SendGrid, etc.)

### Hardware Recommendations

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 2 cores | 4+ cores |
| RAM | 4 GB | 8+ GB |
| Storage | 10 GB | 20+ GB |
| GPU | None | Any (for faster LLM) |

---

## Installation Methods

### Method 1: Docker Compose (Recommended)

This is the easiest and most portable method.

#### Step 1: Clone the Repository

```bash
git clone https://github.com/WhiskeyCoder/homelab-log-analyzer.git
cd homelab-log-analyzer
```

#### Step 2: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit with your settings
nano .env
```

**Important settings to change:**

```env
# LM Studio Configuration
LM_STUDIO_URL=http://host.docker.internal:1234/v1/completions  # For Docker
LM_STUDIO_MODEL=qwen2.5-1.5b-instruct

# Email Configuration (if using direct email)
EMAIL_TO=your-email@example.com
EMAIL_FROM=homelab@example.com
```

**Note**: Use `host.docker.internal` instead of `localhost` when running in Docker to access LM Studio on the host machine.

#### Step 3: Build and Start

```bash
# Build the image
docker-compose build

# Start the service
docker-compose up -d

# Check logs
docker logs -f log-analyzer
```

#### Step 4: Verify Installation

```bash
# Health check
curl http://localhost:8765/health

# Expected response:
# {
#   "status": "healthy",
#   "service": "log-analyzer",
#   "docker": "connected",
#   "timestamp": "2024-01-01T12:00:00"
# }
```

---

### Method 2: Standalone Python

If you prefer to run without Docker:

#### Step 1: Install Python Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 2: Run the Application

```bash
# Start the API server
python log_analyzer.py
```

The API will be available at `http://localhost:8765`.

---

## LM Studio Setup

LM Studio provides the local LLM inference. Here's how to set it up:

### Step 1: Install LM Studio

1. Download from [lmstudio.ai](https://lmstudio.ai/)
2. Install for your operating system
3. Launch LM Studio

### Step 2: Download a Model

We recommend these models for log analysis:

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| Qwen 2.5 1.5B Instruct | ~1 GB | ⚡⚡⚡ | ⭐⭐ | Fast daily summaries |
| Phi-3 Mini 4K | ~2.3 GB | ⚡⚡ | ⭐⭐⭐ | Balanced performance |
| Llama 3.2 3B Instruct | ~2 GB | ⚡⚡ | ⭐⭐⭐ | Best quality |

**To download:**

1. Click the **Search** icon in LM Studio
2. Search for model name (e.g., "qwen2.5-1.5b-instruct")
3. Click **Download**
4. Wait for download to complete

### Step 3: Load the Model

1. Go to **Chat** tab
2. Select your downloaded model from dropdown
3. Click **Load Model**

### Step 4: Start Local Server

1. Go to **Local Server** tab
2. Click **Start Server**
3. Server will start on `http://localhost:1234`
4. Leave LM Studio running

### Step 5: Test the Server

```bash
# Test if server is responding
curl http://localhost:1234/v1/models

# Should return:
# {
#   "data": [
#     {
#       "id": "qwen2.5-1.5b-instruct",
#       ...
#     }
#   ]
# }
```

---

## N8N Integration

N8N provides powerful workflow automation.

### Installation

```bash
# Using Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# Or using npm
npm install n8n -g
n8n start
```

### Import Workflow

1. Access N8N at `http://localhost:5678`
2. Click **Workflows** → **Import from File**
3. Select `n8n_workflow.json` from this repo
4. Update the HTTP Request node URL:
   - Change `YOUR_SERVER_IP` to your actual IP
   - Example: `http://192.168.1.100:8765/analyze`

### Configure SMTP

1. Click on the **Send Email** node
2. Click **Create New Credential**
3. Enter your SMTP details:

**Gmail Example:**
```
Host: smtp.gmail.com
Port: 587
User: your-email@gmail.com
Password: your-app-password  # Generate in Google Account settings
```

**SendGrid Example:**
```
Host: smtp.sendgrid.net
Port: 587
User: apikey
Password: YOUR_SENDGRID_API_KEY
```

### Activate Workflow

1. Click the **Active** toggle in top-right
2. Workflow will now run daily at 22:00

---

## Email Configuration

### Option 1: Gmail

1. Enable 2-Factor Authentication in your Google Account
2. Generate an App Password:
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Click **2-Step Verification** → **App passwords**
   - Generate password for "Mail"
3. Use this password in your `.env` or N8N credentials

### Option 2: SendGrid

1. Sign up at [sendgrid.com](https://sendgrid.com/)
2. Create an API key
3. Use these settings:
   ```env
   SMTP_HOST=smtp.sendgrid.net
   SMTP_PORT=587
   SMTP_USER=apikey
   SMTP_PASSWORD=YOUR_API_KEY
   ```

### Option 3: Self-Hosted (Postfix)

If you run your own mail server:

```env
SMTP_HOST=localhost
SMTP_PORT=25
SMTP_USER=
SMTP_PASSWORD=
```

---

## First Run

### Manual Test

Trigger your first analysis manually to verify everything works:

```bash
curl -X POST http://localhost:8765/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "hours": 24,
    "lm_studio_url": "http://localhost:1234/v1/completions",
    "model": "qwen2.5-1.5b-instruct"
  }' | jq
```

**Expected output:**
```json
{
  "timestamp": "2024-01-01T12:00:00",
  "summary": {
    "critical_issues": [],
    "warnings": [],
    "successes": ["All containers running normally"],
    "recommendations": [],
    "container_status": {
      "plex": "Healthy",
      "nginx": "Healthy"
    },
    "overall_health": "healthy"
  },
  "containers_analyzed": 2,
  "issues_found": 0
}
```

### Scheduled Automation

#### Using N8N

1. Workflow runs automatically at 22:00 daily
2. Check N8N executions log for status
3. Email should arrive within 2-3 minutes

#### Using Cron (Alternative)

If not using N8N, set up a cron job:

```bash
# Edit crontab
crontab -e

# Add this line (runs at 22:00 daily)
0 22 * * * curl -X POST http://localhost:8765/analyze -H "Content-Type: application/json" -d '{"hours": 24}' | mail -s "Home Lab Report" your-email@example.com
```

---

## Verification Checklist

Before running in production, verify:

- [ ] Docker container is running: `docker ps | grep log-analyzer`
- [ ] API is healthy: `curl http://localhost:8765/health`
- [ ] LM Studio server is running: `curl http://localhost:1234/v1/models`
- [ ] Can list containers: `curl http://localhost:8765/containers`
- [ ] Manual analysis works: Test with curl command above
- [ ] Email delivery works (if using N8N or cron)

---

## Next Steps

- [Choose and optimize your LLM model](models.md)
- [Customize log filtering and prompts](../README.md#advanced-usage)
- [Troubleshoot common issues](troubleshooting.md)

---

## Quick Troubleshooting

**Container won't start?**
```bash
# Check logs
docker logs log-analyzer

# Common fix: Docker socket permission
sudo chmod 666 /var/run/docker.sock
```

**Can't connect to LM Studio?**
- Use `host.docker.internal:1234` in Docker
- Use `localhost:1234` for standalone Python
- Ensure LM Studio local server is running

**No logs found?**
- Ensure Docker containers are running
- Check that `/var/run/docker.sock` is mounted
- Try analyzing specific containers by name

For more help, see [Troubleshooting Guide](troubleshooting.md).
