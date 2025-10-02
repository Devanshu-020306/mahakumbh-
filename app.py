from flask import Flask, request, jsonify, render_template
from ai_core.itinerary_planner import generate_itinerary, find_alternative_event
from ai_core.navigation import get_route_suggestion
from ai_core.assistant import answer_question
from ai_core.safety_monitor import analyze_post

app = Flask(__name__)

@app.route('/')
def index():
    """Render the main demo page."""
    return render_template('index.html')

@app.route('/api/get_recommendations', methods=['POST'])
def get_recommendations():
    """
    The main API endpoint that powers all the AI features.
    """
    try:
        data = request.json
        profile = {
            'age_group': data.get('age_group'),
            'interests': data.get('interests', []),
            'budget': data.get('budget')
        }

        # 1. Initial Itinerary Generation
        itinerary = generate_itinerary(profile)

        # 2. Safety Monitoring (Run this before finalizing itinerary)
        community_post = data.get('community_post', '')
        safety_analysis = analyze_post(community_post) if community_post else {
            "status": "Normal", "message": "No community post submitted."
        }
        
        # 3. Dynamic Re-scheduling Logic (AI Safety Override)
        itinerary_update = None
        if safety_analysis.get('status') == 'ALERT' and safety_analysis.get('location'):
            unsafe_location = safety_analysis['location']
            original_events = list(itinerary['suggested_events']) 
            itinerary['suggested_events'] = [
                event for event in itinerary['suggested_events'] if event['location'] != unsafe_location
            ]
            
            if len(itinerary['suggested_events']) < len(original_events):
                alternative = find_alternative_event(profile, [unsafe_location])
                if alternative:
                    itinerary['suggested_events'].append(alternative)
                    itinerary_update = {
                        "unsafe_location": unsafe_location,
                        "new_suggestion": alternative
                    }

        # 4. Crowd Navigation (based on the potentially updated itinerary)
        first_event_location = itinerary['suggested_events'][0]['location'] if itinerary['suggested_events'] else "Mela Grounds"
        navigation_suggestion = get_route_suggestion(first_event_location)

        # 5. Q&A Assistant
        user_question = data.get('question', '')
        assistant_response = answer_question(user_question) if user_question else "Ask me a question to get help."

        # Compile the final response
        response = {
            "itinerary": itinerary,
            "navigation": navigation_suggestion,
            "assistant": { "user_question": user_question, "answer": assistant_response },
            "safety_analysis": safety_analysis,
            "itinerary_update": itinerary_update
        }
        return jsonify(response)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)