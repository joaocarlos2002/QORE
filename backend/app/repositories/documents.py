from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import DocumentStatus, SourceDocument
from app.services import StoredDocument


class DuplicateDocumentError(ValueError):
    """Raised when a document hash or storage path already exists."""


class SourceDocumentRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(
        self,
        source_id: int,
        stored: StoredDocument,
        exam_id: int | None = None,
        status: DocumentStatus = DocumentStatus.DOWNLOADED,
    ) -> SourceDocument:
        document = SourceDocument(
            source_id=source_id,
            exam_id=exam_id,
            filename=stored.filename,
            storage_path=str(stored.path),
            content_hash=stored.content_hash,
            status=status,
        )
        self.session.add(document)
        try:
            self.session.flush()
        except IntegrityError as exc:
            self.session.rollback()
            raise DuplicateDocumentError(stored.filename) from exc
        return document
