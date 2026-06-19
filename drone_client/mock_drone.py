import requests
import time
import random

# Pointing straight to local FastAPI server endpoint
SERVER_URL = "http://127.0.0.1:8000/api/v1/telemetry"

print("🚀 Starting simulated drone client telemetry loop...")

# Simulate a drone flying through a building dropping 10 sequential waypoints
for step in range(1, 11):
    # Generating fake spatial movement coordinates [x, y, z]
    fake_x = round(random.uniform(0.0, 10.0), 2)
    fake_y = round(random.uniform(0.0, 10.0), 2)
    fake_z = round(random.uniform(0.0, 3.0), 2)
    
    # Pack the data exactly how Pydantic schema expects it
    payload = {
        "drone_id": 1,
        "timestamp": time.time(),
        "coords": [fake_x, fake_z, fake_y],
        "human_detected": random.choice([True, False, False, False]), # 25% chance of finding a human
        "fire_detected": False
    }
    
    try:
        # Fire the data across the local network host
        response = requests.post(SERVER_URL, json=payload)
        if response.status_code == 202:
            print(f"✅ Step {step}: Sent coordinates {payload['coords']} | Server Accepted.")
        else:
            print(f"⚠️ Server returned unexpected error status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure your uvicorn server is running in the other terminal.")
        
    time.sleep(2) # Pause for 2 seconds before sending the next movement packet