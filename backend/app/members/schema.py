from marshmallow import Schema, ValidationError, fields, validates_schema


class MemberSchema(Schema):
    """Member response schema."""

    id = fields.UUID()

    first_name = fields.String()

    last_name = fields.String()

    email = fields.Email()

    phone = fields.String(allow_none=True)

    is_active = fields.Boolean()

    address = fields.String(allow_none=True)

    registration_date = fields.DateTime()


member_schema = MemberSchema()

members_schema = MemberSchema(many=True)


class CreateMemberSchema(Schema):
    """Schema used to create a member."""

    first_name = fields.String(required=True)

    last_name = fields.String(required=True)

    email = fields.Email(required=True)

    address = fields.String(allow_none=True)

    phone = fields.String(
        required=False,
        allow_none=True,
    )


create_member_schema = CreateMemberSchema()


class UpdateMemberSchema(Schema):

    first_name = fields.String()
    last_name = fields.String()
    email = fields.Email()

    address = fields.String(allow_none=True)

    phone = fields.String(
        allow_none=True,
    )

    is_active = fields.Boolean()

    @validates_schema
    def validate_not_empty(self, data, **kwargs):
        if not data:
            raise ValidationError("At least one field must be provided.")


update_member_schema = UpdateMemberSchema()
