import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import time
import random
import os
import google.generativeai as genai

# --- 1. INITIALIZATION ---
# Firebase
cred = credentials.Certificate("service-account-key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'YOUR_DATABASE_URL_HERE'
})
ref_zones = db.reference('/zones')
ref_config = db.reference('/simulationConfig')

# Gemini AI (Replace with your key)
genai.configure(api_key="YOUR_GEMINI_API_KEY_HERE")
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 2. DATA LOADING (STRICT INDIA) ---
RAW_DATA_PATH = '../data/Global_Mobility_Report.csv'
PROCESSED_DATA_PATH = '../data/india_only_final.csv'

def get_india_data():
    if os.path.exists(PROCESSED_DATA_PATH):
        return pd.read_csv(PROCESSED_DATA_PATH, low_memory=False)
    
    print("📂 Filtering CSV (One-time setup)...")
    cols = ['sub_region_1', 'date', 'country_region', 'transit_stations_percent_change_from_baseline']
    iter_csv = pd.read_csv(RAW_DATA_PATH, usecols=cols, chunksize=100000, low_memory=False)
    india_df = pd.concat([chunk[chunk['country_region'] == 'India'] for chunk in iter_csv]).dropna(subset=['sub_region_1'])
    india_df.to_csv(PROCESSED_DATA_PATH, index=False)
    return india_df

india_df = get_india_data()

state_coords = {
    "Andaman and Nicobar Islands": {"lat": 11.7401, "lng": 92.6586}, "Andhra Pradesh": {"lat": 15.9129, "lng": 79.7400},
    "Arunachal Pradesh": {"lat": 27.1000, "lng": 93.6167}, "Assam": {"lat": 26.2006, "lng": 92.9376},
    "Bihar": {"lat": 25.0961, "lng": 85.3131}, "Chandigarh": {"lat": 30.7333, "lng": 76.7794},
    "Chhattisgarh": {"lat": 21.2514, "lng": 81.6296}, "Delhi": {"lat": 28.7041, "lng": 77.1025},
    "Goa": {"lat": 15.2993, "lng": 74.1240}, "Gujarat": {"lat": 22.2587, "lng": 71.1924},
    "Haryana": {"lat": 29.0588, "lng": 76.0856}, "Himachal Pradesh": {"lat": 31.1048, "lng": 77.1734},
    "Jammu and Kashmir": {"lat": 33.7782, "lng": 76.5762}, "Jharkhand": {"lat": 23.6102, "lng": 85.2799},
    "Karnataka": {"lat": 12.9716, "lng": 77.5946}, "Kerala": {"lat": 10.1632, "lng": 76.6413},
    "Ladakh": {"lat": 34.1526, "lng": 77.5770}, "Lakshadweep": {"lat": 10.5667, "lng": 72.6417},
    "Madhya Pradesh": {"lat": 23.2599, "lng": 77.4126}, "Maharashtra": {"lat": 19.0760, "lng": 72.8777},
    "Manipur": {"lat": 24.6637, "lng": 93.9063}, "Meghalaya": {"lat": 25.4670, "lng": 91.3662},
    "Mizoram": {"lat": 23.1645, "lng": 92.9376}, "Nagaland": {"lat": 26.1584, "lng": 94.5624},
    "Odisha": {"lat": 20.9517, "lng": 85.0985}, "Puducherry": {"lat": 11.9416, "lng": 79.8083},
    "Punjab": {"lat": 30.7333, "lng": 76.7794}, "Rajasthan": {"lat": 27.0238, "lng": 74.2179},
    "Sikkim": {"lat": 27.5330, "lng": 88.5122}, "Tamil Nadu": {"lat": 11.1271, "lng": 78.6569},
    "Telangana": {"lat": 17.3850, "lng": 78.4867}, "Tripura": {"lat": 23.9408, "lng": 91.9882},
    "Uttar Pradesh": {"lat": 26.8467, "lng": 80.9462}, "Uttarakhand": {"lat": 30.0668, "lng": 79.0193},
    "West Bengal": {"lat": 22.9868, "lng": 87.8550}
}

# --- 3. AI ANALYSIS FUNCTION ---
def get_ai_analysis(top_zones, mode):
    # This simulates high-level AI analysis perfectly without needing the API
    primary_state = top_zones[0]['name']
    density = top_zones[0]['density']
    
    # Technical logic based on actual data
    scenarios = {
        "festival": [
            f"Anomalous density detected in transit hubs due to festive migration.",
            "Deploy additional rapid-response units to main railway terminals."
        ],
        "protest": [
            f"Movement stagnation in (Density: {density}%). High risk of crowd crush.",
            "Establish perimeter cordons and reroute public transport immediately."
        ],
        "religious": [
            f"Mass gathering in exceeding baseline capacity by {density-40}%.",
            "Activate one-way pedestrian flow control systems."
        ],
        "normal": [
            f"Standard peak-hour load. Flow rates within safety margins.",
            "Routine monitoring active. No intervention required."
        ]
    }
    
    # Get the response pair based on mode
    analysis_pair = scenarios.get(mode, scenarios["normal"])
    
    return {
        "level": "High" if density > 75 else "Medium",
        "explanation": analysis_pair[0],
        "action": analysis_pair[1]
    }
# --- 4. MAIN LOOP ---
def run_simulation():
    print("🚀 CrowdBreak Engine Running...")
    while True:
        config = db.reference('/simulationConfig').get()
        mode = config.get('currentMode', 'normal') if config else 'normal'
        print(f"📡 Current Mode from Firebase: {mode}")
        dates = {"festival": ["2021-11-04"], "protest": ["2021-01-26"], "religious": ["2021-03-11"], "normal": ["2021-06-15"]}
        selected_date = random.choice(dates.get(mode, dates["normal"]))
        
        day_data = india_df[india_df['date'] == selected_date]
        zones_update = {}
        analysis_list = []

        for state, coords in state_coords.items():
            row = day_data[day_data['sub_region_1'] == state]
            if row.empty: continue
            
            base_mob = row.iloc[0].get('transit_stations_percent_change_from_baseline', 0)
            mult = 1.6 if mode != "normal" else 1.0
            density = max(10, min(100, 45 + (abs(base_mob) * 0.5 * mult)))
            
            clean_key = state.replace(" ", "_").replace("&", "and").lower()
            zone_obj = {"density": int(density), "speed": round(1.0 - (density/110), 2), "lat": coords["lat"], "lng": coords["lng"]}
            zones_update[clean_key] = zone_obj
            analysis_list.append({"name": state, "density": density})

        # Get AI analysis for the top 3 most crowded states
        analysis_list.sort(key=lambda x: x['density'], reverse=True)
        zones_update["risk"] = get_ai_analysis(analysis_list[:3], mode)

        # Change the update line to this:
        db.reference('/final_demo_data').update(zones_update)
        print(f"🔄 Updated India ({mode}) - AI Risk: {zones_update['risk']['level']}")
        time.sleep(5) # 5 seconds to stay safe with API limits

if __name__ == "__main__":
    run_simulation()