import uuid
from datetime import date

from sqlalchemy.orm import Session

from app.authors.model import Author
from app.authors.repository import AuthorRepository
from app.common.exceptions.not_found import NotFoundException


class AuthorService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = AuthorRepository(session)

    def create_author(
        self,
        first_name: str,
        last_name: str,
        biography: str | None = None,
        country: str | None = None,
        birth_date: date | None = None,
    ) -> Author:

        author = Author(
            first_name=first_name,
            last_name=last_name,
            biography=biography,
            country=country,
            birth_date=birth_date,
        )
        try:

            author = self.repository.create(author)
            self.session.commit()
            return author

        except Exception:

            self.session.rollback()
            raise

    def get_authors(self):

        return self.repository.get_all()

    def get_author(self, author_id):

        author = self.repository.get_by_id(author_id)

        if author is None:
            raise NotFoundException("Author")

        return author

    def update_author(self, author_id, data: dict):
        """Update an existing author."""

        author = self.get_author(author_id)

        try:
            author = self.repository.update(author, data)
            self.session.commit()
            return author
        except Exception:
            self.session.rollback()
            raise

    def delete_author(self, author_id: uuid.UUID) -> None:
        author = self.get_author(author_id)

        try:
            self.repository.delete(author)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
