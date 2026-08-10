# type: ignore
from flask import Blueprint, jsonify, request

from app.extensions import SessionFactory
from app.permissions.schema import (
    create_permission_schema,
    permission_schema,
    permissions_schema,
    update_permission_schema,
)
from app.permissions.service import PermissionService

permission_bp = Blueprint(
    "permissions",
    __name__,
    url_prefix="/api/permissions",
)


@permission_bp.get("/")
def get_permissions():
    with SessionFactory() as session:
        service = PermissionService(session)
        permissions = service.get_permissions()

        return permissions_schema.dump(permissions), 200


@permission_bp.get("/<uuid:permission_id>")
def get_permission(permission_id):

    with SessionFactory() as session:
        service = PermissionService(session)

        permission = service.get_permission(permission_id)

        return jsonify(permission_schema.dump(permission))


@permission_bp.post("/")
def create_permission():

    data = create_permission_schema.load(request.get_json())

    with SessionFactory() as session:
        service = PermissionService(session)

        permission = service.create_permission(
            name=data["name"],
            description=data.get("description"),
        )

        return (
            jsonify(permission_schema.dump(permission)),
            201,
        )


@permission_bp.patch("/<uuid:permission_id>")
def update_permission(permission_id):

    data = update_permission_schema.load(request.get_json())

    with SessionFactory() as session:
        service = PermissionService(session)

        permission = service.update_permission(permission_id, data)

        return jsonify(permission_schema.dump(permission))


@permission_bp.delete("/<uuid:permission_id>")
def delete_permission(permission_id):

    with SessionFactory() as session:
        service = PermissionService(session)

        service.delete_permission(permission_id)

        return (
            jsonify({"message": "Permission deleted successfully."}),
            200,
        )
