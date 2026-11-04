from fastapi import FastAPI, Request

from app.auth import LocalAuthenticator
from app.api import boards_router, documents_router, exams_router, sources_router


def create_app() -> FastAPI:
    app = FastAPI(title="QORE API", version="0.1.0")
    app.state.authenticator = LocalAuthenticator()
    app.include_router(boards_router)
    app.include_router(exams_router)
    app.include_router(documents_router)
    app.include_router(sources_router)

    @app.get("/api/v1/health", tags=["system"])
    async def health(request: Request) -> dict[str, str]:
        await app.state.authenticator.require_token(request)
        return {"status": "ok"}

    return app


app = create_app()
