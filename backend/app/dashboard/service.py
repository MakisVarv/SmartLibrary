from app.dashboard.repository import DashboardRepository


class DashboardService:

    def __init__(self, repository: DashboardRepository):

        self.repository = repository

    def get_dashboard(self):

        return {
            "total_books": self.repository.total_books(),
            "total_authors": self.repository.total_authors(),
            "total_categories": self.repository.total_categories(),
            "total_members": self.repository.total_members(),
            "available_books": self.repository.total_available(),
            "borrowed_books": self.repository.total_borrowed(),
            "overdue_books": self.repository.total_overdue(),
        }
