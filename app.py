from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import requests
import json

app = Flask(__name__)
load_dotenv()

# Claude AI configuration
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY")

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
        
        # Extract the content from Claude's response
        content = claude_response['content'][0]['text']
        
        print("Symptoms: ", symptoms)
        print("Content: ", content)

        # Parse the JSON response
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Fallback to basic analysis if JSON parsing fails
            return {
                "matched_symptoms": [{
                    "symptom": "General Symptoms",
                    "urgency": "medium",
                    "recommendation": "Urgent Care",
                    "description": "Please consult with a healthcare professional for proper evaluation."
                }],
                "overall_urgency": "medium"
            }
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
    data = request.json
    symptoms = data.get('symptoms', '').lower()
    
    if not symptoms.strip():
        return jsonify({
            "error": "Please describe your symptoms."
        })
    
    # Query Claude AI for analysis
    analysis = query_claude(symptoms)
    
    if "error" in analysis:
        return jsonify(analysis)
    
    return jsonify(analysis)

if __name__ == '__main__':
    app.run(debug=True) 