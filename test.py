import config
from groq import Groq
import gspread
from google.oauth2.service_account import Credentials

# ── Test 1: Groq ──────────────────────────────
print("Testing Groq...")
client = Groq(api_key=config.GROQ_API_KEY)
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Say hello in one word"}],
    max_tokens=10
)
print(f"✅ Groq works: {response.choices[0].message.content.strip()}")

# ── Test 2: Google Sheets ─────────────────────
print("\nTesting Google Sheets...")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(config.GOOGLE_CREDENTIALS_FILE, scopes=SCOPES)
gs_client = gspread.authorize(creds)
sheet = gs_client.open_by_key(config.GOOGLE_SHEETS_ID)
print(f"✅ Sheets works: connected to '{sheet.title}'")
print(f"   Tabs: {[ws.title for ws in sheet.worksheets()]}")