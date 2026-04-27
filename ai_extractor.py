import json
import config

SYSTEM_PROMPT = """
You are a task extraction assistant for a CEO managing multiple companies.
Given a WhatsApp message, extract structured task information.

Return ONLY a JSON object with this exact structure:
{
  "is_task": true/false,
  "is_update": true/false,
  "is_blocker": true/false,
  "task": "task description or null",
  "assignee": "person name or null",
  "deadline": "YYYY-MM-DD or null",
  "related_to": "what existing task this update relates to, or null",
  "blocker_reason": "reason for blocker or null",
  "summary": "one line summary of what happened"
}

Rules:
- is_task: true if CEO is assigning something to someone
- is_update: true if someone is giving a progress update
- is_blocker: true if someone mentions a problem, issue, or being stuck
- assignee: extract the person's name being assigned the task
- deadline: infer from words like "by Friday", "tomorrow", "end of week"
- related_to: if this is an update, what task/topic does it relate to
"""


def extract_task(message: str, sender: str, group_name: str) -> dict:
    user_prompt = f"""
Group: {group_name}
Sender: {sender}
Message: {message}

Extract task information from this message.
"""
    if config.AI_PROVIDER == "groq":
        return _extract_with_groq(user_prompt)
    elif config.AI_PROVIDER == "gemini":
        return _extract_with_gemini(user_prompt)
    elif config.AI_PROVIDER == "claude":
        return _extract_with_claude(user_prompt)
    elif config.AI_PROVIDER == "openai":
        return _extract_with_openai(user_prompt)
    else:
        raise ValueError(f"Unknown AI provider: {config.AI_PROVIDER}")


def _extract_with_groq(user_prompt: str) -> dict:
    from groq import Groq
    client = Groq(api_key=config.GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=500,
    )
    text = response.choices[0].message.content.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)


def _extract_with_gemini(user_prompt: str) -> dict:
    from google import genai
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"{SYSTEM_PROMPT}\n\n{user_prompt}"
    )
    text = response.text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(text)


def _extract_with_claude(user_prompt: str) -> dict:
    import anthropic
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}]
    )
    return json.loads(response.content[0].text)


def _extract_with_openai(user_prompt: str) -> dict:
    from openai import OpenAI
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=500,
    )
    return json.loads(response.choices[0].message.content)


def generate_followup_message(task: dict, attempt: int) -> str:
    prompt = f"""
Generate a WhatsApp follow-up message for an overdue task.
Tone: {config.BOT_SETTINGS["tone"]}
Attempt number: {attempt} (be more urgent if attempt > 1)
Task: {task['Task']}
Assigned to: {task['Assignee']}
Deadline was: {task['Deadline']}

Keep it short, 1-2 sentences. Start with @{task['Assignee']}.
Return only the message text, nothing else.
"""
    if config.AI_PROVIDER == "groq":
        from groq import Groq
        client = Groq(api_key=config.GROQ_API_KEY)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
        )
        return response.choices[0].message.content.strip()
    elif config.AI_PROVIDER == "gemini":
        from google import genai
        client = genai.Client(api_key=config.GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text.strip()
    elif config.AI_PROVIDER == "claude":
        import anthropic
        client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    elif config.AI_PROVIDER == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=config.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
        )
        return response.choices[0].message.content