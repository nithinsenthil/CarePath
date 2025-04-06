from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import requests

app = Flask(__name__)
load_dotenv()

# Basic symptom database
SYMPTOM_DATABASE = {
    "chest pain": {
        "urgency": "high",
        "recommendation": "Emergency Room",
        "description": "Chest pain could indicate serious conditions like heart attack. Seek immediate medical attention."
    },
    "difficulty breathing": {
        "urgency": "high",
        "recommendation": "Emergency Room",
        "description": "Difficulty breathing requires immediate medical attention."
    },
    "fever": {
        "urgency": "medium",
        "recommendation": "Urgent Care",
        "description": "High fever may require medical attention, but is not typically an emergency."
    },
    "headache": {
        "urgency": "low",
        "recommendation": "Primary Care",
        "description": "Schedule an appointment with your primary care physician."
    },
    "cough": {
        "urgency": "low",
        "recommendation": "Primary Care",
        "description": "Schedule an appointment with your primary care physician."
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_symptoms():
    data = request.json
    symptoms = data.get('symptoms', '').lower()
    
    # Simple matching logic - in a real app, this would use NLP
    matched_symptoms = []
    for symptom, info in SYMPTOM_DATABASE.items():
        if symptom in symptoms:
            matched_symptoms.append({
                "symptom": symptom,
                **info
            })
    
    if not matched_symptoms:
        return jsonify({
            "error": "No matching symptoms found. Please try describing your symptoms differently."
        })
    
    # Determine overall urgency based on matched symptoms
    urgencies = [s["urgency"] for s in matched_symptoms]
    overall_urgency = "high" if "high" in urgencies else "medium" if "medium" in urgencies else "low"
    
    return jsonify({
        "matched_symptoms": matched_symptoms,
        "overall_urgency": overall_urgency
    })

if __name__ == '__main__':
    app.run(debug=True) 