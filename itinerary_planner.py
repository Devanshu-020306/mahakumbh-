import json

with open('data/events.json', 'r', encoding='utf-8') as f:
    events_data = json.load(f)
with open('data/stays.json', 'r', encoding='utf-8') as f:
    stays_data = json.load(f)

def generate_itinerary(profile):
    age_group = profile.get('age_group')
    interests = profile.get('interests', [])
    budget = profile.get('budget')

    suggested_events = []
    for event in events_data:
        if age_group in event['target_audience'] or any(interest in event.get('type', '').lower() for interest in interests):
            suggested_events.append(event)
    
    if age_group == 'Elderly':
        suggested_events.sort(key=lambda x: (x['type'] != 'Spiritual', x['name'] == "Shahi Snan (Royal Bath)"))

    budget_map = {'Budget': 1, 'Mid-range': 2, 'Luxury': 3}
    price_level = budget_map.get(budget, 1)

    suggested_stays = [
        stay for stay in stays_data 
        if stay['price_level'] == price_level and age_group in stay['suitability']
    ]

    if not suggested_stays:
        suggested_stays = [stay for stay in stays_data if stay['price_level'] == price_level]

    return {
        "suggested_events": suggested_events[:3],
        "suggested_stay": suggested_stays[0] if suggested_stays else None
    }

def find_alternative_event(profile, unsafe_locations):
    """
    Finds a new event suggestion that matches the user's profile
    but is NOT in one of the unsafe locations.
    """
    age_group = profile.get('age_group')
    interests = profile.get('interests', [])
    
    # Also exclude events that are already suggested
    current_event_locations = [event['location'] for event in unsafe_locations]

    for event in events_data:
        is_safe = event['location'] not in unsafe_locations
        is_new = event['location'] not in current_event_locations
        matches_profile = age_group in event['target_audience'] or any(interest in event.get('type', '').lower() for interest in interests)
        
        if is_safe and is_new and matches_profile:
            return event
            
    return None