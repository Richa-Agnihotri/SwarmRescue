from pydantic import BaseModel, Field
from typing import List

class DroneTelemetry(BaseModel):
    drone_id: int = Field(..., description="Unique ID of the drone client")
    timestamp: float = Field(..., description="Epoch timestamp of generation")
    coords: List[float] = Field(..., min_items=3, max_items=3, description="Exact [x, y, z] coordinate positions")
    human_detected: bool = Field(False, description="True if a survivor is flagged in this frame")
    fire_detected: bool = Field(False, description="True if a fire hazard is flagged")