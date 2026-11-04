from dataclasses import dataclass

from app.modules.extraction import ExtractedPage


@dataclass(frozen=True)
class OcrPageDecision:
    page_number: int
    requires_ocr: bool
    reason: str


class OcrPageDetector:
    def __init__(self, minimum_text_characters: int = 20) -> None:
        if minimum_text_characters < 1:
            raise ValueError("minimum_text_characters must be positive")
        self.minimum_text_characters = minimum_text_characters

    def detect(self, pages: tuple[ExtractedPage, ...]) -> tuple[OcrPageDecision, ...]:
        decisions: list[OcrPageDecision] = []
        for page in pages:
            text_length = len("".join(page.text.split()))
            if text_length >= self.minimum_text_characters:
                decisions.append(
                    OcrPageDecision(page.page_number, False, "text content is available")
                )
            elif page.blocks:
                decisions.append(
                    OcrPageDecision(page.page_number, False, "positioned text is available")
                )
            else:
                decisions.append(
                    OcrPageDecision(page.page_number, True, "no usable text content detected")
                )
        return tuple(decisions)
