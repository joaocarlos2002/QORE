from fastapi import APIRouter, Depends, Request
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import DocumentStatus, SourceDocument
from app.repositories.document_queries import SourceDocumentQueryRepository
from app.schemas import Page, SourceDocumentRead


router = APIRouter(prefix="/api/v1/documents", tags=["documents"])


async def require_local_auth(request: Request) -> None:
    await request.app.state.authenticator.require_token(request)


@router.get("", response_model=Page[SourceDocumentRead], dependencies=[Depends(require_local_auth)])
def list_documents(
    status: DocumentStatus | None = None,
    exam_id: int | None = None,
    offset: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
) -> Page[SourceDocumentRead]:
    items = SourceDocumentQueryRepository(db).list(status, exam_id)[offset : offset + limit]
    count = select(func.count()).select_from(SourceDocument)
    if status is not None:
        count = count.where(SourceDocument.status == status)
    if exam_id is not None:
        count = count.where(SourceDocument.exam_id == exam_id)
    total = db.scalar(count) or 0
    return Page(items=items, total=total, offset=offset, limit=limit)
