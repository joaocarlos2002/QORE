from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AnswerKey
from app.repositories import AnswerKeyRepository
from app.schemas import AnswerKeyCreate, AnswerKeyRead


router = APIRouter(prefix="/api/v1/answer-keys", tags=["answer-keys"])


async def require_local_auth(request: Request) -> None:
    await request.app.state.authenticator.require_token(request)


@router.get(
    "/questions/{question_id}",
    response_model=list[AnswerKeyRead],
    dependencies=[Depends(require_local_auth)],
)
def list_answer_keys(question_id: int, db: Session = Depends(get_db)) -> list[AnswerKey]:
    return AnswerKeyRepository(db).list_for_question(question_id)


@router.post(
    "",
    response_model=AnswerKeyRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_local_auth)],
)
def create_answer_key(
    payload: AnswerKeyCreate,
    db: Session = Depends(get_db),
) -> AnswerKey:
    answer_key = AnswerKeyRepository(db).create(
        question_id=payload.question_id,
        answer=payload.answer,
        status=payload.status,
        source_reference=payload.source_reference,
        is_annulled=payload.is_annulled,
    )
    db.commit()
    db.refresh(answer_key)
    return answer_key
