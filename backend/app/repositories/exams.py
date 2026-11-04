from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Exam


class DuplicateExamError(ValueError):
    """Raised when an exam cannot be persisted."""


class ExamRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self, board_id: int | None = None) -> list[Exam]:
        statement = select(Exam).order_by(Exam.year.desc().nullslast(), Exam.name)
        if board_id is not None:
            statement = statement.where(Exam.board_id == board_id)
        return list(self.session.scalars(statement))

    def create(
        self,
        board_id: int,
        name: str,
        source_id: int | None,
        organization: str | None,
        position: str | None,
        year: int | None,
    ) -> Exam:
        exam = Exam(
            board_id=board_id,
            source_id=source_id,
            name=name,
            organization=organization,
            position=position,
            year=year,
        )
        self.session.add(exam)
        try:
            self.session.flush()
        except IntegrityError as exc:
            self.session.rollback()
            raise DuplicateExamError(name) from exc
        return exam
