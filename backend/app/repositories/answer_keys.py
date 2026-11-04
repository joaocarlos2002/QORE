from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import AnswerKey, AnswerKeyStatus


class AnswerKeyRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_for_question(self, question_id: int) -> list[AnswerKey]:
        statement = (
            select(AnswerKey)
            .where(AnswerKey.question_id == question_id)
            .order_by(AnswerKey.created_at)
        )
        return list(self.session.scalars(statement))

    def create(
        self,
        question_id: int,
        answer: str | None,
        status: AnswerKeyStatus,
        source_reference: str | None,
        is_annulled: bool = False,
    ) -> AnswerKey:
        answer_key = AnswerKey(
            question_id=question_id,
            answer=answer,
            status=status,
            source_reference=source_reference,
            is_annulled=is_annulled,
        )
        self.session.add(answer_key)
        self.session.flush()
        return answer_key
