from datetime import datetime

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field

from app.models import PermissionStatus, SourceType


class SourceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    url: AnyHttpUrl
    source_type: SourceType = SourceType.OTHER
    permission_status: PermissionStatus = PermissionStatus.UNKNOWN
    license_notes: str | None = None
    availability_notes: str | None = None


class SourceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    url: str
    source_type: SourceType
    permission_status: PermissionStatus
    license_notes: str | None
    availability_notes: str | None
    created_at: datetime
