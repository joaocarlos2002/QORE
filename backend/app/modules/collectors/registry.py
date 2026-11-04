from collections.abc import Callable

from app.modules.collectors.base import Collector


class CollectorRegistry:
    def __init__(self) -> None:
        self._factories: dict[str, Callable[[], Collector]] = {}

    def register(self, name: str, factory: Callable[[], Collector]) -> None:
        key = self._normalize(name)
        if key in self._factories:
            raise ValueError(f"Collector already registered: {name}")
        self._factories[key] = factory

    def create(self, name: str) -> Collector:
        key = self._normalize(name)
        try:
            factory = self._factories[key]
        except KeyError as exc:
            raise LookupError(f"Collector not registered: {name}") from exc
        return factory()

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._factories))

    @staticmethod
    def _normalize(name: str) -> str:
        normalized = name.strip().lower()
        if not normalized:
            raise ValueError("Collector name cannot be empty")
        return normalized
