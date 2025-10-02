import json

with open('data/events.json', 'r', encoding='utf-8') as f:
    events_data = json.load(f)
KNOWN_LOCATIONS = list(set([event['location'] for event in events_data]))

SAFETY_KEYWORDS = [
    'stampede', 'fire', 'unsafe', 'danger', 'emergency', 'crush', 'chaos', 'riot'
]
MISSING_PERSON_KEYWORDS = [
    'missing', 'lost', 'can\'t find', 'separated', 'child lost'
]

def analyze_post(text):
    text_lower = text.lower()
    
    alert_location = None
    for loc in KNOWN_LOCATIONS:
        if loc.lower() in text_lower:
            alert_location = loc
            break

    found_safety_keywords = [kw for kw in SAFETY_KEYWORDS if kw in text_lower]
    if found_safety_keywords:
        return {
            "status": "ALERT",
            "type": "High-Priority Safety Alert",
            "message": "Immediate attention required. Potential danger detected.",
            "flagged_keywords": found_safety_keywords,
            "location": alert_location
        }
    
    found_missing_keywords = [kw for kw in MISSING_PERSON_KEYWORDS if kw in text_lower]
    if found_missing_keywords:
        return {
            "status": "ALERT",
            "type": "Missing Person Report",
            "message": "A potential missing person report has been flagged.",
            "flagged_keywords": found_missing_keywords,
            "location": alert_location
        }
        
    return {
        "status": "Normal",
        "type": "General Feedback",
        "message": "Community feed is clear. No immediate threats detected.",
        "flagged_keywords": [],
        "location": None
    }