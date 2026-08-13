from marshmallow import Schema, ValidationError, fields, validate, validates_schema


class CategorySchema(Schema):
    """Category response schema."""

    id = fields.UUID()

    name = fields.String()

    description = fields.String(allow_none=True)


class CreateCategorySchema(Schema):

    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=50),
    )

    description = fields.String(
        required=False,
        allow_none=True,
        validate=validate.Length(min=1, max=255),
    )


class UpdateCategorySchema(Schema):
    name = fields.String(
        required=False,
        validate=validate.Length(min=1, max=50),
    )

    description = fields.String(
        required=False,
        allow_none=True,
        validate=validate.Length(min=1, max=255),
    )

    @validates_schema
    def validate_not_empty(self, data, **kwargs):
        if "name" not in data and "description" not in data:
            raise ValidationError("At least one field must be provided.")


category_schema = CategorySchema()

categories_schema = CategorySchema(many=True)

create_category_schema = CreateCategorySchema()

update_category_schema = UpdateCategorySchema()
