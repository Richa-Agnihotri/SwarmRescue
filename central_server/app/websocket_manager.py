from fastapi import WebSocket
from typing import List

class ConnectionManager:
    def __init__(self):
        # Keeps an active list of all open web browser dashboards
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"📡 New dashboard connected. Total active tabs: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"🛑 Dashboard disconnected. Remaining: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        # Push data packets out to every single open web dashboard instantly
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                # Handle silent broken browser closures cleanly
                self.active_connections.remove(connection)