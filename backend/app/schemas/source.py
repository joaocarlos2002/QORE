from datetime import datetime

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field

from app.models import SourceType


class SourceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    url: AnyHttpUrl
    source_type: SourceType = SourceType.OTHER
    availability_notes: str | None = None


class SourceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    url: str
    source_type: SourceType
    availability_notes: str | None
    created_at: datetime
