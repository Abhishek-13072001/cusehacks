"""
Seed data script for OrangeVoice demo.
Run this before demo to reset feedback.json with realistic sample data.
Usage: python seed_data.py
"""

import json
from datetime import datetime, timedelta

# Generate timestamps relative to now
now = datetime.now()
week1 = (now - timedelta(days=7)).isoformat()
week2 = now.isoformat()

seed_data = [
    # ============ IST 615 — Cycle 1 (declining path starts here) ============
    {"course": "IST 615", "feedback": "Azure lab setup was really confusing, I could not finish the setup steps", "cycle": 1, "timestamp": week1, "addressed": False},
    {"course": "IST 615", "feedback": "Azure walkthrough was too fast, got lost during the demo", "cycle": 1, "timestamp": week1, "addressed": False},
    {"course": "IST 615", "feedback": "Lecture on VMs was excellent, very clear examples", "cycle": 1, "timestamp": week1, "addressed": False},
    {"course": "IST 615", "feedback": "Assignment instructions were clear and helpful", "cycle": 1, "timestamp": week1, "addressed": False},
    {"course": "IST 615", "feedback": "I could not set up Azure quotas, no help was given", "cycle": 1, "timestamp": week1, "addressed": False},
    {"course": "IST 615", "feedback": "Professor explains cloud concepts really well", "cycle": 1, "timestamp": week1, "addressed": False},
    {"course": "IST 615", "feedback": "Wish there was a setup video for Azure environment", "cycle": 1, "timestamp": week1, "addressed": False},

    # ============ IST 615 — Cycle 2 (worsened, triggers CRITICAL alert) ============
    {"course": "IST 615", "feedback": "Azure setup is still really confusing even after professor talked about it in class", "cycle": 2, "timestamp": week2, "addressed": False},
    {"course": "IST 615", "feedback": "The lab still does not work for me, no changes felt", "cycle": 2, "timestamp": week2, "addressed": False},
    {"course": "IST 615", "feedback": "I am still lost on Azure quotas, no help received", "cycle": 2, "timestamp": week2, "addressed": False},
    {"course": "IST 615", "feedback": "No improvement at all, still cannot finish the lab", "cycle": 2, "timestamp": week2, "addressed": False},
    {"course": "IST 615", "feedback": "Getting even more frustrated with Azure setup", "cycle": 2, "timestamp": week2, "addressed": False},
    {"course": "IST 615", "feedback": "The pace did not slow down at all, still too fast", "cycle": 2, "timestamp": week2, "addressed": False},

    # ============ IST 688 — Cycle 1 (mixed/mild concerns) ============
    {"course": "IST 688", "feedback": "Streamlit lab was confusing at start", "cycle": 1, "timestamp": week1, "addressed": False},
    {"course": "IST 688", "feedback": "RAG concepts moved too fast", "cycle": 1, "timestamp": week1, "addressed": False},
    {"course": "IST 688", "feedback": "Not clear how to use ChromaDB", "cycle": 1, "timestamp": week1, "addressed": False},
    {"course": "IST 688", "feedback": "Good discussion sessions helped", "cycle": 1, "timestamp": week1, "addressed": False},
    {"course": "IST 688", "feedback": "Assignment 2 was well-structured", "cycle": 1, "timestamp": week1, "addressed": False},
    {"course": "IST 688", "feedback": "Professor is knowledgeable but rushed", "cycle": 1, "timestamp": week1, "addressed": False},

    # ============ IST 688 — Cycle 2 (improved after professor's response) ============
    {"course": "IST 688", "feedback": "RAG walkthrough this week really helped clarify things", "cycle": 2, "timestamp": week2, "addressed": False},
    {"course": "IST 688", "feedback": "ChromaDB tutorial was clear and effective", "cycle": 2, "timestamp": week2, "addressed": False},
    {"course": "IST 688", "feedback": "Loving the new pace of lectures", "cycle": 2, "timestamp": week2, "addressed": False},
    {"course": "IST 688", "feedback": "Professor addressed our concerns well", "cycle": 2, "timestamp": week2, "addressed": False},
    {"course": "IST 688", "feedback": "Great class this week, everything makes sense now", "cycle": 2, "timestamp": week2, "addressed": False},
    {"course": "IST 688", "feedback": "Streamlit lab was much better after the walkthrough", "cycle": 2, "timestamp": week2, "addressed": False},
    {"course": "IST 688", "feedback": "Really appreciate the extra effort to help us learn", "cycle": 2, "timestamp": week2, "addressed": False},
]

with open("data/feedback.json", "w", encoding="utf-8") as f:
    json.dump(seed_data, f, indent=2)

print(f"✅ Seeded {len(seed_data)} feedback entries")
print(f"   • IST 615: 7 (Cycle 1) + 6 (Cycle 2) = 13 entries")
print(f"   • IST 688: 6 (Cycle 1) + 7 (Cycle 2) = 13 entries")
print(f"\n📁 Saved to: data/feedback.json")
print(f"🎯 Ready for demo!")