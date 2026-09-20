import json
import os
from datetime import datetime

DATA_FILE = "data/feedback.json"

def load_feedback():
    """Load all feedback from JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_feedback(course_code, feedback_text, cycle=1):
    """Append a new feedback entry."""
    entries = load_feedback()
    new_entry = {
        "course": course_code.upper().strip(),
        "feedback": feedback_text.strip(),
        "cycle": cycle,
        "timestamp": datetime.now().isoformat(),
        "addressed": False
    }
    entries.append(new_entry)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)
    return new_entry

def get_feedback_for_course(course_code, cycle=None):
    """Get all feedback for a specific course, optionally filtered by cycle."""
    entries = load_feedback()
    filtered = [e for e in entries if e["course"] == course_code.upper().strip()]
    if cycle is not None:
        filtered = [e for e in filtered if e.get("cycle", 1) == cycle]
    return filtered

def get_all_courses():
    """Return list of unique course codes with feedback."""
    entries = load_feedback()
    return sorted(list(set(e["course"] for e in entries)))