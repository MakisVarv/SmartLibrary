from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.authors.model import Author
from app.books.model import Book
from app.borrowings.model import Borrowing, BorrowStatus
from app.categories.model import Category
from app.members.model import Member


class DashboardRepository:

    def __init__(self, session: Session):
        self.session = session

    def total_books(self):
        return self.session.scalar(select(func.count(Book.id)))

    def total_categories(self):
        return self.session.scalar(select(func.count(Category.id)))

    def total_members(self):
        return self.session.scalar(select(func.count(Member.id)))

    def total_authors(self):
        return self.session.scalar(select(func.count(Author.id)))

    def total_available(self):
        return self.session.scalar(select(func.sum(Book.available_copies))) or 0

    def total_borrowed(self):
        return (
            self.session.scalar(
                select(func.count(Borrowing.id)).where(
                    Borrowing.status == BorrowStatus.BORROWED
                )
            )
            or 0
        )

    def total_overdue(self):
        return (
            self.session.scalar(
                select(func.count(Borrowing.id)).where(
                    Borrowing.status == BorrowStatus.BORROWED,
                    Borrowing.due_date < date.today(),
                )
            )
        ) or 0
