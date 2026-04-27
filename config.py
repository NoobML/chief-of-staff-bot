import os
from dotenv import load_dotenv

load_dotenv()

# ── AI Provider ───────────────────────────────────────────────────────────────
# Options: "groq", "claude", "openai", "gemini"
AI_PROVIDER = os.getenv("AI_PROVIDER", "groq")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ── Twilio ────────────────────────────────────────────────────────────────────
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

# ── Google Sheets ─────────────────────────────────────────────────────────────
GOOGLE_SHEETS_ID = os.getenv("GOOGLE_SHEETS_ID")
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")

# ── CEO / Admin ───────────────────────────────────────────────────────────────
CEO_WHATSAPP = os.getenv("CEO_WHATSAPP")
CEO_PRIVATE_GROUP = os.getenv("CEO_PRIVATE_GROUP", os.getenv("CEO_WHATSAPP"))

# ── WhatsApp Group Map ────────────────────────────────────────────────────────
# Map your WhatsApp group/sandbox numbers to readable names
# Format: "whatsapp:+1234567890": "Team Name"
# Add as many groups as needed
GROUP_MAP = {
    group.strip(): name.strip()
    for group, name in (
        pair.split("=", 1)
        for pair in os.getenv("GROUP_MAP", "").split(",")
        if "=" in pair
    )
}

# ── Bot Behavior ──────────────────────────────────────────────────────────────
# All configurable without touching code
BOT_SETTINGS = {
    "followup_delay_hours": int(os.getenv("FOLLOWUP_DELAY_HOURS", "24")),
    "max_followups": int(os.getenv("MAX_FOLLOWUPS", "3")),
    "tone": os.getenv("BOT_TONE", "professional"),
    "language": os.getenv("BOT_LANGUAGE", "english"),
    "alert_ceo_on_blocker": os.getenv("ALERT_CEO_ON_BLOCKER", "true").lower() == "true",
    "daily_digest_time": os.getenv("DAILY_DIGEST_TIME", "09:00"),
    "followup_time": os.getenv("FOLLOWUP_TIME", "10:00"),
}
