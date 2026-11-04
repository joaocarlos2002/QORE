from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Board


class DuplicateBoardError(ValueError):
    """Raised when a board name is already registered."""


class BoardRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self) -> list[Board]:
        statement = select(Board).order_by(Board.name)
        return list(self.session.scalars(statement))

    def create(self, name: str) -> Board:
        board = Board(name=name)
        self.session.add(board)
        try:
            self.session.flush()
        except IntegrityError as exc:
            self.session.rollback()
            raise DuplicateBoardError(name) from exc
        return board
