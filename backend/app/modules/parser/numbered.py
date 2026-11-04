from dataclasses import dataclass
import re

from app.modules.extraction import ExtractedPage
from app.modules.parser.base import ParsedQuestion, ParserError


_QUESTION_START = re.compile(r"(?m)^\s*(\d{1,4})[.)]\s+")
_ALTERNATIVE_START = re.compile(r"(?m)^\s*([A-E])[\).]\s+")


@dataclass(frozen=True)
class NumberedQuestionParser:
    name: str = "numbered"

    def parse(self, pages: tuple[ExtractedPage, ...]) -> tuple[ParsedQuestion, ...]:
        parsed: list[ParsedQuestion] = []
        for page in pages:
            text = page.text.strip()
            if not text:
                continue
            matches = list(_QUESTION_START.finditer(text))
            if not matches:
                continue
            for index, match in enumerate(matches):
                end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
                raw_question = text[match.end() : end].strip()
                parsed.append(self._parse_question(match.group(1), raw_question, page.page_number))
        if not parsed and pages:
            raise ParserError("No numbered questions found in extracted pages")
        return tuple(parsed)

    @staticmethod
    def _parse_question(number: str, raw_question: str, page_number: int) -> ParsedQuestion:
        alternatives = list(_ALTERNATIVE_START.finditer(raw_question))
        if not alternatives:
            return ParsedQuestion(
                number=number,
                statement=raw_question,
                alternatives=(),
                source_page=page_number,
                is_incomplete=True,
                warnings=("no alternatives detected",),
            )

        statement = raw_question[: alternatives[0].start()].strip()
        values: list[str] = []
        for index, alternative in enumerate(alternatives):
            end = alternatives[index + 1].start() if index + 1 < len(alternatives) else len(raw_question)
            values.append(raw_question[alternative.end() : end].strip())
        incomplete = not statement or any(not value for value in values)
        warnings = ("incomplete question structure",) if incomplete else ()
        return ParsedQuestion(
            number=number,
            statement=statement,
            alternatives=tuple(values),
            source_page=page_number,
            is_incomplete=incomplete,
            warnings=warnings,
        )
