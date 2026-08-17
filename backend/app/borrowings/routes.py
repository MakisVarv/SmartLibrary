# type: ignore
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.auth.authorization import permission_required
from app.borrowings.schema import (
    borrowing_schema,
    borrowings_schema,
    create_borrowing_schema,
    update_borrowing_schema,
)
from app.borrowings.service import BorrowingService
from app.extensions import SessionFactory

borrowing_bp = Blueprint("borrowings", __name__, url_prefix="/api/borrowings")


@borrowing_bp.get("/")
@jwt_required()
@permission_required("borrowing.read")
def get_borrowings():
    with SessionFactory() as session:
        service = BorrowingService(session)
        borrowings = service.get_borrowings()

        return borrowings_schema.dump(borrowings), 200


@borrowing_bp.get("/<uuid:borrowing_id>")
@jwt_required()
@permission_required("borrowing.read")
def get_borrowing(borrowing_id):

    with SessionFactory() as session:
        service = BorrowingService(session)

        borrowing = service.get_borrowing(borrowing_id)

        return borrowing_schema.dump(borrowing)


@borrowing_bp.post("/")
@jwt_required()
@permission_required("borrowing.create")
def create_borrowing():
    data = create_borrowing_schema.load(request.get_json())

    with SessionFactory() as session:
        service = BorrowingService(session)

        borrowing = service.create_borrowing(**data)

        return (
            borrowing_schema.dump(borrowing),
            201,
        )


@borrowing_bp.patch("/<uuid:borrowing_id>")
@jwt_required()
@permission_required("borrowing.update")
def update_borrowing(borrowing_id):
    data = update_borrowing_schema.load(request.get_json())

    with SessionFactory() as session:
        service = BorrowingService(session)

        borrowing = service.update_borrowing(borrowing_id, data)

        return borrowing_schema.dump(borrowing)


@borrowing_bp.delete("/<uuid:borrowing_id>")
@jwt_required()
@permission_required("borrowing.delete")
def delete_borrowing(borrowing_id):

    with SessionFactory() as session:
        service = BorrowingService(session)

        service.delete_borrowing(borrowing_id)

        return (
            {"message": "Borrowing deleted successfully."},
            200,
        )


@borrowing_bp.post("/<uuid:borrowing_id>/return")
@jwt_required()
@permission_required("borrowing.update")
def return_borrowing(borrowing_id):

    with SessionFactory() as session:
        service = BorrowingService(session)

        borrowing = service.return_book(borrowing_id)

        return borrowing_schema.dump(borrowing)
