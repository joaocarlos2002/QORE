from app.api.boards import router as boards_router
from app.api.exams import router as exams_router
from app.api.sources import router as sources_router

__all__ = ["boards_router", "exams_router", "sources_router"]
