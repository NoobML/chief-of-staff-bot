<div align="center">

# 🤖 Chief of Staff Bot

**An AI-powered WhatsApp bot that manages your team's tasks automatically.**

Assign tasks in WhatsApp → Bot saves them → Follows up when overdue → Alerts you on blockers.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136+-red.svg)](https://fastapi.tiangolo.com)

Built by [NoobML](https://github.com/NoobML)

</div>

---

## 🎯 The Problem

As a CEO or manager, you assign tasks across multiple WhatsApp groups every day. You forget who was assigned what. Deadlines pass. No one follows up. Things fall through the cracks.

**Chief of Staff Bot fixes this.**

---

## ✨ What it does

- 📥 **Reads** every message in your WhatsApp groups
- 🧠 **Detects** task assignments, updates, and blockers using AI
- 📊 **Saves** tasks to Google Sheets automatically
- ⏰ **Follows up** when deadlines pass — without you lifting a finger
- 🚨 **Alerts** you instantly when someone flags a blocker
- 📋 **Sends** a daily digest of all active tasks every morning

---

## 🔄 How it works

```
You send a WhatsApp message:
"John, please build the landing page by Friday"
         ↓
Bot reads the message
         ↓
AI extracts: Task + Assignee + Deadline
         ↓
Saved to Google Sheets
         ↓
Friday arrives, no update from John?
         ↓
Bot sends: "@John — landing page due today, any update?"
         ↓
John replies: "There's an issue with hosting"
         ↓
Bot alerts you: "🚨 Blocker flagged by John — hosting issue"
```

---

## 🛠 Tech Stack

| Component | Technology |
|---|---|
| **Backend** | Python + FastAPI |
| **AI** | Groq / Claude / OpenAI / Gemini |
| **WhatsApp** | Twilio |
| **Storage** | Google Sheets |
| **Scheduler** | APScheduler |

---

## 📋 Prerequisites

Before you start, make sure you have:

- Python 3.10+
- A [Twilio account](https://twilio.com) (free sandbox available)
- A [Google account](https://google.com) (for Sheets)
- An AI provider key — [Groq](https://console.groq.com) is free and recommended

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/NoobML/chief-of-staff-bot
cd chief-of-staff-bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
pip install groq
```

### 3. Configure environment
```bash
cp .env.example .env
```
Fill in your values in `.env` — see [Configuration](#-configuration) below.

### 4. Add Google credentials
- Go to [Google Cloud Console](https://console.cloud.google.com)
- Create a project → Enable **Google Sheets API** + **Google Drive API**
- Create a **Service Account** → Download `credentials.json`
- Place `credentials.json` in the project folder
- Share your Google Sheet with the service account email

### 5. Run setup
```bash
python setup.py
```
This automatically creates all required Google Sheet tabs with correct headers.

### 6. Start the bot
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 7. Connect Twilio webhook
In Twilio → Messaging → WhatsApp Sandbox → set webhook to:
```
http://your-server-ip:8000/webhook
```

---

## 🤖 AI Provider Setup

Pick one — swap anytime by changing `AI_PROVIDER` in `.env`:

| Provider | Cost | Speed | Get Key |
|---|---|---|---|
| **Groq** ⭐ | Free | Very fast | [console.groq.com](https://console.groq.com) |
| **Claude** | ~$6-9/month | Fast | [console.anthropic.com](https://console.anthropic.com) |
| **OpenAI** | Pay per use | Fast | [platform.openai.com](https://platform.openai.com) |
| **Gemini** | Free tier | Fast | [aistudio.google.com](https://aistudio.google.com) |

> ⭐ We recommend Groq for getting started — it's free and very fast.

---

## ⚙️ Configuration

All settings in `.env` — no code changes needed:

```bash
# Switch AI provider instantly
AI_PROVIDER=groq

# Bot personality
BOT_TONE=professional        # professional | casual | friendly
BOT_LANGUAGE=english

# Follow-up behavior
FOLLOWUP_DELAY_HOURS=24      # hours before first follow-up
MAX_FOLLOWUPS=3              # max reminders before CEO escalation
FOLLOWUP_TIME=10:00          # time to check for overdue tasks

# Daily digest
DAILY_DIGEST_TIME=09:00      # morning summary time

# Alerts
ALERT_CEO_ON_BLOCKER=true    # ping CEO when blocker flagged

# Map your WhatsApp groups to readable names
GROUP_MAP=whatsapp:+14155238886=Dev Group,whatsapp:+0987654321=Marketing
```

---

## 📊 Google Sheets Structure

The bot uses 4 tabs (created automatically by `setup.py`):

| Tab | Purpose |
|---|---|
| **Tasks** | All assigned tasks with status tracking |
| **Roster** | Team members, roles, and contact info |
| **Updates Log** | Full history of every update and action |
| **Settings** | Bot behavior key-value configuration |

---

## 🔧 Troubleshooting

**Bot not receiving messages?**
- Check ngrok/server is running and webhook URL is updated in Twilio

**AI not extracting tasks correctly?**
- Make sure `AI_PROVIDER` matches your API key in `.env`

**Google Sheets connection failing?**
- Confirm `credentials.json` is in project root
- Confirm sheet is shared with service account email

**Twilio error "same To and From"?**
- Update `CEO_WHATSAPP` in `.env` to your personal WhatsApp number

---

## 📁 Project Structure

```
chief-of-staff-bot/
├── main.py            # FastAPI app + webhook handler
├── ai_extractor.py    # AI provider abstraction (Groq/Claude/OpenAI/Gemini)
├── sheets.py          # Google Sheets read/write operations
├── scheduler.py       # Follow-up and digest scheduler
├── whatsapp.py        # Twilio message sender
├── config.py          # All configuration loaded from .env
├── setup.py           # One-time Google Sheet setup script
├── requirements.txt   # Python dependencies
└── .env.example       # Environment variable template
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Open an issue for bugs or feature requests
- Submit a pull request
- Star the repo if it helped you ⭐

---

## 📄 License

MIT — free to use, modify and distribute.

