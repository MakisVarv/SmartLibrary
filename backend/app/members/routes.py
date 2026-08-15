# type: ignore
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.auth.authorization import permission_required
from app.extensions import SessionFactory
from app.members.schema import (
    create_member_schema,
    member_schema,
    members_schema,
    update_member_schema,
)
from app.members.service import MemberService

member_bp = Blueprint("members", __name__, url_prefix="/api/members")


@member_bp.get("/")
@jwt_required()
@permission_required("member.read")
def get_members():
    with SessionFactory() as session:
        service = MemberService(session)
        members = service.get_members()

        return members_schema.dump(members), 200


@member_bp.get("/<uuid:member_id>")
@jwt_required()
@permission_required("member.read")
def get_member(member_id):

    with SessionFactory() as session:
        service = MemberService(session)

        member = service.get_member(member_id)

        return member_schema.dump(member)


@member_bp.post("/")
@jwt_required()
@permission_required("member.create")
def create_member():
    data = create_member_schema.load(request.get_json())

    with SessionFactory() as session:
        service = MemberService(session)

        member = service.create_member(**data)

        return (
            member_schema.dump(member),
            201,
        )


@member_bp.patch("/<uuid:member_id>")
@jwt_required()
@permission_required("member.update")
def update_member(member_id):
    data = update_member_schema.load(request.get_json())

    with SessionFactory() as session:
        service = MemberService(session)

        member = service.update_member(member_id, data)

        return member_schema.dump(member)


@member_bp.delete("/<uuid:member_id>")
@jwt_required()
@permission_required("member.delete")
def delete_member(member_id):

    with SessionFactory() as session:
        service = MemberService(session)

        service.delete_member(member_id)

        return (
            {"message": "Member deleted successfully."},
            200,
        )
