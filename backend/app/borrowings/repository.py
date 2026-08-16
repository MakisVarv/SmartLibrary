import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.borrowings.model import Borrowing


class BorrowingRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        statement = select(Borrowing)
        return self.session.scalars(statement).all()

    def get_by_id(self, borrowing_id: uuid.UUID):
        return self.session.get(Borrowing, borrowing_id)

    def create(self, borrowing: Borrowing):
        self.session.add(borrowing)
        self.session.flush()
        self.session.refresh(borrowing)
        return borrowing

    def update(self, borrowing: Borrowing, data: dict) -> Borrowing:

        allowed_fields = {
            "due_date",
        }

        for field, value in data.items():
            if field in allowed_fields:
                setattr(borrowing, field, value)

        self.session.flush()
        self.session.refresh(borrowing)

        return borrowing

    def delete(self, borrowing: Borrowing) -> None:
        self.session.delete(borrowing)
        self.session.flush()
