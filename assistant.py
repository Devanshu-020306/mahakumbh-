QA_PAIRS = {
    "shahi snan": "The next Shahi Snan is on the main festival day at Triveni Sangam, starting at 4 AM. It will be very crowded.",
    "ghat": "The nearest major ghat is Har Ki Pauri. It is approximately 2 km from the main camp area.",
    "food": "Free community kitchens (Bhandaras) are available near most ashrams. For restaurants, check the main market road.",
    "emergency": "For any emergency, please dial 112 or visit the nearest police help desk. They are located at every sector entrance.",
    "help": "You can ask me about 'Shahi Snan', the nearest 'ghat', 'food', or 'emergency' services."
}

def answer_question(query):
    query_lower = query.lower()
    for keyword, answer in QA_PAIRS.items():
        if keyword in query_lower:
            return answer
    
    return "I'm sorry, I can only answer questions about: Shahi Snan, ghat, food, and emergency. Please type 'help' for options."