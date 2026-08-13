# type: ignore
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.auth.authorization import permission_required
from app.categories.schema import (
    categories_schema,
    category_schema,
    create_category_schema,
    update_category_schema,
)
from app.categories.service import CategoryService
from app.extensions import SessionFactory

category_bp = Blueprint(
    "categories",
    __name__,
    url_prefix="/api/categories",
)


@category_bp.get("/")
@jwt_required()
@permission_required("category.read")
def get_categories():
    with SessionFactory() as session:
        service = CategoryService(session)
        categories = service.get_categories()

        return categories_schema.dump(categories), 200


@category_bp.get("/<uuid:category_id>")
@jwt_required()
@permission_required("category.read")
def get_category(category_id):

    with SessionFactory() as session:
        service = CategoryService(session)

        category = service.get_category(category_id)

        return category_schema.dump(category)


@category_bp.post("/")
@jwt_required()
@permission_required("category.create")
def create_category():

    data = create_category_schema.load(request.get_json())

    with SessionFactory() as session:
        service = CategoryService(session)

        category = service.create_category(
            name=data["name"],
            description=data.get("description"),
        )

        return (
            category_schema.dump(category),
            201,
        )


@category_bp.patch("/<uuid:category_id>")
@jwt_required()
@permission_required("category.update")
def update_category(category_id):

    data = update_category_schema.load(request.get_json())

    with SessionFactory() as session:
        service = CategoryService(session)

        category = service.update_category(category_id, data)

        return category_schema.dump(category)


@category_bp.delete("/<uuid:category_id>")
@jwt_required()
@permission_required("category.delete")
def delete_category(category_id):

    with SessionFactory() as session:
        service = CategoryService(session)

        service.delete_category(category_id)

        return (
            {"message": "Category deleted successfully."},
            200,
        )
