#!/usr/bin/env python3
# /// script
# dependencies = [
# "mcp",
# "requests",
# ]
# ///
import requests
import os
from datetime import datetime

from mcp.server.fastmcp import FastMCP

app = FastMCP("luna-mcp")

FEEDING_TYPES = {
    "BREASTFEEDING_RIGHT_NIPPLE",
    "BABY_BOTTLE",
    "BREASTFEEDING_LEFT_NIPPLE",
    "BREASTFEEDING_BOTH_NIPPLE",
}

BATH_TYPE = "BATH"
DIAPERCHANGE_PEE_TYPE = "DIAPERCHANGE_PEE"
DIAPERCHANGE_POO_TYPE = "DIAPERCHANGE_POO"


def get_logbook_url():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                if not 'json' in line:
                    return line + '/lunatracker_logbook.json'
                return line
    raise ValueError("URL not found in .env")


def download_logbook():
    url = get_logbook_url()
    response = requests.get(url)
    return response.json()


def upload_logbook(events):
    url = get_logbook_url()
    response = requests.put(url, json=events)
    response.raise_for_status()


def format_last_event(last_event, not_found_message):
    if not last_event:
        return not_found_message
    dt = datetime.fromtimestamp(last_event["time"])
    now = datetime.now()
    elapsed = now - dt
    hours = int(elapsed.total_seconds() // 3600)
    minutes = int((elapsed.total_seconds() % 3600) // 60)
    return f"{dt.strftime('%A, %B %-d, %H:%M')}\n{hours} hours and {minutes} minutes ago"


@app.tool()
def last_feeding() -> str:
    """Returns the last time the baby got fed as a human-readable date"""
    events = download_logbook()
    feeding_events = [e for e in events if e.get("type") in FEEDING_TYPES]
    if not feeding_events:
        return "No feeding events found"
    last_event = max(feeding_events, key=lambda e: e.get("time", 0))
    return format_last_event(last_event, "No feeding events found")


@app.tool()
def last_bath() -> str:
    """Returns the last time the baby had a bath as a human-readable date"""
    events = download_logbook()
    bath_events = [e for e in events if e.get("type") == BATH_TYPE]
    if not bath_events:
        return "No bath events found"
    last_event = max(bath_events, key=lambda e: e.get("time", 0))
    return format_last_event(last_event, "No bath events found")


@app.tool()
def last_diaper() -> str:
    """Returns the last diaper change as a human-readable date"""
    events = download_logbook()
    diaper_events = [e for e in events if e.get("type") in (DIAPERCHANGE_PEE_TYPE, DIAPERCHANGE_POO_TYPE)]
    if not diaper_events:
        return "No diaper events found"
    last_event = max(diaper_events, key=lambda e: e.get("time", 0))
    return format_last_event(last_event, "No diaper events found")


@app.tool()
def add_bath() -> str:
    """Adds a bath event to the logbook"""
    events = download_logbook()
    new_event = {
        "time": int(datetime.now().timestamp()),
        "type": BATH_TYPE,
        "signature": "voice"
    }
    events.append(new_event)
    events.sort(key=lambda e: e.get("time", 0), reverse=True)
    upload_logbook(events)
    return "Bath added successfully"


@app.tool()
def add_pee() -> str:
    """Adds a pee diaper change event to the logbook"""
    events = download_logbook()
    new_event = {
        "time": int(datetime.now().timestamp()),
        "type": DIAPERCHANGE_PEE_TYPE,
        "signature": "voice"
    }
    events.append(new_event)
    events.sort(key=lambda e: e.get("time", 0), reverse=True)
    upload_logbook(events)
    return "Pee diaper added successfully"


@app.tool()
def add_poo() -> str:
    """Adds a poo diaper change event to the logbook"""
    events = download_logbook()
    new_event = {
        "time": int(datetime.now().timestamp()),
        "type": DIAPERCHANGE_POO_TYPE,
        "signature": "voice"
    }
    events.append(new_event)
    events.sort(key=lambda e: e.get("time", 0), reverse=True)
    upload_logbook(events)
    return "Poo diaper added successfully"

if __name__ == "__main__":
    print(last_feeding())
    print()
    print(last_bath())
    print()
    print(last_diaper())
