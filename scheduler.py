from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import sheets
import whatsapp
import ai_extractor
import config


def check_followups():
    """Run daily — check overdue tasks and send follow-up reminders."""
    print(f"[Scheduler] Checking overdue tasks at {datetime.now()}")
    overdue = sheets.get_overdue_tasks()

    for task in overdue:
        count = sheets.increment_followup_count(task["ID"])
        max_followups = config.BOT_SETTINGS["max_followups"]

        if count <= max_followups:
            # Send reminder to the group
            message = ai_extractor.generate_followup_message(task, attempt=count)
            whatsapp.send_to_group(task["Group"], message)
            sheets.log_update(task["ID"], f"Follow-up #{count} sent", "bot")
            print(f"[Scheduler] Follow-up #{count} sent for task {task['ID']}")
        else:
            # Escalate to CEO
            whatsapp.alert_ceo(
                f"Task *{task['Task']}* assigned to *{task['Assignee']}* "
                f"has had {count} follow-ups with no response.\n"
                f"Deadline was: {task['Deadline']}\n"
                f"Consider taking action."
            )
            sheets.log_update(task["ID"], "Escalated to CEO", "bot")


def send_daily_digest():
    """Send CEO a morning summary of all active tasks."""
    tasks = sheets.get_all_active_tasks()
    if not tasks:
        return

    lines = ["📋 *Daily Task Digest*\n"]
    for t in tasks:
        status_emoji = {"Pending": "⏳", "In Progress": "🔄", "Blocked": "🔴"}.get(t["Status"], "•")
        lines.append(f"{status_emoji} *{t['Task']}*\n   → {t['Assignee']} | Due: {t['Deadline']} | {t['Status']}\n")

    whatsapp.alert_ceo("\n".join(lines))
    print(f"[Scheduler] Daily digest sent — {len(tasks)} active tasks")


def start_scheduler():
    scheduler = BackgroundScheduler()

    # Follow-ups: daily at 10am
    scheduler.add_job(check_followups, "cron", hour=10, minute=0)

    # Digest: daily at configured time
    digest_time = config.BOT_SETTINGS["daily_digest_time"].split(":")
    scheduler.add_job(send_daily_digest, "cron",
                      hour=int(digest_time[0]),
                      minute=int(digest_time[1]))

    scheduler.start()
    print("[Scheduler] Started — follow-ups at 10:00, digest at", config.BOT_SETTINGS["daily_digest_time"])
    return scheduler