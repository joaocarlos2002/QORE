from datetime import datetime
from enum import StrEnum

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class AnswerKeyStatus(StrEnum):
    PRELIMINARY = "preliminary"
    FINAL = "final"
    ANNULLED = "annulled"


class AnswerKey(Base):
    __tablename__ = "answer_keys"

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), index=True)
    answer: Mapped[str | None] = mapped_column(String(32))
    status: Mapped[AnswerKeyStatus] = mapped_column(default=AnswerKeyStatus.PRELIMINARY)
    is_annulled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    source_reference: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    question: Mapped["Question"] = relationship()
