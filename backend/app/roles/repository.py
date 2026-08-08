import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import roles
from app.roles.model import Role


class RoleRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        statement = select(Role)
        return self.session.scalars(statement).all()

    def get_by_id(self, role_id: uuid.UUID):
        return self.session.get(Role, role_id)

    def create(self, role: Role):
        self.session.add(role)
        self.session.commit()
        self.session.refresh(role)
        return role
