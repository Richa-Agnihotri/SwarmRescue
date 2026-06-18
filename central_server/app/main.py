from fastapi import FastAPI, WebSocket, WebSocketDisconnect, status
from app.schemas import DroneTelemetry
from app.websocket_manager import ConnectionManager

app = FastAPI(
    title="SwarmRescue Gateway",
    description="High-concurrency network core routing multi-drone telemetry grids."
)

# Initialize live data broadcaster
manager = ConnectionManager()

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "SwarmRescue Backend Tower"}

# ENDPOINT 1: HTTP POST INGESTION (For the Drone Clients)
@app.post("/api/v1/telemetry", status_code=status.HTTP_202_ACCEPTED)
async def receive_drone_telemetry(payload: DroneTelemetry):
    print(f"📥 Ingested packet -> Drone {payload.drone_id} at coordinates {payload.coords}")
    
    
    # Stream the incoming packet out to the frontend dashboard over WebSockets instantly
    await manager.broadcast(payload.dict())
    
    return {"status": "ingested", "drone_id": payload.drone_id}

#  ENDPOINT 2: WEBSOCKET STREAM (For the React Frontend Dashboard)
@app.websocket("/ws/mission-control")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep line open. We can listen for command inputs from UI here if needed.
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)