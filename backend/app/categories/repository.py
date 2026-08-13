import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.categories.model import Category


class CategoryRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_name(self, name: str) -> Category | None:

        stmt = select(Category).where(Category.name == name)

        return self.session.execute(stmt).scalar_one_or_none()

    def exists(self, name: str) -> bool:

        return self.get_by_name(name) is not None

    def get_all(self):
        statement = select(Category)
        return self.session.scalars(statement).all()

    def get_by_id(self, category_id: uuid.UUID):
        return self.session.get(Category, category_id)

    def create(self, category: Category):
        self.session.add(category)
        self.session.flush()
        self.session.refresh(category)
        return category

    def update(self, category: Category, data: dict) -> Category:
        if "name" in data:
            category.name = data["name"]

        if "description" in data:
            category.description = data["description"]

        self.session.flush()
        self.session.refresh(category)

        return category

    def delete(self, category: Category) -> None:
        self.session.delete(category)
        self.session.flush()
