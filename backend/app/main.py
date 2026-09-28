from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from app.api import health, trades
from app.core.config import get_settings
from app.core.events import BusChannel
from app.core.redis_bus import subscribe

settings = get_settings()

app = FastAPI(title="Trade Automation API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.dashboard_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(trades.router)


@app.websocket("/ws/live")
async def live_updates(websocket: WebSocket) -> None:
    await websocket.accept()
    async for event in subscribe(BusChannel.EXECUTION):
        await websocket.send_json(event)

