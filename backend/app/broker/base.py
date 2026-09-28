from abc import ABC, abstractmethod

from app.core.events import SignalEvent


class BrokerClient(ABC):
    @abstractmethod
    async def place_order(self, signal: SignalEvent, quantity: int) -> str:
        raise NotImplementedError

    @abstractmethod
    async def cancel_all_orders(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def current_mtm(self) -> float:
        raise NotImplementedError

