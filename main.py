from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
import ai_extractor
import sheets
import whatsapp
import scheduler
import config

app = FastAPI(title="Chief of Staff Bot")


@app.on_event("startup")
def on_startup():
    scheduler.start_scheduler()
    print("[App] Chief of Staff Bot is running.")


@app.post("/webhook", response_class=PlainTextResponse)
async def whatsapp_webhook(
    Body: str = Form(...),
    From: str = Form(...),
    To: str = Form(...),
    ProfileName: str = Form("")
):
    # Clean up sender name
    sender = ProfileName if ProfileName and ProfileName not in ["", "Ok?"] else From
    group_name = config.GROUP_MAP.get(To, To)

    print(f"[Webhook] {sender} in {group_name}: {Body[:80]}")

    # Extract task info via AI
    extracted = ai_extractor.extract_task(
        message=Body,
        sender=sender,
        group_name=group_name
    )
    print(f"[AI] {extracted.get('summary', 'no summary')}")

    # ── Task assigned ─────────────────────────────────────────────────────────
    if extracted.get("is_task") and extracted.get("assignee"):
        task_id = sheets.save_task(
            extracted, sender=sender, group=To, raw_message=Body
        )
        sheets.log_update(task_id, "Task created", sender)
        whatsapp.send_message(
            config.CEO_WHATSAPP,
            f"✅ *Task saved!*\n"
            f"*{extracted['task']}*\n"
            f"→ Assignee: {extracted['assignee']}\n"
            f"→ Deadline: {extracted.get('deadline', 'not set')}\n"
            f"→ ID: #{task_id}"
        )

    # ── Blocker flagged ───────────────────────────────────────────────────────
    elif extracted.get("is_blocker"):
        related = _find_related_task(extracted.get("related_to"), sender)
        if related:
            sheets.update_task_status(related["ID"], "Blocked", Body)
            sheets.log_update(related["ID"], f"Blocked: {extracted.get('blocker_reason', Body)}", sender)

        if config.BOT_SETTINGS["alert_ceo_on_blocker"]:
            whatsapp.alert_ceo(
                f"🔴 *Blocker flagged* in {group_name}\n\n"
                f"By: {sender}\n"
                f"Issue: {extracted.get('blocker_reason', Body)}\n"
                f"Related to: {extracted.get('related_to', 'unknown task')}"
            )

    # ── Progress update ───────────────────────────────────────────────────────
    elif extracted.get("is_update"):
        related = _find_related_task(extracted.get("related_to"), sender)
        if related:
            sheets.update_task_status(related["ID"], "In Progress")
            sheets.log_update(related["ID"], Body, sender)
            print(f"[App] Update logged for task {related['ID']}")

    return "OK"


@app.get("/health")
def health():
    return {"status": "running", "ai_provider": config.AI_PROVIDER}


def _find_related_task(related_to: str | None, assignee: str) -> dict | None:
    if not related_to:
        return None
    tasks = sheets.get_all_active_tasks()
    for task in tasks:
        if (related_to and related_to.lower() in task["Task"].lower()) or \
           task["Assignee"].lower() == assignee.lower():
            return task
    return None
