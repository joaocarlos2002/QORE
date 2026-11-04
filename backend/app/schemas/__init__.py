from app.schemas.board import BoardCreate, BoardRead
from app.schemas.common import ErrorDetail, ErrorResponse, Page
from app.schemas.exam import ExamCreate, ExamRead
from app.schemas.document import SourceDocumentRead
from app.schemas.source import SourceCreate, SourceRead

__all__ = [
    "BoardCreate",
    "BoardRead",
    "ErrorDetail",
    "ErrorResponse",
    "ExamCreate",
    "ExamRead",
    "SourceDocumentRead",
    "Page",
    "SourceCreate",
    "SourceRead",
]
