import uuid

from sqlalchemy.orm import Session

from app.categories.model import Category
from app.categories.repository import CategoryRepository
from app.common.exceptions.base_exception import AppException
from app.common.exceptions.not_found import NotFoundException


class CategoryService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = CategoryRepository(session)

    def create_category(
        self,
        name: str,
        description: str | None = None,
    ) -> Category:

        if self.repository.exists(name):
            raise AppException("Category already exists.", 409)

        category = Category(
            name=name,
            description=description,
        )
        try:
            category = self.repository.create(category)
            self.session.commit()
            return category
        except Exception:
            self.session.rollback()
            raise

    def get_categories(self):

        return self.repository.get_all()

    def get_category(self, category_id):

        category = self.repository.get_by_id(category_id)

        if category is None:
            raise NotFoundException("Category")

        return category

    def update_category(self, category_id: uuid.UUID, data: dict) -> Category:
        category = self.get_category(category_id)
        if "name" in data:
            existing = self.repository.get_by_name(data["name"])
            if existing and existing.id != category.id:
                raise AppException("Category already exists.", 409)
        try:
            category = self.repository.update(category, data)
            self.session.commit()
            return category
        except Exception:
            self.session.rollback()
            raise

    def delete_category(self, category_id: uuid.UUID) -> None:
        category = self.get_category(category_id)

        try:
            self.repository.delete(category)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
