import uuid
from datetime import date
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import Base

if TYPE_CHECKING:
    from app.books.model import Book
    from app.members.model import Member


class BorrowStatus(str, Enum):
    BORROWED = "BORROWED"
    RETURNED = "RETURNED"


class Borrowing(Base):
    __tablename__ = "borrowings"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    borrow_date: Mapped[date] = mapped_column(
        Date(),
        server_default=func.current_date(),
        nullable=False,
    )

    due_date: Mapped[date] = mapped_column(
        Date(),
        nullable=False,
    )

    return_date: Mapped[date | None] = mapped_column(
        Date(),
        nullable=True,
    )

    status: Mapped[BorrowStatus] = mapped_column(
        SQLEnum(BorrowStatus),
        default=BorrowStatus.BORROWED,
        nullable=False,
    )
    member_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("members.id", ondelete="RESTRICT"),
        nullable=False,
    )
    member: Mapped["Member"] = relationship(
        "Member",
        back_populates="borrowings",
    )
    book_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("books.id", ondelete="RESTRICT"),
        nullable=False,
    )
    book: Mapped["Book"] = relationship(
        "Book",
        back_populates="borrowings",
    )
