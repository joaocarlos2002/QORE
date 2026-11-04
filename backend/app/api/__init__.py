from app.api.boards import router as boards_router
from app.api.answer_keys import router as answer_keys_router
from app.api.exams import router as exams_router
from app.api.documents import router as documents_router
from app.api.sources import router as sources_router

__all__ = [
    "answer_keys_router",
    "boards_router",
    "documents_router",
    "exams_router",
    "sources_router",
]
