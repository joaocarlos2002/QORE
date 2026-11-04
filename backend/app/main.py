from fastapi import FastAPI, Request

from app.auth import LocalAuthenticator


def create_app() -> FastAPI:
    app = FastAPI(title="QORE API", version="0.1.0")
    app.state.authenticator = LocalAuthenticator()

    @app.get("/api/v1/health", tags=["system"])
    async def health(request: Request) -> dict[str, str]:
        await app.state.authenticator.require_token(request)
        return {"status": "ok"}

    return app


app = create_app()
