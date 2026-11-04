from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models import ProcessingRecord, ProcessingStatus
from app.modules.jobs.state import JobStateMachine


class JobManager:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, stage: str, document_id: int | None = None) -> ProcessingRecord:
        record = ProcessingRecord(
            document_id=document_id,
            stage=stage,
            status=ProcessingStatus.PENDING,
            progress=0,
            attempt=0,
        )
        self.session.add(record)
        self.session.flush()
        return record

    def start(self, record: ProcessingRecord) -> ProcessingRecord:
        JobStateMachine.transition(record.status, ProcessingStatus.RUNNING)
        record.status = ProcessingStatus.RUNNING
        record.attempt += 1
        record.started_at = datetime.now(timezone.utc)
        return record

    def update_progress(self, record: ProcessingRecord, progress: int) -> ProcessingRecord:
        if record.status is not ProcessingStatus.RUNNING:
            raise ValueError("Only running jobs can update progress")
        if not 0 <= progress <= 100:
            raise ValueError("progress must be between 0 and 100")
        record.progress = progress
        return record

    def finish(
        self,
        record: ProcessingRecord,
        status: ProcessingStatus,
        message: str | None = None,
    ) -> ProcessingRecord:
        JobStateMachine.transition(record.status, status)
        record.status = status
        record.progress = 100 if status is ProcessingStatus.COMPLETED else record.progress
        record.message = message
        record.finished_at = datetime.now(timezone.utc)
        return record
