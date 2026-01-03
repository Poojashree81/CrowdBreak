🛡️ CrowdBreak: AI-Powered Urban Safety Intelligence
CrowdBreak is a real-time crowd monitoring and safety intervention system designed for the Indian context. By analyzing mobility data through a Hybrid Inference Model, the system detects potential crowd-crush risks during festivals, protests, and religious gatherings, providing automated emergency protocols.

🌟 Key Features
Real-time Analytics: Processes live mobility data to calculate crowd density and movement speed across 35+ Indian states and union territories.

Hybrid AI Engine: Combines local high-speed heuristic processing for zero-latency alerts with Google Gemini 1.5 Pro for deep contextual safety analysis.

Scenario-Based Simulation: Toggle between "Normal," "Festival," "Protest," and "Religious Gathering" modes to observe how the AI adapts its safety logic.

Interactive Dashboard: A live-updating map interface built with Firebase and Google Maps API for incident commanders.

🛠️ Tech Stack
Language: Python 3.10+
Frontend: HTML5, CSS3, JavaScript (ES6)
Database: Firebase Realtime Database
AI: Google Gemini 2.5 API
Hosting: Firebase Hosting
Data: Google Global Mobility Reports (Indian Transit Sub-region data)

🚀 Getting Started
1. Prerequisites
Python installed on your machine.
A Firebase Project with Realtime Database enabled.
A Google Gemini API Key.
A Google Maps JavaScript API Key.

2. Installation
Clone the repository and install dependencies:
    git clone https://github.com/YOUR_USERNAME/CrowdBreak.git
    cd CrowdBreak
    pip install -r requirements.txt

3. Configuration
Place your service-account-key.json (from Firebase) in the /simulator folder.
Update the api_key in simulator.py with your Gemini API key.
Update the Firebase config in index.html with your web app credentials.

4. Running the Project
Start the Simulation Engine:
    python simulator.py
Launch the Dashboard: Open index.html in your browser or deploy via Firebase:
    firebase deploy --only hosting

🧠 System Architecture: Hybrid Inference
To ensure zero-latency in life-critical situations, CrowdBreak utilizes a two-tier analysis system:

Edge Layer: Immediately calculates crowd speed and density. If thresholds (e.g., >80%) are met, safety actions are triggered instantly.

Cloud Layer: The data is asynchronously sent to Gemini AI to generate a natural language summary and long-term strategic recommendations (e.g., "Deploy marshals to Dadar Station").

🛡️ Safety & Privacy
Anonymized Data: The system uses aggregate mobility percentages, ensuring no individual tracking or PII (Personally Identifiable Information) is processed.

Fail-Safe Design: If the API connection is lost, the system defaults to local heuristic safety protocols.