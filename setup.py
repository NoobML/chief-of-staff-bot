"""
Chief of Staff Bot — One-time setup script
Run this once to prepare your Google Sheet automatically.
"""

import sys
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SHEETS_CONFIG = {
    "Tasks": {
        "headers": [
            "ID", "Task", "Assignee", "Group", "Deadline",
            "Status", "Message", "AssignedBy", "CreatedAt",
            "LastUpdated", "Followups"
        ],
        "sample": [
            "SAMPLE01", "Build landing page", "John", "Dev Group",
            "2026-05-01", "Pending", "John please build the landing page by Friday",
            "CEO", "2026-04-27 09:00", "2026-04-27 09:00", "0"
        ]
    },
    "Roster": {
        "headers": ["Name", "WhatsApp", "Role", "Company", "Branch"],
        "sample": ["John", "+923001234567", "Web Developer", "IT Co", "Development"]
    },
    "Updates Log": {
        "headers": ["TaskID", "Update", "By", "Timestamp"],
        "sample": ["SAMPLE01", "Task created", "CEO", "2026-04-27 09:00"]
    },
    "Settings": {
        "headers": ["Key", "Value"],
        "sample": ["followup_delay_hours", "24"]
    }
}


def print_step(msg):
    print(f"\n→ {msg}")


def print_ok(msg):
    print(f" {msg}")


def print_err(msg):
    print(f"  {msg}")


def connect_sheets():
    creds_file = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
    sheet_id = os.getenv("GOOGLE_SHEETS_ID")

    if not sheet_id:
        print_err("GOOGLE_SHEETS_ID not found in .env")
        sys.exit(1)

    if not os.path.exists(creds_file):
        print_err(f"credentials.json not found. Make sure it's in the project folder.")
        sys.exit(1)

    creds = Credentials.from_service_account_file(creds_file, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id)
    print_ok(f"Connected to Google Sheet: '{sheet.title}'")
    return sheet


def setup_tabs(sheet):
    existing_tabs = [ws.title for ws in sheet.worksheets()]

    for tab_name, config in SHEETS_CONFIG.items():
        print_step(f"Setting up '{tab_name}' tab...")

        if tab_name in existing_tabs:
            ws = sheet.worksheet(tab_name)
            print_ok(f"Tab already exists — skipping creation")
        else:
            ws = sheet.add_worksheet(title=tab_name, rows=1000, cols=20)
            print_ok(f"Tab created")

        # Set headers in row 1
        existing_headers = ws.row_values(1)
        if existing_headers != config["headers"]:
            ws.update("A1", [config["headers"]])
            print_ok(f"Headers set: {config['headers']}")
        else:
            print_ok(f"Headers already correct")

        # Add sample row if sheet is empty
        all_values = ws.get_all_values()
        if len(all_values) <= 1:
            ws.append_row(config["sample"])
            print_ok(f"Sample row added")
        else:
            print_ok(f"Data already exists — skipping sample row")

    # Remove default Sheet1 if it exists and is empty
    if "Sheet1" in existing_tabs:
        try:
            ws = sheet.worksheet("Sheet1")
            if ws.get_all_values() == []:
                sheet.del_worksheet(ws)
                print_ok("Removed empty default 'Sheet1'")
        except Exception:
            pass


def verify_env():
    print_step("Checking .env configuration...")
    required = ["GOOGLE_SHEETS_ID", "GOOGLE_CREDENTIALS_FILE"]
    optional = {
        "AI_PROVIDER": "groq",
        "GROQ_API_KEY": None,
        "ANTHROPIC_API_KEY": None,
        "OPENAI_API_KEY": None,
        "GEMINI_API_KEY": None,
        "TWILIO_ACCOUNT_SID": None,
        "TWILIO_AUTH_TOKEN": None,
        "TWILIO_WHATSAPP_NUMBER": None,
        "CEO_WHATSAPP": None,
    }

    all_good = True
    for key in required:
        val = os.getenv(key)
        if val:
            print_ok(f"{key} is set")
        else:
            print_err(f"{key} is MISSING — required!")
            all_good = False

    for key in optional:
        val = os.getenv(key)
        if val:
            print_ok(f"{key} is set")
        else:
            print(f"  {key} not set (optional)")

    return all_good


def main():
    print("\n" + "="*50)
    print("  Chief of Staff Bot — Setup")
    print("="*50)

    # Step 1: Check env
    env_ok = verify_env()
    if not env_ok:
        print("\n Fix missing required variables in .env and run again.")
        sys.exit(1)

    # Step 2: Connect to Sheets
    print_step("Connecting to Google Sheets...")
    sheet = connect_sheets()

    # Step 3: Setup tabs
    print_step("Setting up sheet tabs...")
    setup_tabs(sheet)

    # Done
    print("\n" + "="*50)
    print("  Setup complete!")
    print("="*50)
    print("\nNext step: run the bot with:")
    print("  uvicorn main:app --host 0.0.0.0 --port 8000\n")


if __name__ == "__main__":
    main()
