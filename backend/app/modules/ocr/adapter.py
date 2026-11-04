from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class OcrText:
    page_number: int
    text: str
    language: str


class OcrError(RuntimeError):
    """Raised when an OCR engine cannot process a page."""


class OcrEngine(Protocol):
    name: str

    def recognize(self, document: Path, page_number: int, language: str) -> OcrText:
        """Recognize one document page and preserve its source number."""


class DisabledOcrEngine:
    name = "disabled"

    def recognize(self, document: Path, page_number: int, language: str) -> OcrText:
        raise OcrError(
            f"OCR is disabled for page {page_number} of {document.name}; "
            "configure an OCR engine before processing scanned pages"
        )
