import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.authors.model import Author


class AuthorRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        statement = select(Author)
        return self.session.scalars(statement).all()

    def get_by_id(self, author_id: uuid.UUID):
        return self.session.get(Author, author_id)

    def create(self, author: Author):
        self.session.add(author)
        self.session.flush()
        self.session.refresh(author)
        return author

    def update(self, author: Author, data: dict) -> Author:

        allowed_fields = {
            "first_name",
            "last_name",
            "biography",
            "country",
            "birth_date",
        }

        for field, value in data.items():
            if field in allowed_fields:
                setattr(author, field, value)

        self.session.flush()
        self.session.refresh(author)

        return author

    def delete(self, author: Author) -> None:
        self.session.delete(author)
        self.session.flush()
