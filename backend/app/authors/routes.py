# type: ignore
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.auth.authorization import permission_required
from app.authors.schema import (
    author_schema,
    authors_schema,
    create_author_schema,
    update_author_schema,
)
from app.authors.service import AuthorService
from app.extensions import SessionFactory

author_bp = Blueprint("authors", __name__, url_prefix="/api/authors")


@author_bp.get("/")
@jwt_required()
@permission_required("author.read")
def get_authors():
    with SessionFactory() as session:
        service = AuthorService(session)
        authors = service.get_authors()

        return authors_schema.dump(authors), 200


@author_bp.get("/<uuid:author_id>")
@jwt_required()
@permission_required("author.read")
def get_author(author_id):

    with SessionFactory() as session:
        service = AuthorService(session)

        author = service.get_author(author_id)

        return author_schema.dump(author)


@author_bp.post("/")
@jwt_required()
@permission_required("author.create")
def create_author():
    data = create_author_schema.load(request.get_json())

    with SessionFactory() as session:
        service = AuthorService(session)

        author = service.create_author(**data)

        return (
            author_schema.dump(author),
            201,
        )


@author_bp.patch("/<uuid:author_id>")
@jwt_required()
@permission_required("author.update")
def update_author(author_id):
    data = update_author_schema.load(request.get_json())

    with SessionFactory() as session:
        service = AuthorService(session)

        author = service.update_author(author_id, data)

        return author_schema.dump(author)


@author_bp.delete("/<uuid:author_id>")
@jwt_required()
@permission_required("author.delete")
def delete_author(author_id):

    with SessionFactory() as session:
        service = AuthorService(session)

        service.delete_author(author_id)

        return (
            {"message": "Author deleted successfully."},
            200,
        )
