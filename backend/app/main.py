from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title="QORE API", version="0.1.0")

    @app.get("/api/v1/health", tags=["system"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
