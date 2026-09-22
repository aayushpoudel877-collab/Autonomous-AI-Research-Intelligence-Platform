from collections import defaultdict
from collections.abc import Callable

class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[str, list[Callable[[object], None]]] = defaultdict(list)

    def subscribe(self, event: str, handler: Callable[[object], None]) -> None:
        self._handlers[event].append(handler)

    def publish(self, event: str, payload: object) -> None:
        for handler in tuple(self._handlers[event]):
            handler(payload)
