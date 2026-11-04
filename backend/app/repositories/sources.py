from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Source, SourceType


class DuplicateSourceError(ValueError):
    """Raised when a source name or URL is already registered."""


class SourceRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self) -> list[Source]:
        statement = select(Source).order_by(Source.name)
        return list(self.session.scalars(statement))

    def create(
        self,
        name: str,
        url: str,
        source_type: SourceType,
        availability_notes: str | None,
    ) -> Source:
        source = Source(
            name=name,
            url=url,
            source_type=source_type,
            availability_notes=availability_notes,
        )
        self.session.add(source)
        try:
            self.session.flush()
        except IntegrityError as exc:
            self.session.rollback()
            raise DuplicateSourceError(name) from exc
        return source
