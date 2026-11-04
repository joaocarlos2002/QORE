from collections.abc import Generator
from pathlib import Path
import os

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


def _database_url() -> str:
    return os.environ.get(
        "QORE_DATABASE_URL",
        f"sqlite:///{Path.home() / 'AppData' / 'Local' / 'QuestionEngine' / 'database' / 'qore.db'}",
    )


def create_database_engine() -> Engine:
    url = _database_url()
    if url.startswith("sqlite:///"):
        Path(url.removeprefix("sqlite:///")).parent.mkdir(parents=True, exist_ok=True)
    return create_engine(url, connect_args={"check_same_thread": False})


engine = create_database_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
