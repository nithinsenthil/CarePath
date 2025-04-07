# Symptom-to-Care Navigator

A web application that helps users determine the appropriate level of medical care based on their symptoms. The application uses Claude AI for symptom analysis and Google Maps API for location-based recommendations.

## Features

- **Symptom Analysis**: Users can describe their symptoms in plain English
- **Care Recommendations**: AI-powered analysis suggests appropriate care level
- **Location Services**: Finds nearby medical facilities based on urgency
- **Travel Information**: Provides travel time and distance to facilities
- **Emergency Guidance**: Offers immediate steps for emergency situations

## Project Structure

```
CarePath/
├── static/
│   └── styles.css           # CSS styles for the application
├── templates/
│   └── index.html          # Main application interface
├── app.py                  # Flask backend with AI integration
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - `ANTHROPIC_API_KEY`: Your Claude API key
   - `GOOGLE_MAPS_API_KEY`: Your Google Maps API key

4. Run the application:
   ```bash
   python app.py
   ```

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **AI**: Claude (via Anthropic API)
- **Maps**: Google Maps API
- **Styling**: Custom CSS with frosted glass effect

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