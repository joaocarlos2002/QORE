from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class DocumentStatus(StrEnum):
    DISCOVERED = "discovered"
    DOWNLOADED = "downloaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"


class SourceDocument(Base):
    __tablename__ = "source_documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"), index=True)
    exam_id: Mapped[int | None] = mapped_column(ForeignKey("exams.id"), index=True)
    filename: Mapped[str] = mapped_column(String(260))
    storage_path: Mapped[str] = mapped_column(String(2048), unique=True)
    content_hash: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    status: Mapped[DocumentStatus] = mapped_column(default=DocumentStatus.DISCOVERED)
    collected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    source: Mapped["Source"] = relationship()
    exam: Mapped["Exam | None"] = relationship()
