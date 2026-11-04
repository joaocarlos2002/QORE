from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ExamCreate(BaseModel):
    board_id: int = Field(gt=0)
    source_id: int | None = Field(default=None, gt=0)
    name: str = Field(min_length=1, max_length=240)
    organization: str | None = Field(default=None, max_length=240)
    position: str | None = Field(default=None, max_length=240)
    year: int | None = Field(default=None, ge=1900, le=2200)


class ExamRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    board_id: int
    source_id: int | None
    name: str
    organization: str | None
    position: str | None
    year: int | None
    created_at: datetime
