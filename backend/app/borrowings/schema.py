from marshmallow import Schema, ValidationError, fields, validates_schema

from app.books.schema import book_schema
from app.members.schema import member_schema


class BorrowingSchema(Schema):
    """Borrowing response schema."""

    id = fields.UUID()

    borrow_date = fields.Date()

    due_date = fields.Date()

    return_date = fields.Date(allow_none=True)

    status = fields.Function(serialize=lambda borrowing: borrowing.status.value)

    book = fields.Nested(book_schema)

    member = fields.Nested(member_schema)


class CreateBorrowingSchema(Schema):

    book_id = fields.UUID(required=True)

    member_id = fields.UUID(required=True)

    due_date = fields.Date(required=True)


class UpdateBorrowingSchema(Schema):

    due_date = fields.Date()

    @validates_schema
    def validate_not_empty(self, data, **kwargs):
        if not data:
            raise ValidationError("At least one field must be provided.")


borrowing_schema = BorrowingSchema()

borrowings_schema = BorrowingSchema(many=True)


create_borrowing_schema = CreateBorrowingSchema()


update_borrowing_schema = UpdateBorrowingSchema()
