from app.models import ProcessingStatus


class InvalidJobTransition(ValueError):
    """Raised when a processing job changes state illegally."""


class JobStateMachine:
    _transitions = {
        ProcessingStatus.PENDING: {
            ProcessingStatus.RUNNING,
            ProcessingStatus.CANCELLED,
        },
        ProcessingStatus.RUNNING: {
            ProcessingStatus.COMPLETED,
            ProcessingStatus.FAILED,
            ProcessingStatus.CANCELLED,
        },
        ProcessingStatus.FAILED: {ProcessingStatus.PENDING},
        ProcessingStatus.COMPLETED: set(),
        ProcessingStatus.CANCELLED: set(),
    }

    @classmethod
    def transition(
        cls, current: ProcessingStatus, target: ProcessingStatus
    ) -> ProcessingStatus:
        if target not in cls._transitions[current]:
            raise InvalidJobTransition(f"{current.value} -> {target.value}")
        return target
