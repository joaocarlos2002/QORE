from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class SourceType(StrEnum):
    OFFICIAL = "official"
    PUBLIC = "public"
    OTHER = "other"


class PermissionStatus(StrEnum):
    UNKNOWN = "unknown"
    AUTHORIZED = "authorized"
    RESTRICTED = "restricted"


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    url: Mapped[str] = mapped_column(String(2048), unique=True, index=True)
    source_type: Mapped[SourceType] = mapped_column(default=SourceType.OTHER)
    permission_status: Mapped[PermissionStatus] = mapped_column(
        default=PermissionStatus.UNKNOWN
    )
    license_notes: Mapped[str | None] = mapped_column(Text)
    availability_notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    exams: Mapped[list["Exam"]] = relationship(back_populates="source")


class Exam(Base):
    __tablename__ = "exams"

    id: Mapped[int] = mapped_column(primary_key=True)
    board_id: Mapped[int] = mapped_column(ForeignKey("boards.id"), index=True)
    source_id: Mapped[int | None] = mapped_column(ForeignKey("sources.id"), index=True)
    name: Mapped[str] = mapped_column(String(240), index=True)
    organization: Mapped[str | None] = mapped_column(String(240))
    position: Mapped[str | None] = mapped_column(String(240))
    year: Mapped[int | None] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    board: Mapped["Board"] = relationship()
    source: Mapped[Source | None] = relationship(back_populates="exams")
