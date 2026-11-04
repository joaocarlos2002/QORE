from dataclasses import dataclass
from pathlib import Path

import fitz


@dataclass(frozen=True)
class ExtractedBlock:
    page_number: int
    text: str
    left: float
    top: float
    right: float
    bottom: float


@dataclass(frozen=True)
class ExtractedPage:
    page_number: int
    text: str
    blocks: tuple[ExtractedBlock, ...]


class PdfTextExtractor:
    def extract(self, path: Path) -> tuple[ExtractedPage, ...]:
        if not path.is_file():
            raise FileNotFoundError(path)

        pages: list[ExtractedPage] = []
        with fitz.open(path) as document:
            for page_index, page in enumerate(document):
                blocks: list[ExtractedBlock] = []
                for block in page.get_text("blocks"):
                    left, top, right, bottom, text, *_ = block
                    normalized_text = text.strip()
                    if normalized_text:
                        blocks.append(
                            ExtractedBlock(
                                page_number=page_index + 1,
                                text=normalized_text,
                                left=left,
                                top=top,
                                right=right,
                                bottom=bottom,
                            )
                        )
                pages.append(
                    ExtractedPage(
                        page_number=page_index + 1,
                        text=page.get_text("text").strip(),
                        blocks=tuple(blocks),
                    )
                )
        return tuple(pages)
