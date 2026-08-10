# type: ignore
from flask import Blueprint, jsonify, request

from app.extensions import SessionFactory
from app.roles.schema import (
    add_permission_schema,
    create_role_schema,
    role_schema,
    roles_schema,
    update_role_schema,
)
from app.roles.service import RoleService

role_bp = Blueprint(
    "roles",
    __name__,
    url_prefix="/api/roles",
)


@role_bp.get("/")
def get_roles():
    with SessionFactory() as session:
        service = RoleService(session)
        roles = service.get_roles()

        return roles_schema.dump(roles), 200


@role_bp.get("/<uuid:role_id>")
def get_role(role_id):

    with SessionFactory() as session:
        service = RoleService(session)

        role = service.get_role(role_id)

        return jsonify(role_schema.dump(role))


@role_bp.post("/")
def create_role():

    data = create_role_schema.load(request.get_json())

    with SessionFactory() as session:
        service = RoleService(session)

        role = service.create_role(
            name=data["name"],
            description=data.get("description"),
        )

        return (
            jsonify(role_schema.dump(role)),
            201,
        )


@role_bp.patch("/<uuid:role_id>")
def update_role(role_id):

    data = update_role_schema.load(request.get_json())

    with SessionFactory() as session:
        service = RoleService(session)

        role = service.update_role(role_id, data)

        return jsonify(role_schema.dump(role))


@role_bp.delete("/<uuid:role_id>")
def delete_role(role_id):

    with SessionFactory() as session:
        service = RoleService(session)

        service.delete_role(role_id)

        return (
            jsonify({"message": "Role deleted successfully."}),
            200,
        )


@role_bp.post("/<uuid:role_id>/permissions")
def assign_permission(role_id):
    data = add_permission_schema.load(request.get_json())

    with SessionFactory() as session:
        service = RoleService(session)

        role = service.assign_permission(
            role_id,
            data["permission_id"],
        )

        return role_schema.dump(role), 200


@role_bp.delete("/<uuid:role_id>/permissions/<uuid:permission_id>")
def remove_permission(role_id, permission_id):
    with SessionFactory() as session:
        service = RoleService(session)

        role = service.remove_permission(role_id, permission_id)

        return role_schema.dump(role), 200
