import uuid

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import or_

from app.books.model import Book


class BookRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_all(
        self,
        page: int = 1,
        page_size: int = 10,
        search: str | None = None,
    ):
        offset = (page - 1) * page_size

        statement = select(Book)

        if search:
            pattern = f"%{search.strip()}%"

            statement = statement.where(
                or_(
                    Book.title.ilike(pattern),
                    Book.isbn.ilike(pattern),
                )
            )

        statement = (
            statement.order_by(Book.title, Book.id).offset(offset).limit(page_size)
        )

        return self.session.scalars(statement).all()

    def count(self, search: str | None = None):
        statement = select(func.count(Book.id))
        if search:
            pattern = f"%{search.strip()}%"

            statement = statement.where(
                or_(
                    Book.title.ilike(pattern),
                    Book.isbn.ilike(pattern),
                )
            )
        return self.session.scalar(statement) or 0

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
