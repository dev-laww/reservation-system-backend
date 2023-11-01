from ..repositories import AnalyticsRepository


class AnalyticsController:
    repo = AnalyticsRepository()

    def get_all_payments(self, year: int, month: int):
        """
        Get all analytics.

        :return: list of analytics.
        """
        return self.repo.get_all_payments(year, month)
