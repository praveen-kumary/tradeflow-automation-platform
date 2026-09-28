from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class BusChannel(StrEnum):
    CANDLES = "candles.closed"
    SIGNALS = "signals.validated"
    EXECUTION = "execution.events"
    HEALTH = "system.health"
    ALERTS = "system.alerts"


class CandleEvent(BaseModel):
    symbol: str
    timeframe: str
    ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int


class SignalSide(StrEnum):
    BUY = "BUY"
    SELL = "SELL"
    WAIT = "WAIT"


class SignalEvent(BaseModel):
    symbol: str
    strategy: str
    side: SignalSide
    entry_price: float
    stop_loss: float
    target_price: float | None = None
    atr: float | None = None
    reason: str
    ts: datetime = Field(default_factory=datetime.utcnow)


class ExecutionEvent(BaseModel):
    symbol: str
    status: str
    message: str
    order_id: str | None = None
    ts: datetime = Field(default_factory=datetime.utcnow)


class HealthEvent(BaseModel):
    component: str
    ok: bool
    message: str
    ts: datetime = Field(default_factory=datetime.utcnow)

