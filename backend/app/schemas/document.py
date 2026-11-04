from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models import DocumentStatus


class SourceDocumentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source_id: int
    exam_id: int | None
    filename: str
    storage_path: str
    content_hash: str
    status: DocumentStatus
    collected_at: datetime | None
    created_at: datetime
