from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models import AnswerKeyStatus


class AnswerKeyCreate(BaseModel):
    question_id: int = Field(gt=0)
    answer: str | None = Field(default=None, max_length=32)
    status: AnswerKeyStatus = AnswerKeyStatus.PRELIMINARY
    source_reference: str | None = None
    is_annulled: bool = False


class AnswerKeyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question_id: int
    answer: str | None
    status: AnswerKeyStatus
    source_reference: str | None
    is_annulled: bool
    created_at: datetime
