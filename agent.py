import requests
import json
import uuid
from datetime import datetime, timezone


SESSION_ID = str(uuid.uuid4())


def build_system_prompt() -> str:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return f"""You are an assistant with access to two tools.

Today's date is {today}.

Tool: get_calendar_events
Description: Returns the events on the user's calendar for a given date.
Arguments: date (string, format YYYY-MM-DD)

Tool: get_emails
Description: Returns the user's recent emails.
Arguments: none

You must respond with exactly one of these two JSON formats, and nothing else — no explanation, no text before or after the JSON.

To call a tool:
{{"type": "tool_call", "name": "<tool name>", "args": {{...}}}}

To give your final answer:
{{"type": "final_answer", "content": "your answer here"}}
"""


def log_event(event_type: str, data: dict):
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": SESSION_ID,
        "event_type": event_type,
        "data": data,
    }
    with open("agent_log.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")
        
        
def call_model(messages: list) -> str:
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "qwen2.5:7b-instruct",
        "messages": messages,
        "stream": False,
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["message"]["content"]


def get_calendar_events(date: str) -> list:
    return [
        {"time": "10.00", "title": "Team standup"},
        {"time": "14:00", "title": "Dentist appointment"},
    ]
   

def get_emails() -> list:
    return [
        {"from": "manager@company.com", "subject": "Q3 planning", "body": "Let's sync on Q3 planning next week."},
        {"from": "hr@company.com", "subject": "Benefits enrollment", "body": "Reminder: benefits enrollment closes this Friday."},
    ]

   
def parse_response(text: str) -> dict:
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return {"type": "parse_error", "raw": text}

    if parsed.get("type") == "tool_call":
        return {"type": "tool_call", "name": parsed.get("name"), "args": parsed.get("args", {})}
    elif parsed.get("type") == "final_answer":
        return {"type": "final_answer", "content": parsed.get("content")}
    else:
        return {"type": "parse_error", "raw": text}   
    
     
TOOLS = {
    "get_calendar_events": get_calendar_events,
    "get_emails": get_emails,
}


def agent_loop(user_input: str, max_turns: int = 5):
    log_event("user_input", {"content": user_input})
    messages = [
        {"role": "system", "content": build_system_prompt()},
        {"role": "user", "content": user_input},
    ]

    for turn in range(max_turns):
        reply = call_model(messages)
        result = parse_response(reply)

        if result["type"] == "tool_call":
            log_event("tool_call", {"name": result["name"], "args": result["args"]})

            tool_function = TOOLS.get(result["name"])
            if tool_function:
                tool_result = tool_function(**result["args"])
            else:
                tool_result = {"error": f"Unknown tool: {result['name']}"}

            log_event("tool_result", {"name": result["name"], "result": tool_result})

            messages.append({"role": "assistant", "content": reply})
            messages.append({"role": "user", "content": f"Tool result: {json.dumps(tool_result)}"})

        elif result["type"] == "final_answer":
            log_event("final_answer", {"content": result["content"]})
            return result["content"]

        else:
            log_event("parse_error", {"raw": result["raw"]})
            return "Error: could not parse model's response."

    log_event("max_turns_exceeded", {})
    return "Error: exceeded maximum number of turns without a final answer."



    
    