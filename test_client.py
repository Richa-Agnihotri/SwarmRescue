import requests
import time

payload = {
    "drone_id": 1,
    "timestamp": int(time.time()),  
    "coords": [12.54, 45.12, 3.50], 
    "human_detected": True,
    "fire_detected": False
}

URL = "http://127.0.0.1:8000/api/v1/telemetry"
response = requests.post(URL, json=payload)
print(response.json())