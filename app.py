from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime
from pathlib import Path

# Get the absolute path to the .env file
env_path = Path('.') / '.env'
print(f"Loading environment from: {env_path.absolute()}")

app = Flask(__name__)
load_dotenv(env_path)

# API configurations
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# print("Environment variables:")
# print("CLAUDE_API_KEY exists:", bool(CLAUDE_API_KEY))
# print("GOOGLE_MAPS_API_KEY exists:", bool(GOOGLE_MAPS_API_KEY))
# print("GOOGLE_MAPS_API_KEY value:", GOOGLE_MAPS_API_KEY)

def get_nearby_facilities(latitude, longitude, facility_type):
    """Get nearby medical facilities using Google Places API."""
    
    print("Google Maps API Key:", GOOGLE_MAPS_API_KEY)
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    # Determine the type of facility to search for
    if facility_type == "Emergency Room":
        types = "hospital"
        keyword = "emergency"
    else:  # Urgent Care or Primary Care
        types = "doctor"
        keyword = "urgent care"
    
    params = {
        "location": f"{latitude},{longitude}",
        "radius": "5000",  # 5km radius
        "type": types,
        "keyword": keyword,
        "key": GOOGLE_MAPS_API_KEY
    }
    
    try:
        print("Fetching facilities...")
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        print("Facilities fetched:", data)
        
        if data["status"] == "OK":
            facilities = []
            for place in data["results"][:5]:  # Get top 5 results
                facilities.append({
                    "name": place["name"],
                    "address": place.get("vicinity", "Address not available"),
                    "rating": place.get("rating", "No rating available"),
                    "place_id": place["place_id"]
                })
            return facilities
        elif data["status"] == "REQUEST_DENIED":
            print("Error: Google Maps API request denied. Please check your API key configuration.")
            return []
        else:
            print(f"Warning: Google Maps API returned status: {data['status']}")
            return []
    except Exception as e:
        print(f"Error fetching facilities: {str(e)}")
        return []

def get_emergency_guidance(symptoms):
    """Get emergency guidance for high-urgency situations."""
    prompt = f"""You are an emergency medical advisor. For the following symptoms, provide ONLY a JSON response with emergency guidance steps:

Symptoms: {symptoms}

Provide your response in EXACTLY this JSON format, with no other text:
{{
    "emergency_steps": [
        "Step 1 description",
        "Step 2 description",
        ...
    ],
    "do_not_do": [
        "What not to do 1",
        "What not to do 2",
        ...
    ],
    "additional_notes": "Any additional important information"
}}"""

    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    data = {
        "model": "claude-3-opus-20240229",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = requests.post(CLAUDE_API_URL, headers=headers, json=data)
        response.raise_for_status()
        claude_response = response.json()
        content = claude_response['content'][0]['text']
        return json.loads(content)
    except Exception as e:
        print(f"Error getting emergency guidance: {str(e)}")
        return None

def query_claude(symptoms):
    """Query Claude AI to analyze symptoms and provide recommendations."""
    prompt = f"""You are a medical symptom analyzer. Your task is to analyze the following symptoms and provide ONLY a JSON response, with no additional text or explanation before or after the JSON.

Symptoms to analyze: {symptoms}

Provide your response in EXACTLY this JSON format, with no other text:
{{
    "matched_symptoms": [
        {{
            "symptom": "symptom name",
            "urgency": "high/medium/low",
            "recommendation": "Emergency Room/Urgent Care/Primary Care",
            "description": "detailed explanation"
        }}
    ],
    "overall_urgency": "high/medium/low"
}}

Guidelines for analysis:
- High urgency: life-threatening conditions, severe pain, difficulty breathing
- Medium urgency: conditions requiring prompt attention but not immediately life-threatening
- Low urgency: conditions that can wait for regular doctor's appointment
- Emergency Room: for life-threatening conditions
- Urgent Care: for conditions requiring prompt attention
- Primary Care: for non-urgent conditions

Remember: Respond with ONLY the JSON object, no other text."""

    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    data = {
        "model": "claude-3-opus-20240229",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = requests.post(CLAUDE_API_URL, headers=headers, json=data)
        response.raise_for_status()
        claude_response = response.json()
        content = claude_response['content'][0]['text']
        
        print("Symptoms: ", symptoms)
        print("Content: ", content)

        return json.loads(content)
    except Exception as e:
        print(f"Error querying Claude: {str(e)}")
        return {
            "error": "Unable to analyze symptoms at this time. Please try again later."
        }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_symptoms():
    print("Analyzing symptoms...")

    data = request.json
    symptoms = data.get('symptoms', '').lower()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    if not symptoms.strip():
        return jsonify({
            "error": "Please describe your symptoms."
        })
    
    # Get symptom analysis from Claude
    analysis = query_claude(symptoms)
    
    if "error" in analysis:
        return jsonify(analysis)
    print("Location data:", latitude, longitude)
    print("Urgency level:", analysis.get("overall_urgency"))
    print("Will search facilities:", bool(latitude and longitude and analysis["overall_urgency"] in ["high", "medium"]))
    # If location is provided and urgency is high/medium, get nearby facilities
    if latitude and longitude and analysis["overall_urgency"] in ["high", "medium"]:
        facility_type = "Emergency Room" if analysis["overall_urgency"] == "high" else "Urgent Care"
        facilities = get_nearby_facilities(latitude, longitude, facility_type)
        analysis["nearby_facilities"] = facilities
    
    # If urgency is high, get emergency guidance
    if analysis["overall_urgency"] == "high":
        emergency_guidance = get_emergency_guidance(symptoms)
        if emergency_guidance:
            analysis["emergency_guidance"] = emergency_guidance
    
    print("Analysis complete")
    return jsonify(analysis)

if __name__ == '__main__':
    app.run(debug=True) 