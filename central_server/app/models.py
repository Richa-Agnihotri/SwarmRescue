from sqlalchemy import Column, Integer, Float, Boolean, String
from app.database import Base

class TelemetryLog(Base):
    __tablename__ = "telemetry_logs"

    id = Column(Integer, primary_key=True, index=True)
    drone_id = Column(Integer, index=True)
    timestamp = Column(Float)
    # Storing coordinates as a string (e.g., "4.2,1.5,2.3") to keep SQLite simple
    coords = Column(String) 
    human_detected = Column(Boolean, default=False)
    fire_detected = Column(Boolean, default=False)