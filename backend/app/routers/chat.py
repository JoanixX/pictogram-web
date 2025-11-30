from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict

router = APIRouter(prefix="/chat", tags=["Chat"])

class ConnectionManager:
    def __init__(self):
        # Map room_id -> List[WebSocket]
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def broadcast(self, message: dict, room_id: str):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/{room_id}/{username}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, username: str):
    await manager.connect(websocket, room_id)
    try:
        # Notify user joined
        await manager.broadcast({
            "type": "system",
            "content": f"{username} ha entrado a la sala",
            "user": "System"
        }, room_id)
        
        while True:
            data = await websocket.receive_json()
            # data expected format: {"content": [...pictograms...], "type": "message"}
            await manager.broadcast({
                "type": "message",
                "content": data.get("content"),
                "user": username
            }, room_id)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
        await manager.broadcast({
            "type": "system",
            "content": f"{username} ha salido de la sala",
            "user": "System"
        }, room_id)
