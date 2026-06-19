from fastapi import FastAPI, WebSocket, WebSocketDisconnect, status, Depends
from sqlalchemy.orm import Session
from app.schemas import DroneTelemetry
from app.websocket_manager import ConnectionManager
from app.database import engine, Base, get_db
from app.models import TelemetryLog

# Automatically generate the database file and tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SwarmRescue Gateway")
manager = ConnectionManager()

@app.get("/")
def health_check():
    return {"status": "healthy"}

# ENDPOINT 1: HTTP POST INGESTION (Saves Drone Data to DB) 
@app.post("/api/v1/telemetry", status_code=status.HTTP_202_ACCEPTED)
async def receive_drone_telemetry(payload: DroneTelemetry, db: Session = Depends(get_db)):
    coords_str = ",".join(map(str, payload.coords))
    
    db_log = TelemetryLog(
        drone_id=payload.drone_id,
        timestamp=payload.timestamp,
        coords=coords_str,
        human_detected=payload.human_detected,
        fire_detected=payload.fire_detected
    )
    
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    
    print(f"💾 Saved to DB -> Drone {payload.drone_id} committed record ID: {db_log.id}")
    
    await manager.broadcast(payload.dict())
    return {"status": "saved_and_ingested", "record_id": db_log.id}

#  NEW ENDPOINT 2: HTTP GET HISTORY (For the Frontend Dashboard) ---
@app.get("/api/v1/telemetry/history")
def get_telemetry_history(drone_id: int = None, db: Session = Depends(get_db)):
    """
    Fetches historical paths. If a specific drone_id is provided, 
    it filters just for that drone; otherwise, it returns everything.
    """
    query = db.query(TelemetryLog)
    if drone_id:
        query = query.filter(TelemetryLog.drone_id == drone_id)
    
    logs = query.order_by(TelemetryLog.timestamp.asc()).all()
    
    # Format the data cleanly back into JSON lists for the frontend
    formatted_logs = []
    for log in logs:
        formatted_logs.append({
            "id": log.id,
            "drone_id": log.drone_id,
            "timestamp": log.timestamp,
            "coords": [float(x) for x in log.coords.split(",")], # Convert string back to list
            "human_detected": log.human_detected,
            "fire_detected": log.fire_detected
        })
        
    return formatted_logs

# ENDPOINT 3: WEBSOCKET STREAM 
@app.websocket("/ws/mission-control")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)