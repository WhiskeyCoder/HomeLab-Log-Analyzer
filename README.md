# 🧠 HomeLab Log Analyzer — Zero-Noise, AI-Powered Daily Summaries  
A fully-local, fully-automated system that turns your chaotic Docker logs into clean, structured, actionable data... every night... powered by your own local LLM.

No cloud.  
No API fees.  
No bullshit.  
Just *pure self-hosted magic* ✨

---

## 🚀 What This Project Does
This tool automatically:

- Collects logs from all (or selected) Docker containers  
- Removes noise, health-checks, pings, spam, repeat lines  
- Feeds the cleaned logs into **your local LLM** via LM Studio  
- Generates a structured **JSON summary** of critical issues, warnings, successes, anomalies, and recommendations  
- Sends you a **daily email report** via N8N  
- Runs 100% offline, on your own hardware

Think of it as your homelab’s private Network God.

Original Reddit Post - [https://www.reddit.com/r/homelab/comments/1p9f82c/this_is_a_good_use_of_an_llm/](https://www.reddit.com/r/homelab/comments/1p9f82c/this_is_a_good_use_of_an_llm/)

Reddit Post of Release - [https://www.reddit.com/r/homelab/comments/1pa8d94/i_built_the_full_local_llm_logsummarizer_system/](https://www.reddit.com/r/homelab/comments/1pa8d94/i_built_the_full_local_llm_logsummarizer_system/)


---

## 🏗️ How It Works
```
┌─────────────┐      ┌────────────────┐      ┌──────────────┐      ┌──────────┐
│   N8N       │─────▶│  FastAPI App   │─────▶│  LM Studio   │─────▶│  Email   │
│ (Scheduler) │      │ (Log Analyzer) │      │ (Local LLM)  │      │ Delivery │
└─────────────┘      └────────────────┘      └──────────────┘      └──────────┘
      22:00               ↓                        ↓
                     Pull Logs             Summarize in JSON
                     Filter Noise          Return Clean Insights
```

**N8N triggers ➜ Python FastAPI pulls & filters logs ➜ LM Studio analyzes ➜ N8N emails results.**

![N8N Dashboard](https://raw.githubusercontent.com/WhiskeyCoder/HomeLab-Log-Analyzer/refs/heads/main/images/n8n.png)


---

## ✨ Features at a Glance
- 🐳 **Docker log ingestion** (auto or per-container)
- 🧹 **Noise-filtering engine** (health checks, ping/pong, heartbeats, empty lines, etc.)
- 🤖 **Local LLM analysis** (Qwen, Phi-3, Llama, anything LM Studio supports)
- 📦 **Structured JSON output**
- 🔔 **Daily summary email**
- 🔒 **100% private & offline**
- ⚡ **Lightweight — runs on a mini-PC or NUC**
- 🔁 **Plug-and-play with N8N automation**

---

## 🔧 Included in This Repository
- `log_analyzer.py` — Complete FastAPI backend  
- `n8n_workflow.json` — Drop-in N8N daily summary workflow  
- `docker-compose.yml` — One-command deployment  
- `Dockerfile` — Containerized API  
- `requirements.txt` — All dependencies  
- `quickstart.sh` — Setup in under 60 seconds  
- Comprehensive documentation:  
  - `docs/setup.md`  
  - `docs/models.md`  
  - `docs/troubleshooting.md`  
  - `docs/api.md`  
  - `docs/architecture.md`

---

## 🧪 Example Output (JSON)
```json
{
  "critical_issues": ["Container 'db' restarted unexpectedly"],
  "warnings": ["High memory usage in 'plex'"],
  "successes": ["Backup completed in 'nextcloud'"],
  "recommendations": [
    "Investigate container restarts",
    "Review memory allocation"
  ],
  "container_status": {
    "db": "2 restarts detected",
    "plex": "Memory warning"
  },
  "overall_health": "degraded"
}
```

---

## 🛠️ Installation
```bash
git clone https://github.com/WhiskeyCoder/homelab-log-analyzer
cd homelab-log-analyzer
python log_analyzer.py
```

---

## 🤖 Why Local LLM?
Because it’s:

- **Free** (no API bills)  
- **Fast** (sub-second inference on small models)  
- **Private** (no logs leaving your machine)  
- **Customizable** (your prompt, your workflow)

Models supported:  
- Qwen  
- Phi-3  
- Llama  
- Anything LM Studio can serve

---

## 📨 Example Daily Email
- 🔴 Critical Issues  
- ⚠️ Warnings  
- ✅ Successes  
- 💡 Recommendations  
- 📊 Per-container status  
- 🟢 Overall homelab health

Beautiful HTML formatting included.

![Email Sample](https://raw.githubusercontent.com/WhiskeyCoder/HomeLab-Log-Analyzer/refs/heads/main/images/email.png)

---

## 🤝 Contribute
PRs welcome.  
New noise-filters, better prompts, new N8N flows — bring them on.

---

## 📜 License
MIT — use it, break it, improve it, ship it.

---

If your homelab produces logs, this tool turns them into clarity.

Give your servers a voice.  
