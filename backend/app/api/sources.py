from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Source
from app.repositories import SourceRepository
from app.schemas import Page, SourceCreate, SourceRead


router = APIRouter(prefix="/api/v1/sources", tags=["sources"])


async def require_local_auth(request: Request) -> None:
    await request.app.state.authenticator.require_token(request)


@router.get("", response_model=Page[SourceRead], dependencies=[Depends(require_local_auth)])
def list_sources(
    offset: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
) -> Page[SourceRead]:
    if offset < 0 or not 1 <= limit <= 100:
        raise HTTPException(status_code=422, detail="Invalid pagination values")
    items = SourceRepository(db).list()[offset : offset + limit]
    total = db.scalar(select(func.count()).select_from(Source)) or 0
    return Page(items=items, total=total, offset=offset, limit=limit)


@router.post(
    "",
    response_model=SourceRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_local_auth)],
)
def create_source(payload: SourceCreate, db: Session = Depends(get_db)) -> Source:
    source = SourceRepository(db).create(
        payload.name,
        str(payload.url),
        payload.source_type,
        payload.permission_status,
        payload.license_notes,
        payload.availability_notes,
    )
    db.commit()
    db.refresh(source)
    return source
