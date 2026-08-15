import uuid

from sqlalchemy.orm import Session

from app.common.exceptions.bad_request import BadRequestException
from app.common.exceptions.not_found import NotFoundException
from app.members.model import Member
from app.members.repository import MemberRepository


class MemberService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = MemberRepository(session)

    def create_member(
        self,
        first_name: str,
        last_name: str,
        email: str,
        address: str | None = None,
        phone: str | None = None,
    ) -> Member:

        if self.repository.get_by_email(email):
            raise BadRequestException("Email already exists.")

        member = Member(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
        )
        try:

            member = self.repository.create(member)
            self.session.commit()
            return member

        except Exception:

            self.session.rollback()
            raise

    def get_members(self):

        return self.repository.get_all()

    def get_member(self, member_id):

        member = self.repository.get_by_id(member_id)

        if member is None:
            raise NotFoundException("Member")

        return member

    def update_member(self, member_id, data: dict):
        """Update an existing member."""

        member = self.get_member(member_id)

        if "email" in data:
            existing = self.repository.get_by_email(data["email"])

            if existing and existing.id != member.id:
                raise BadRequestException("Email already exists.")

        try:
            member = self.repository.update(member, data)
            self.session.commit()
            return member
        except Exception:
            self.session.rollback()
            raise

    def delete_member(self, member_id: uuid.UUID) -> None:
        member = self.get_member(member_id)

        try:
            self.repository.delete(member)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
