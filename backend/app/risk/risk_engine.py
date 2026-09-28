from dataclasses import dataclass

from app.core.config import Settings
from app.core.events import SignalEvent


@dataclass
class RiskDecision:
    allowed: bool
    quantity: int
    reason: str


class RiskEngine:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.trading_blocked = False

    def evaluate_daily_mtm(self, current_mtm: float) -> None:
        max_loss = self.settings.account_starting_capital * (
            self.settings.max_daily_drawdown_pct / 100
        )
        if current_mtm <= -max_loss:
            self.trading_blocked = True

    def size_order(self, signal: SignalEvent) -> RiskDecision:
        if self.trading_blocked:
            return RiskDecision(False, 0, "Daily kill switch is active")

        per_trade_risk = self.settings.account_starting_capital * (
            self.settings.risk_per_trade_pct / 100
        )
        stop_distance = abs(signal.entry_price - signal.stop_loss)
        if stop_distance <= 0:
            return RiskDecision(False, 0, "Invalid stop distance")

        quantity = int(per_trade_risk // stop_distance)
        if quantity < 1:
            return RiskDecision(False, 0, "Position size below minimum quantity")

        return RiskDecision(True, quantity, "Risk accepted")

