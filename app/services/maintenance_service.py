from app.repositories.maintenance_repository import MaintenanceRepository
from app.repositories.vehicle_repository import VehicleRepository
import datetime


class MaintenanceService:

    # ------------------------------------------------------
    # MAIN METHODS (admin / store)
    # ------------------------------------------------------
    @staticmethod
    def get_all(query=None, page=None, per_page=None):
        """
        Повертає: (items, pages)
        Підтримує пошук + пагінацію.
        """
        return MaintenanceRepository.get_all(query=query, page=page, per_page=per_page)

    @staticmethod
    def get_by_id(mid):
        return MaintenanceRepository.get_by_id(mid)

    @staticmethod
    def create(data):
        """Створення ТО з перевіркою на існування транспортного засобу."""
        vehicle = VehicleRepository.get_by_id(data.get("vehicle_id"))
        if not vehicle:
            raise ValueError("Vehicle not found")

        return MaintenanceRepository.create(data)

    @staticmethod
    def update(mid, data):
        return MaintenanceRepository.update(mid, data)

    @staticmethod
    def delete(mid):
        return MaintenanceRepository.delete(mid)

    # ------------------------------------------------------
    # STATISTICS (dashboard)
    # ------------------------------------------------------
    @staticmethod
    def count_upcoming():
        """
        Рахує кількість ТО, дата яких у майбутньому.
        Працює з datetime або date.
        """
        maintenances, _ = MaintenanceRepository.get_all()  # <-- бере тільки items

        today = datetime.date.today()
        upcoming = 0

        for m in maintenances:
            next_date = m.next_date

            if not next_date:
                continue

            if isinstance(next_date, datetime.datetime):
                next_date = next_date.date()

            if next_date > today:
                upcoming += 1

        return upcoming

    # ------------------------------------------------------
    # BACKWARD COMPATIBILITY
    # ------------------------------------------------------
    @staticmethod
    def get_all_maintenance():
        maintenances, _ = MaintenanceRepository.get_all()
        return maintenances

    @staticmethod
    def get_maintenance(mid):
        return MaintenanceRepository.get_by_id(mid)

    @staticmethod
    def create_maintenance(data):
        return MaintenanceService.create(data)

    @staticmethod
    def update_maintenance(mid, data):
        return MaintenanceService.update(mid, data)

    @staticmethod
    def delete_maintenance(mid):
        return MaintenanceService.delete(mid)
