from marshmallow import Schema, ValidationError, fields, validates_schema


class AuthorSchema(Schema):
    """Author response schema."""

    id = fields.UUID()

    first_name = fields.String()

    last_name = fields.String()

    biography = fields.String(allow_none=True)

    country = fields.String(allow_none=True)

    birth_date = fields.Date(allow_none=True)


author_schema = AuthorSchema()

authors_schema = AuthorSchema(many=True)


class CreateAuthorSchema(Schema):
    """Schema used to create a author."""

    first_name = fields.String(required=True)

    last_name = fields.String(required=True)

    biography = fields.String(required=False, allow_none=True)

    country = fields.String(required=False, allow_none=True)

    birth_date = fields.Date(required=False, allow_none=True)


create_author_schema = CreateAuthorSchema()


class UpdateAuthorSchema(Schema):

    first_name = fields.String()

    last_name = fields.String()

    biography = fields.String(allow_none=True)

    country = fields.String(allow_none=True)

    birth_date = fields.Date(allow_none=True)

    @validates_schema
    def validate_not_empty(self, data, **kwargs):
        if not data:
            raise ValidationError("At least one field must be provided.")


update_author_schema = UpdateAuthorSchema()
