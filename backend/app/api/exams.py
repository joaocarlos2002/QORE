from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Exam
from app.repositories import ExamRepository
from app.schemas import ExamCreate, ExamRead, Page


router = APIRouter(prefix="/api/v1/exams", tags=["exams"])


async def require_local_auth(request: Request) -> None:
    await request.app.state.authenticator.require_token(request)


@router.get("", response_model=Page[ExamRead], dependencies=[Depends(require_local_auth)])
def list_exams(
    board_id: int | None = None,
    offset: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
) -> Page[ExamRead]:
    if offset < 0 or not 1 <= limit <= 100:
        raise HTTPException(status_code=422, detail="Invalid pagination values")
    items = ExamRepository(db).list(board_id)[offset : offset + limit]
    count = select(func.count()).select_from(Exam)
    if board_id is not None:
        count = count.where(Exam.board_id == board_id)
    total = db.scalar(count) or 0
    return Page(items=items, total=total, offset=offset, limit=limit)


@router.post(
    "",
    response_model=ExamRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_local_auth)],
)
def create_exam(payload: ExamCreate, db: Session = Depends(get_db)) -> Exam:
    exam = ExamRepository(db).create(
        payload.board_id,
        payload.name,
        payload.source_id,
        payload.organization,
        payload.position,
        payload.year,
    )
    db.commit()
    db.refresh(exam)
    return exam
