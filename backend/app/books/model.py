import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import Base

if TYPE_CHECKING:
    from app.authors.model import Author
    from app.categories.model import Category


class Book(Base):
    __tablename__ = "books"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    title: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    isbn: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    publication_year: Mapped[int] = mapped_column(Integer, nullable=False)
    pages: Mapped[int] = mapped_column(Integer, nullable=False)
    copies: Mapped[int] = mapped_column(Integer, nullable=False)
    available_copies: Mapped[int] = mapped_column(Integer, nullable=False)
    author_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("authors.id", ondelete="RESTRICT"),
        nullable=False,
    )
    author: Mapped["Author"] = relationship(
        "Author",
        back_populates="books",
    )

    category_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False,
    )
    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="books",
    )
    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
