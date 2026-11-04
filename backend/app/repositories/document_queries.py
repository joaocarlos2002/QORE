from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import DocumentStatus, SourceDocument


class SourceDocumentQueryRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(
        self,
        status: DocumentStatus | None = None,
        exam_id: int | None = None,
    ) -> list[SourceDocument]:
        statement = select(SourceDocument).order_by(SourceDocument.created_at.desc())
        if status is not None:
            statement = statement.where(SourceDocument.status == status)
        if exam_id is not None:
            statement = statement.where(SourceDocument.exam_id == exam_id)
        return list(self.session.scalars(statement))
