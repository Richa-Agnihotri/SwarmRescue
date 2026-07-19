# Spatiotemporal Engine

## Overview

The **Spatiotemporal Engine** is the integration and reasoning module of the **SwarmRescue** system.

It bridges the computer vision pipeline and the Mission Control backend by processing object detections, performing temporal reasoning, simulating drone movement, generating standardized telemetry, and transmitting mission updates to the Central Server.

Rather than performing object detection itself, the engine consumes detections produced by the YOLO-based Vision Module and transforms them into reliable, backend-ready telemetry.

---

# System Architecture

```
                    SwarmRescue

        Drone Video
             │
             ▼
     Vision Module (YOLO)
             │
             ▼
  Spatiotemporal Engine
             │
 ┌───────────┼────────────┐
 │           │            │
 ▼           ▼            ▼
Temporal  Trajectory   Telemetry
Filter    Simulation    Generation
             │
             ▼
     Telemetry Sender
             │
             ▼
      Mission Control API
             │
             ▼
      SQLite Database
             │
             ▼
     Mission Control UI
```

---

# Responsibilities

The Spatiotemporal Engine is responsible for:

- Reading prerecorded drone video
- Running object detection through the Vision Module
- Performing temporal confirmation of detected events
- Simulating deterministic drone trajectories
- Creating standardized telemetry packets
- Transmitting telemetry to the Mission Control backend

---

# Non-Responsibilities

This module intentionally does **not**:

- Train object detection models
- Modify YOLO weights
- Perform database operations
- Implement backend APIs
- Visualize telemetry
- Manage Mission Control UI

---

# Features

- Modular architecture
- YOLO inference wrapper
- Frame-by-frame processing
- Sliding-window temporal confirmation
- Deterministic drone trajectory simulation
- Backend-compatible telemetry generation
- HTTP-based telemetry transmission
- Backend health checking
- End-to-end integration with SwarmRescue Central Server

---

# Project Structure

```
spatiotemporal_engine/
│
├── config/
│
├── logs/
│
├── trajectories/
│   └── test_video.mp4
│
├── src/
│   ├── communication/
│   │   └── telemetry_sender.py
│   │
│   ├── mission/
│   │   ├── config.py
│   │   ├── logger.py
│   │   └── mission_engine.py
│   │
│   ├── models/
│   │   └── detection.py
│   │
│   ├── simulation/
│   │   ├── drone_trajectory.py
│   │   └── video_reader.py
│   │
│   ├── telemetry/
│   │   └── telemetry_packet.py
│   │
│   ├── tracking/
│   │   └── temporal_filter.py
│   │
│   ├── vision/
│   │   └── detector.py
│   │
│   └── main.py
│
├── tests/
│
├── pyproject.toml
│
└── README.md
```

---

# Processing Pipeline

Each frame passes through the following stages:

```
Video Frame
      │
      ▼
Vision Detector
      │
      ▼
Detections
      │
      ▼
Temporal Confirmation
      │
      ▼
Confirmed Events
      │
      ▼
Trajectory Simulation
      │
      ▼
Telemetry Packet
      │
      ▼
Telemetry Sender
      │
      ▼
Mission Control Backend
```

---

# Modules

## Vision Module

The Vision Module encapsulates the YOLO object detector behind a reusable interface.

Responsibilities:

- Load the trained model
- Perform inference
- Convert predictions into standardized Detection objects

The remaining modules remain independent of the underlying computer vision framework.

---

## Video Reader

Simulates a drone camera using prerecorded video.

Provides:

- Frame index
- Timestamp
- OpenCV frame

Automatically releases resources using Python context managers.

---

## Temporal Confirmation Filter

Object detectors may produce unstable predictions due to:

- Motion blur
- Occlusion
- Lighting changes
- Sensor noise

The Temporal Confirmation Filter stabilizes detections using a sliding window.

Default configuration:

- Window size: **5 frames**
- Confirmation threshold: **3 frames**

Only persistent detections generate mission telemetry.

---

## Drone Trajectory Simulation

The trajectory simulator produces deterministic drone positions throughout the mission.

Current assumptions:

- Constant speed
- Constant heading
- Constant altitude

Because downstream modules depend only on the `position_at(timestamp)` interface, simulated trajectories can later be replaced with real GPS telemetry without modifying the remainder of the system.

---

## Telemetry Packet

Represents a single mission update.

Each packet contains:

- Drone ID
- Timestamp
- Position
- Human detection status
- Fire detection status

The packet is serialized into the exact JSON schema expected by the backend.

Example:

```json
{
  "drone_id": 1,
  "timestamp": 2.75,
  "coords": [8.25, 0.0, 20.0],
  "human_detected": false,
  "fire_detected": true
}
```

---

## Telemetry Sender

Responsible for communication with the Mission Control backend.

Responsibilities:

- Backend health check
- HTTP POST requests
- Response validation
- Error propagation

Endpoints:

```
GET  /
POST /api/v1/telemetry
```

---

## Mission Engine

The Mission Engine orchestrates the complete processing pipeline.

For every video frame it:

1. Reads the next frame.
2. Runs object detection.
3. Applies temporal confirmation.
4. Computes the drone position.
5. Creates a telemetry packet.
6. Sends telemetry to the backend.
7. Logs mission progress.

This module serves as the runtime entry point of the Spatiotemporal Engine.

---

# Testing

Each module has been tested independently before integration.

Current test suite includes:

| Test | Description |
|------|-------------|
| `test_detector.py` | YOLO model loading and inference |
| `test_video_reader.py` | Video frame acquisition |
| `test_video_detection.py` | Detection pipeline |
| `test_temporal_filter.py` | Temporal confirmation |
| `test_video_temporal_pipeline.py` | Video + detection + temporal integration |
| `test_drone_trajectory.py` | Trajectory simulation |
| `test_telemetry_packet.py` | Telemetry serialization |
| `test_telemetry_sender.py` | Backend communication |

---

# Running the Project

## 1. Clone the repository

```bash
git clone <repository-url>
cd spatiotemporal_engine
```

---

## 2. Create a virtual environment

```bash
python -m venv .venv
```

---

## 3. Activate the environment

### Windows

```powershell
.venv\Scripts\Activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

## 4. Install dependencies

```bash
pip install -e .
```

---

## 5. Start the Central Server

```bash
uvicorn app.main:app --reload
```

---

## 6. Run the Mission Engine

```bash
python -m src.main
```

---

# Expected Runtime Flow

```
Mission started.

Frame 0001
↓

YOLO Detection
↓

Temporal Confirmation
↓

Trajectory Simulation
↓

Telemetry Packet
↓

Mission Control API

...

Mission completed.
```

---

# Current Status

**MVP Completed**

Implemented:

- Video processing
- YOLO integration
- Temporal reasoning
- Drone trajectory simulation
- Telemetry generation
- Backend communication
- End-to-end pipeline execution

The module is fully integrated with the SwarmRescue Central Server and is ready for demonstration and further system integration.

---

# Future Work

Potential enhancements include:

- Real drone GPS integration
- Live camera streaming
- Multi-drone mission support
- WebSocket telemetry streaming
- Mission replay
- Configuration via YAML/TOML
- Docker deployment
- Retry mechanisms and fault tolerance
- Performance metrics and monitoring

---

# License

This project is part of the **SwarmRescue** system and is intended for academic and research purposes.