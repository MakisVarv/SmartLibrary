# type: ignore
import os

from sqlalchemy import select

from app.permissions.model import Permission
from app.roles.model import Role
from app.users.repository import UserRepository
from app.users.service import UserService

PERMISSIONS = [
    {"name": "book.read", "description": "Read book information"},
    {"name": "book.create", "description": "Create books"},
    {"name": "book.update", "description": "Update books"},
    {"name": "book.delete", "description": "Delete books"},
    {"name": "member.read", "description": "Read member information"},
    {"name": "member.create", "description": "Create members"},
    {"name": "member.update", "description": "Update members"},
    {"name": "member.delete", "description": "Delete members"},
    {"name": "borrowing.read", "description": "Read borrowing information"},
    {"name": "borrowing.create", "description": "Create borrowings"},
    {"name": "borrowing.update", "description": "Update borrowings"},
    {"name": "borrowing.delete", "description": "Delete borrowings"},
    {"name": "dashboard.read", "description": "View dashboard"},
]
ROLES = [
    {
        "name": "Admin",
        "description": "Full system administrator",
    },
    {
        "name": "Librarian",
        "description": "Manages books, members, and borrowings",
    },
    {
        "name": "Member",
        "description": "Standard library member",
    },
]
ROLE_PERMISSIONS = {
    "Admin": [permission["name"] for permission in PERMISSIONS],
    "Librarian": [
        "book.read",
        "book.create",
        "book.update",
        "book.delete",
        "member.read",
        "member.create",
        "member.update",
        "member.delete",
        "borrowing.read",
        "borrowing.create",
        "borrowing.update",
        "borrowing.delete",
        "dashboard.read",
    ],
    "Member": [
        "book.read",
        "borrowing.read",
    ],
}


def seed_permissions(session):

    print("Starting permission seed...")

    for permission in PERMISSIONS:

        print(permission["name"])

        existing = session.scalar(
            select(Permission).where(Permission.name == permission["name"])
        )

        if existing:
            print(f"{permission['name']} already exists")
            continue

        print(f"Adding {permission['name']}")

        session.add(
            Permission(name=permission["name"], description=permission["description"])
        )

    session.commit()

    print("Commit completed.")


def seed_roles(session):
    print("Starting roles seed")
    for role in ROLES:

        print(role["name"])

        existing = session.scalar(select(Role).where(Role.name == role["name"]))

        if existing:
            print(f"{role['name']} already exists")
            continue

        print(f"Adding {role['name']}")

        session.add(Role(name=role["name"], description=role["description"]))

    session.commit()

    print("Commit completed.")


def seed_role_permissions(session):
    print("Starting role-permission seed...")

    for role_name, permission_names in ROLE_PERMISSIONS.items():
        role = session.scalar(select(Role).where(Role.name == role_name))

        if role is None:
            raise RuntimeError(f"Role '{role_name}' does not exist.")

        existing_permissions = {permission.name for permission in role.permissions}

        for permission_name in permission_names:
            if permission_name in existing_permissions:
                print(f"{role_name} already has {permission_name}")
                continue

            permission = session.scalar(
                select(Permission).where(Permission.name == permission_name)
            )

            if permission is None:
                raise RuntimeError(f"Permission '{permission_name}' does not exist.")

            print(f"Assigning {permission_name} to {role_name}")
            role.permissions.append(permission)

    session.commit()
    print("Role-permission commit completed.")


def seed_admin(session):
    print("Starting admin seed...")

    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")
    first_name = os.getenv("ADMIN_FIRST_NAME", "System")
    last_name = os.getenv("ADMIN_LAST_NAME", "Admin")

    if not email or not password:
        raise RuntimeError("ADMIN_EMAIL and ADMIN_PASSWORD must be configured.")

    user_repository = UserRepository(session)

    existing = user_repository.get_by_email(email)

    if existing:
        print("Admin user already exists.")
        return

    admin_role = session.scalar(select(Role).where(Role.name == "Admin"))

    if admin_role is None:
        raise RuntimeError("Admin role does not exist.")

    user_service = UserService(session)

    user_service.create_user(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        role_id=admin_role.id,
    )

    print("Admin user created.")


if __name__ == "__main__":
    from app.extensions import SessionFactory

    with SessionFactory() as session:
        seed_permissions(session)
        seed_roles(session)
        seed_role_permissions(session)
        seed_admin(session)
