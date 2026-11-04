from dataclasses import dataclass
from typing import Protocol

from app.modules.extraction import ExtractedPage


@dataclass(frozen=True)
class ParsedQuestion:
    number: str | None
    statement: str
    alternatives: tuple[str, ...]
    source_page: int
    is_incomplete: bool
    warnings: tuple[str, ...] = ()


class ParserError(RuntimeError):
    """Raised when a parser cannot interpret the extracted document."""


class Parser(Protocol):
    name: str

    def parse(self, pages: tuple[ExtractedPage, ...]) -> tuple[ParsedQuestion, ...]:
        """Parse extracted pages without discarding incomplete questions."""
