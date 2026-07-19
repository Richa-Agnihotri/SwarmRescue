from fastapi import FastAPI, WebSocket, WebSocketDisconnect, status, Depends, HTTPException  # Updated imports
from fastapi.middleware.cors import CORSMiddleware 
from sqlalchemy.orm import Session
from app.schemas import DroneTelemetry
from app.websocket_manager import ConnectionManager
from app.database import engine, Base, get_db
from app.models import TelemetryLog
import logging

# Automatically generate the database file and tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SwarmRescue Gateway")

# Configure the logging format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(), # Prints clean logs to your terminal
        logging.FileHandler("swarm_rescue.log") # Automatically saves logs to a file!
    ]
)
logger = logging.getLogger("SwarmRescue")

# CONFIGURING CORS MIDDLEWARE 
# This unlocks your API lanes so the React team can fetch the data securely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all frontend origins (React, Vite, Live Server)
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # Allows all browser headers
)

manager = ConnectionManager()

@app.get("/")
def health_check():
    return {"status": "healthy"}


# ENDPOINT 1: HTTP POST INGESTION (Saves Drone Data to DB with Validation Guardrails) 
@app.post("/api/v1/telemetry", status_code=status.HTTP_202_ACCEPTED)
async def receive_drone_telemetry(payload: DroneTelemetry, db: Session = Depends(get_db)):
    
    # 🛑 GUARDRAIL: Validate that coordinates contain exactly 3 elements (X, Y, Z)
    if not payload.coords or len(payload.coords) != 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid coordinate format. Payload must contain exactly three numerical values [X, Y, Z]."
        )
        
    try:
        # Double-check that all coordinate values can be cast to floats successfully
        coords_str = ",".join(map(str, [float(x) for x in payload.coords]))
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Coordinates must be numeric values (integers or floats)."
        )
    
    db_log = TelemetryLog(
        drone_id=payload.drone_id,
        timestamp=payload.timestamp,
        coords=coords_str,
        human_detected=payload.human_detected,
        fire_detected=payload.fire_detected
    )
    
    # 🛡️ DATABASE TRANSACTION FAIL-SAFE BLOCK
    try:
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        logger.info(f"Database Commit Success -> Drone {payload.drone_id} logged record ID: {db_log.id}")
    except Exception as e:
        db.rollback()  # ⏪ Reverts any partial changes so the session doesn't corrupt
        logger.error(f"Database Transaction Failed for Drone {payload.drone_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error: Database write operation failed."
        )
    
    await manager.broadcast(payload.dict())
    return {"status": "saved_and_ingested", "record_id": db_log.id}


# ENDPOINT 2: HTTP GET HISTORY (For the Frontend Dashboard)
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