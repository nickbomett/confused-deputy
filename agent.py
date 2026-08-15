import requests
import json
import uuid
from datetime import datetime, timezone


SESSION_ID = str(uuid.uuid4())


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
    
    
    