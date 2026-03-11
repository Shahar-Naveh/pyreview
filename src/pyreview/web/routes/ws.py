"""WebSocket endpoint for streaming review progress to the browser."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, review_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(review_id, []).append(websocket)

    def disconnect(self, review_id: str, websocket: WebSocket):
        conns = self.active_connections.get(review_id, [])
        if websocket in conns:
            conns.remove(websocket)

    async def broadcast(self, review_id: str, message: dict):
        for ws in self.active_connections.get(review_id, []):
            try:
                await ws.send_json(message)
            except Exception:
                pass


manager = ConnectionManager()


@router.websocket("/ws/review/{review_id}")
async def review_progress(websocket: WebSocket, review_id: str):
    await manager.connect(review_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(review_id, websocket)
