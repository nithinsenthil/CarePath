# Symptom-to-Care Navigator

A web application that helps users determine the appropriate level of medical care based on their symptoms. Users can input their symptoms in plain English and receive recommendations for the type of care they should seek, along with urgency levels.

## Features

- Simple, intuitive interface for describing symptoms
- Real-time analysis of symptoms
- Urgency level assessment (High, Medium, Low)
- Specific care recommendations (Emergency Room, Urgent Care, Primary Care)
- Detailed explanations for each recommendation

## Setup Instructions

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```bash
   python app.py
   ```
4. Open your web browser and navigate to `http://localhost:5000`

## Technical Implementation

- Backend: Python Flask
- Frontend: HTML, CSS, JavaScript
- Simple symptom matching algorithm
- Modern, responsive UI design

## Future Enhancements

- Integration with Google Maps API for finding nearby medical facilities
- More sophisticated symptom analysis using NLP
- User accounts for tracking symptom history
- Integration with electronic health records
- Multi-language support

## Project Structure

```
.
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   └── index.html     # Main application page
└── README.md          # Project documentation
```

## Contributing

Feel free to submit issues and enhancement requests! 