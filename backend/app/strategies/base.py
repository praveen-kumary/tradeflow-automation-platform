from dataclasses import dataclass

from app.core.events import SignalSide


@dataclass(frozen=True)
class StrategyDecision:
    side: SignalSide
    stop_loss: float | None
    target_price: float | None
    reason: str

