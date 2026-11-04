from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True)
class CollectorDocument:
    filename: str
    url: str
    kind: str
    discovered_at: datetime


@dataclass(frozen=True)
class CollectorResult:
    source_name: str
    documents: tuple[CollectorDocument, ...]
    warnings: tuple[str, ...] = ()


class CollectorError(RuntimeError):
    def __init__(self, source_name: str, message: str) -> None:
        super().__init__(f"{source_name}: {message}")
        self.source_name = source_name
        self.message = message


class Collector(Protocol):
    name: str

    def discover(self, query: str | None = None) -> CollectorResult:
        """Discover authorized exam and answer-key documents."""

    def download(self, document: CollectorDocument) -> bytes:
        """Download one previously discovered authorized document."""
