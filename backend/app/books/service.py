import uuid
from datetime import date
from typing import Sequence

from sqlalchemy.orm import Session

from app.authors.repository import AuthorRepository
from app.books.model import Book
from app.books.repository import BookRepository
from app.categories.repository import CategoryRepository
from app.common.exceptions.bad_request import BadRequestException
from app.common.exceptions.not_found import NotFoundException


class BookService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = BookRepository(session)
        self.category_repository = CategoryRepository(session)
        self.author_repository = AuthorRepository(session)

    def create_book(
        self,
        title: str,
        isbn: str,
        publication_year: int,
        pages: int,
        copies: int,
        available_copies: int,
        category_id: uuid.UUID,
        author_id: uuid.UUID,
        description: str | None = None,
    ) -> Book:
        existing = self.repository.get_by_isbn(isbn)
        if existing:
            raise BadRequestException("This ISBN already exists.")
        if self.author_repository.get_by_id(author_id) is None:
            raise NotFoundException("Author")
        if self.category_repository.get_by_id(category_id) is None:
            raise NotFoundException("Category")
        if publication_year > date.today().year:
            raise BadRequestException("Publication year cannot be in the future.")
        if available_copies > copies:
            raise BadRequestException("Available copies cannot exceed total copies.")
        book = Book(
            title=title,
            isbn=isbn,
            publication_year=publication_year,
            pages=pages,
            copies=copies,
            available_copies=available_copies,
            category_id=category_id,
            author_id=author_id,
            description=description,
        )

        try:
            book = self.repository.create(book)
            self.session.commit()
            return book

        except Exception:

            self.session.rollback()
            raise

    def get_books(self) -> Sequence[Book]:

        return self.repository.get_all()

    def get_book(self, book_id) -> Book:

        book = self.repository.get_by_id(book_id)

        if book is None:
            raise NotFoundException("Book")

        return book

    def update_book(self, book_id, data: dict) -> Book:
        """Update an existing book."""

        book = self.get_book(book_id)
        if "isbn" in data:
            existing = self.repository.get_by_isbn(data["isbn"])
            if existing and existing.id != book.id:
                raise BadRequestException("This ISBN already exists.")

        if (
            "author_id" in data
            and self.author_repository.get_by_id(data["author_id"]) is None
        ):
            raise NotFoundException("Author")
        if (
            "category_id" in data
            and self.category_repository.get_by_id(data["category_id"]) is None
        ):
            raise NotFoundException("Category")
        if "publication_year" in data and data["publication_year"] > date.today().year:
            raise BadRequestException("Publication year cannot be in the future.")
        new_copies = data.get("copies", book.copies)
        new_available = data.get("available_copies", book.available_copies)

        if new_available > new_copies:
            raise BadRequestException("Available copies cannot exceed total copies.")
        try:
            book = self.repository.update(book, data)
            self.session.commit()
            return book
        except Exception:
            self.session.rollback()
            raise

    def delete_book(self, book_id: uuid.UUID) -> None:
        book = self.get_book(book_id)

        try:
            self.repository.delete(book)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
