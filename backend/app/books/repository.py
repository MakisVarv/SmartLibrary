import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.books.model import Book


class BookRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        statement = select(Book)
        return self.session.scalars(statement).all()

    def get_by_id(self, book_id: uuid.UUID):
        return self.session.get(Book, book_id)

    def get_by_isbn(self, isbn: str):

        stmt = select(Book).where(Book.isbn == isbn)

        return self.session.execute(stmt).scalar_one_or_none()

    def create(self, book: Book):
        self.session.add(book)
        self.session.flush()
        self.session.refresh(book)
        return book

    def update(self, book: Book, data: dict) -> Book:

        allowed_fields = {
            "title",
            "isbn",
            "publication_year",
            "pages",
            "copies",
            "description",
            "available_copies",
            "author_id",
            "category_id",
        }

        for field, value in data.items():
            if field in allowed_fields:
                setattr(book, field, value)

        self.session.flush()
        self.session.refresh(book)

        return book

    def delete(self, book: Book) -> None:
        self.session.delete(book)
        self.session.flush()
