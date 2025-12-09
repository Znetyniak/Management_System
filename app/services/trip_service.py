from app.repositories.trip_repository import TripRepository
from app.repositories.driver_repository import DriverRepository
from app.repositories.vehicle_repository import VehicleRepository


def _normalize_list(res):
    """res may be list OR (items, pages). Always returns list."""
    if isinstance(res, tuple) and len(res) == 2:
        return res[0]
    return res


def _normalize_paginated(res):
    """res may be list OR (items, pages). Always returns (items, pages)."""
    if isinstance(res, tuple) and len(res) == 2:
        return res
    return res, 1


class TripService:

    # ------------------------------------------------------
    # MAIN METHODS (Store/Admin)
    # ------------------------------------------------------
    @staticmethod
    def get_all(query=None, page=None, per_page=None):
        """
        Якщо page/per_page — повертає (items, pages)
        Якщо без пагінації — повертає список items
        """
        res = TripRepository.get_all(query=query, page=page, per_page=per_page)

        if page and per_page:
            # пагінований режим
            return _normalize_paginated(res)

        # простий список
        return _normalize_list(res)

    @staticmethod
    def get_by_id(tid):
        return TripRepository.get_by_id(tid)

    @staticmethod
    def create(data):
        driver = DriverRepository.get_by_id(data.get("driver_id"))
        if not driver:
            raise ValueError("Driver not found")

        vehicle = VehicleRepository.get_by_id(data.get("vehicle_id"))
        if not vehicle:
            raise ValueError("Vehicle not found")

        return TripRepository.create(data)

    @staticmethod
    def update(tid, data):
        return TripRepository.update(tid, data)

    @staticmethod
    def delete(tid):
        return TripRepository.delete(tid)

    # ------------------------------------------------------
    # DASHBOARD METRICS
    # ------------------------------------------------------
    @staticmethod
    def count_active():
        trips = TripService.get_all()  # ← ТЕПЕР ПОВЕРТАЄ СПИСОК
        active = [
            t for t in trips
            if not getattr(t, "distance_km", None) or t.distance_km == 0
        ]
        return len(active)

    # ------------------------------------------------------
    # BACKWARD COMPATIBILITY (залишаємо)
    # ------------------------------------------------------
    @staticmethod
    def get_all_trips():
        return TripService.get_all()

    @staticmethod
    def get_trip(tid):
        return TripService.get_by_id(tid)

    @staticmethod
    def create_trip(data):
        return TripService.create(data)

    @staticmethod
    def update_trip(tid, data):
        return TripService.update(tid, data)

    @staticmethod
    def delete_trip(tid):
        return TripService.delete(tid)
