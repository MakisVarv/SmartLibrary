from flask import Blueprint
from flask_jwt_extended import jwt_required

from app.auth.authorization import permission_required
from app.dashboard.repository import DashboardRepository
from app.dashboard.service import DashboardService
from app.extensions import SessionFactory

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/api/dashboard",
)


@dashboard_bp.get("")
@jwt_required()
@permission_required("dashboard.read")
def get_dashboard():
    with SessionFactory() as session:
        repository = DashboardRepository(session)

        service = DashboardService(repository)

        dashboard = service.get_dashboard()
        return dashboard
