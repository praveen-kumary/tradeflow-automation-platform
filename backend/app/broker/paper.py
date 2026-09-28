from uuid import uuid4

from app.broker.base import BrokerClient
from app.core.events import SignalEvent


class PaperBroker(BrokerClient):
    async def place_order(self, signal: SignalEvent, quantity: int) -> str:
        return f"PAPER-{uuid4().hex[:10].upper()}-{quantity}"

    async def cancel_all_orders(self) -> None:
        return None

    async def current_mtm(self) -> float:
        return 0.0

