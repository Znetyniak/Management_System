from app.repositories.vehicle_repository import VehicleRepository


class VehicleService:

    # ------------------------------------------------------
    # MAIN METHODS (використовують admin/store)
    # ------------------------------------------------------
    @staticmethod
    def get_all(query=None, page=None, per_page=None):
        """
        Повертає:
        - якщо page=None → просто список автомобілів
        - якщо page не None → (items, pages)
        """
        return VehicleRepository.get_all(query=query, page=page, per_page=per_page)

    @staticmethod
    def get_by_id(vid):
        return VehicleRepository.get_by_id(vid)

    @staticmethod
    def create(data):
        allowed = {"brand", "model", "year", "vin", "technical_state"}
        clean = {k: v for k, v in data.items() if k in allowed}
        return VehicleRepository.create(clean)

    @staticmethod
    def update(vid, data):
        allowed = {"brand", "model", "year", "vin", "technical_state"}
        clean = {k: v for k, v in data.items() if k in allowed}
        return VehicleRepository.update(vid, clean)

    @staticmethod
    def delete(vid):
        return VehicleRepository.delete(vid)

    # ------------------------------------------------------
    # BACKWARD COMPATIBILITY (старий код підтримується)
    # ------------------------------------------------------
    @staticmethod
    def get_all_vehicles():
        vehicles, _ = VehicleRepository.get_all()
        return vehicles

    @staticmethod
    def get_vehicle(vid):
        return VehicleRepository.get_by_id(vid)

    @staticmethod
    def create_vehicle(data):
        return VehicleService.create(data)

    @staticmethod
    def update_vehicle(vid, data):
        return VehicleService.update(vid, data)

    @staticmethod
    def delete_vehicle(vid):
        return VehicleService.delete(vid)
