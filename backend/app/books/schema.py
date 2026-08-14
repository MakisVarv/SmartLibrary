from marshmallow import Schema, ValidationError, fields, validate, validates_schema

from app.authors.schema import author_schema
from app.categories.schema import category_schema


class BookSchema(Schema):
    """Book response schema."""

    id = fields.UUID()

    title = fields.String()

    isbn = fields.String()

    publication_year = fields.Integer()

    pages = fields.Integer()

    copies = fields.Integer()

    available_copies = fields.Integer()

    description = fields.String(allow_none=True)

    author = fields.Nested(author_schema)

    category = fields.Nested(category_schema)


class CreateBookSchema(Schema):

    title = fields.String(required=True, validate=validate.Length(min=1, max=50))

    isbn = fields.String(required=True, validate=validate.Length(min=1, max=50))

    publication_year = fields.Integer(required=True, validate=validate.Range(min=1))

    pages = fields.Integer(required=True, validate=validate.Range(min=1))

    copies = fields.Integer(required=True, validate=validate.Range(min=0))

    available_copies = fields.Integer(required=True, validate=validate.Range(min=0))

    description = fields.String(
        required=False, allow_none=True, validate=validate.Length(min=1, max=255)
    )
    author_id = fields.UUID(required=True)

    category_id = fields.UUID(required=True)


class UpdateBookSchema(Schema):

    title = fields.String(required=False, validate=validate.Length(min=1, max=50))

    isbn = fields.String(required=False, validate=validate.Length(min=1, max=50))

    publication_year = fields.Integer(required=False, validate=validate.Range(min=1))

    pages = fields.Integer(required=False, validate=validate.Range(min=1))

    copies = fields.Integer(required=False, validate=validate.Range(min=0))

    available_copies = fields.Integer(required=False, validate=validate.Range(min=0))

    description = fields.String(
        required=False, allow_none=True, validate=validate.Length(min=1, max=255)
    )
    author_id = fields.UUID(required=False)

    category_id = fields.UUID(required=False)

    @validates_schema
    def validate_not_empty(self, data, **kwargs):
        if not data:
            raise ValidationError("At least one field must be provided.")


book_schema = BookSchema()

books_schema = BookSchema(many=True)

create_book_schema = CreateBookSchema()

update_book_schema = UpdateBookSchema()
