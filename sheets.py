import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import uuid
import config

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_sheet():
    creds = Credentials.from_service_account_file(config.GOOGLE_CREDENTIALS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open_by_key(config.GOOGLE_SHEETS_ID)


# ── Tasks ─────────────────────────────────────────────────────────────────────

def save_task(extracted: dict, sender: str, group: str, raw_message: str) -> str:
    """Save a new task to the Tasks sheet. Returns task ID."""
    sheet = get_sheet().worksheet("Tasks")
    task_id = str(uuid.uuid4())[:8].upper()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    row = [
        task_id,
        extracted.get("task", ""),
        extracted.get("assignee", ""),
        group,                              # company/group detected from group name
        extracted.get("deadline", ""),
        "Pending",                          # status
        raw_message,                        # original message
        sender,                             # assigned by
        now,                                # created at
        now,                                # last updated
        "0",                                # follow-up count
    ]
    sheet.append_row(row)
    print(f"[Sheets] Task saved: {task_id} → {extracted.get('task')}")
    return task_id


def update_task_status(task_id: str, status: str, update_note: str = ""):
    """Update a task's status and last-updated timestamp."""
    sheet = get_sheet().worksheet("Tasks")
    records = sheet.get_all_records()

    for i, row in enumerate(records, start=2):  # row 1 is header
        if row["ID"] == task_id:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            sheet.update_cell(i, 6, status)       # Status column
            sheet.update_cell(i, 10, now)          # Last Updated column
            if update_note:
                sheet.update_cell(i, 7, update_note)
            print(f"[Sheets] Task {task_id} → {status}")
            return


def get_overdue_tasks() -> list:
    """Get all pending tasks past their deadline."""
    sheet = get_sheet().worksheet("Tasks")
    records = sheet.get_all_records()
    today = datetime.now().date()
    overdue = []

    for row in records:
        if row["Status"] in ("Pending", "In Progress") and row["Deadline"]:
            try:
                deadline = datetime.strptime(row["Deadline"], "%Y-%m-%d").date()
                if deadline < today:
                    overdue.append(row)
            except ValueError:
                pass  # skip rows with unparseable dates
    return overdue


def increment_followup_count(task_id: str) -> int:
    """Increment follow-up counter and return new count."""
    sheet = get_sheet().worksheet("Tasks")
    records = sheet.get_all_records()

    for i, row in enumerate(records, start=2):
        if row["ID"] == task_id:
            count = int(row.get("Followups", 0)) + 1
            sheet.update_cell(i, 11, str(count))
            return count
    return 0


# ── Roster ────────────────────────────────────────────────────────────────────

def get_roster() -> list:
    """Get all team members and their details."""
    sheet = get_sheet().worksheet("Roster")
    return sheet.get_all_records()


def get_member_by_name(name: str) -> dict | None:
    """Find a team member by name (case-insensitive)."""
    roster = get_roster()
    for member in roster:
        if member["Name"].lower() == name.lower():
            return member
    return None


# ── Update Log ────────────────────────────────────────────────────────────────

def log_update(task_id: str, update: str, by: str):
    """Log any update/event for a task."""
    sheet = get_sheet().worksheet("Updates Log")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    sheet.append_row([task_id, update, by, now])


# ── Daily Digest ──────────────────────────────────────────────────────────────

def get_all_active_tasks() -> list:
    """Get all non-completed tasks for the daily digest."""
    sheet = get_sheet().worksheet("Tasks")
    records = sheet.get_all_records()
    return [r for r in records if r["Status"] not in ("Done", "Cancelled")]