from dataclasses import dataclass

from app.modules.parser import ParsedQuestion


@dataclass(frozen=True)
class ExtractionValidation:
    valid: bool
    warnings: tuple[str, ...]


class ExtractionValidator:
    def validate(
        self,
        questions: tuple[ParsedQuestion, ...],
        page_count: int,
    ) -> ExtractionValidation:
        warnings: list[str] = []
        seen_numbers: set[str] = set()

        for question in questions:
            if question.source_page < 1 or question.source_page > page_count:
                warnings.append(
                    f"question {question.number or '<unknown>'} has an invalid source page"
                )
            if not question.statement.strip():
                warnings.append(f"question {question.number or '<unknown>'} has no statement")
            if question.number and question.number in seen_numbers:
                warnings.append(f"question number {question.number} is duplicated")
            if question.number:
                seen_numbers.add(question.number)
            if len(question.alternatives) == 1:
                warnings.append(
                    f"question {question.number or '<unknown>'} has only one alternative"
                )
            warnings.extend(question.warnings)

        return ExtractionValidation(valid=not warnings, warnings=tuple(warnings))
