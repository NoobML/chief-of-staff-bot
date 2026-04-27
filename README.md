# 🤖 Chief of Staff Bot

An AI-powered WhatsApp bot that acts as your personal Chief of Staff — tracking tasks, following up automatically, and alerting you when things go wrong.

Built by [NoobML](https://github.com/NoobML)

---

## What it does

- **Reads** WhatsApp messages and detects task assignments
- **Saves** tasks (assignee, deadline, status) to Google Sheets
- **Follows up** automatically when deadlines pass
- **Alerts** the CEO instantly when someone flags a blocker
- **Sends** a daily digest of all active tasks every morning

---

## Tech Stack

- **Python** + FastAPI
- **AI**: Groq (free) / Claude / OpenAI / Gemini — swap with one config change
- **WhatsApp**: Twilio
- **Storage**: Google Sheets
- **Scheduler**: APScheduler

---

## Quick Start

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
# Fill in your values in .env
```

### 4. Add Google credentials
- Follow [Google Sheets Setup Guide](docs/setup-google-sheets.md)
- Place `credentials.json` in the project folder

### 5. Run setup
```bash
python setup.py
```
This automatically creates all required Google Sheet tabs.

### 6. Start the bot
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 7. Connect Twilio webhook
Set your Twilio WhatsApp sandbox webhook to:
```
http://your-server-ip:8000/webhook
```

---

## AI Provider Setup

| Provider | Cost | Get Key |
|---|---|---|
| **Groq** | Free | [console.groq.com](https://console.groq.com) |
| **Claude** | ~$6-9/month | [console.anthropic.com](https://console.anthropic.com) |
| **OpenAI** | Pay per use | [platform.openai.com](https://platform.openai.com) |
| **Gemini** | Free tier | [aistudio.google.com](https://aistudio.google.com) |

Set `AI_PROVIDER` in `.env` to switch providers instantly.

---

## Google Sheets Structure

The bot uses 4 tabs:

| Tab | Purpose |
|---|---|
| **Tasks** | All assigned tasks with status |
| **Roster** | Team members and their details |
| **Updates Log** | Full history of all updates |
| **Settings** | Bot behavior configuration |

---

## Configuration

All settings in `.env` — no code changes needed:

```bash
BOT_TONE=professional        # professional, casual, friendly
FOLLOWUP_DELAY_HOURS=24      # hours before first follow-up
MAX_FOLLOWUPS=3              # max reminders before CEO escalation
DAILY_DIGEST_TIME=09:00      # when to send morning summary
ALERT_CEO_ON_BLOCKER=true    # ping CEO when blocker flagged
```

---

## License

MIT — free to use, modify and distribute.
