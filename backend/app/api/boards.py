from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Board
from app.repositories import BoardRepository
from app.schemas import BoardCreate, BoardRead, Page


router = APIRouter(prefix="/api/v1/boards", tags=["boards"])


async def require_local_auth(request: Request) -> None:
    await request.app.state.authenticator.require_token(request)


@router.get("", response_model=Page[BoardRead], dependencies=[Depends(require_local_auth)])
def list_boards(
    offset: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
) -> Page[BoardRead]:
    if offset < 0 or not 1 <= limit <= 100:
        raise HTTPException(status_code=422, detail="Invalid pagination values")
    repository = BoardRepository(db)
    items = repository.list()[offset : offset + limit]
    total = db.scalar(select(func.count()).select_from(Board)) or 0
    return Page(items=items, total=total, offset=offset, limit=limit)


@router.post(
    "",
    response_model=BoardRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_local_auth)],
)
def create_board(payload: BoardCreate, db: Session = Depends(get_db)) -> Board:
    board = BoardRepository(db).create(payload.name)
    db.commit()
    db.refresh(board)
    return board
