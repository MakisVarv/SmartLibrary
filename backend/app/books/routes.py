# type: ignore
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.auth.authorization import permission_required
from app.books.schema import (
    book_schema,
    books_schema,
    create_book_schema,
    update_book_schema,
)
from app.books.service import BookService
from app.common.exceptions.bad_request import BadRequestException
from app.extensions import SessionFactory

book_bp = Blueprint("books", __name__, url_prefix="/api/books")


@book_bp.get("/")
@jwt_required()
@permission_required("book.read")
def get_books():
    page = request.args.get("page", default=1, type=int)
    page_size = request.args.get("page_size", default=10, type=int)
    search = request.args.get("search")

    if page < 1 or page_size < 1:
        raise BadRequestException("Page and page size must be greater than 0.")

    with SessionFactory() as session:
        service = BookService(session)

        books, pagination = service.get_books(
            page=page,
            page_size=page_size,
            search=search,
        )

        return {
            "items": books_schema.dump(books),
            "pagination": pagination,
        }, 200


@book_bp.get("/<uuid:book_id>")
@jwt_required()
@permission_required("book.read")
def get_book(book_id):

    with SessionFactory() as session:
        service = BookService(session)

        book = service.get_book(book_id)

        return book_schema.dump(book)


@book_bp.post("/")
@jwt_required()
@permission_required("book.create")
def create_book():
    data = create_book_schema.load(request.get_json())

    with SessionFactory() as session:
        service = BookService(session)

        book = service.create_book(**data)

        return (
            book_schema.dump(book),
            201,
        )


@book_bp.patch("/<uuid:book_id>")
@jwt_required()
@permission_required("book.update")
def update_book(book_id):
    data = update_book_schema.load(request.get_json())

    with SessionFactory() as session:
        service = BookService(session)

        book = service.update_book(book_id, data)

        return book_schema.dump(book)


@book_bp.delete("/<uuid:book_id>")
@jwt_required()
@permission_required("book.delete")
def delete_book(book_id):

    with SessionFactory() as session:
        service = BookService(session)

        service.delete_book(book_id)

        return (
            {"message": "Book deleted successfully."},
            200,
        )
