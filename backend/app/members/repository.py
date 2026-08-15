import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.members.model import Member


class MemberRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str) -> Member | None:

        stmt = select(Member).where(Member.email == email)

        return self.session.execute(stmt).scalar_one_or_none()

    def exists(self, email: str) -> bool:

        return self.get_by_email(email) is not None

    def get_all(self):
        statement = select(Member)
        return self.session.scalars(statement).all()

    def get_by_id(self, member_id: uuid.UUID):
        return self.session.get(Member, member_id)

    def create(self, member: Member):
        self.session.add(member)
        self.session.flush()
        self.session.refresh(member)
        return member

    def update(self, member: Member, data: dict) -> Member:

        allowed_fields = {
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "is_active",
        }

        for field, value in data.items():
            if field in allowed_fields:
                setattr(member, field, value)

        self.session.flush()
        self.session.refresh(member)

        return member

    def delete(self, member: Member) -> None:
        self.session.delete(member)
        self.session.flush()
