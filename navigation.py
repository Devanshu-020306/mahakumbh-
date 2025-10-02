import json

with open('data/crowd_data.json', 'r', encoding='utf-8') as f:
    crowd_data = json.load(f)

def get_route_suggestion(destination_name):
    for location, data in crowd_data.items():
        if location.lower() in destination_name.lower():
            return {
                "destination": location,
                "crowd_info": data
            }
    
    return {
        "destination": destination_name,
        "crowd_info": {
            "crowd_level": "Unknown",
            "message": "No real-time crowd data available for this location.",
            "alternative_route": "Please follow standard navigation."
        }
    }