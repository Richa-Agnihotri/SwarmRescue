# SwarmRescue Gateway - Core API Specifications

This document defines the backend communication endpoints built for the SwarmRescue data pipeline.

## 1. Data Ingestion Endpoint (For ML / Drone Client Team)
* **Protocol:** HTTP POST
* **URL:** `http://127.0.0.1:8000/api/v1/telemetry`
* **Content-Type:** `application/json`

### Request Payload Structure:
```json
{
  "drone_id": 1,
  "timestamp": 1715163400.0,
  "coords": [4.25, 1.50, 2.30], 
  "human_detected": false,
  "fire_detected": false
}