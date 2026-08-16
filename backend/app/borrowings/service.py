import datetime
import uuid
from typing import Sequence

from sqlalchemy.orm import Session

from app.books.repository import BookRepository
from app.borrowings.model import Borrowing, BorrowStatus
from app.borrowings.repository import BorrowingRepository
from app.common.exceptions.bad_request import BadRequestException
from app.common.exceptions.not_found import NotFoundException
from app.members.repository import MemberRepository


class BorrowingService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = BorrowingRepository(session)
        self.member_repository = MemberRepository(session)
        self.book_repository = BookRepository(session)

    def get_borrowings(self) -> Sequence[Borrowing]:

        return self.repository.get_all()

    def get_borrowing(self, borrowing_id) -> Borrowing:

        borrowing = self.repository.get_by_id(borrowing_id)

        if borrowing is None:
            raise NotFoundException("Borrowing")
        return borrowing

    def create_borrowing(self, book_id, member_id, due_date) -> Borrowing:
        book = self.book_repository.get_by_id(book_id)
        member = self.member_repository.get_by_id(member_id)
        if book is None:
            raise NotFoundException("Book")
        if member is None:
            raise NotFoundException("Member")
        if book.available_copies == 0:
            raise BadRequestException("No copies available")
        if due_date <= datetime.date.today():
            raise BadRequestException("Due date must be after borrow date.")
        if not member.is_active:
            raise BadRequestException("Not an active member")

        borrowing = Borrowing(member_id=member_id, book_id=book_id, due_date=due_date)
        try:
            borrowing = self.repository.create(borrowing)
            book.available_copies -= 1
            self.session.commit()
            return borrowing

        except Exception:

            self.session.rollback()
            raise

    def update_borrowing(self, borrowing_id, data: dict) -> Borrowing:
        """Update an existing borrowing."""
        borrowing = self.get_borrowing(borrowing_id)
        if "due_date" in data and data["due_date"] <= borrowing.borrow_date:
            raise BadRequestException("Due date must be after borrow date.")
        if borrowing.status == BorrowStatus.RETURNED:
            raise BadRequestException("Book is already returned")
        try:
            borrowing = self.repository.update(borrowing, data)
            self.session.commit()
            return borrowing
        except Exception:
            self.session.rollback()
            raise

    def delete_borrowing(self, borrowing_id: uuid.UUID) -> None:
        borrowing = self.get_borrowing(borrowing_id)

        try:
            self.repository.delete(borrowing)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

    def return_book(self, borrowing_id):
        borrowing = self.get_borrowing(borrowing_id)
        book = self.book_repository.get_by_id(borrowing.book_id)
        if borrowing.status == BorrowStatus.RETURNED:
            raise BadRequestException("Book is already returned")

        try:
            borrowing.status = BorrowStatus.RETURNED
            borrowing.return_date = datetime.date.today()
            if book:
                book.available_copies += 1
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
