from app.associations import role_permissions
from app.roles.model import Role
from app.roles.routes import role_bp
from app.roles.service import RoleService

__all__ = [
    "Role",
    "RoleService",
    "role_bp",
    "role_permissions",
]
