from app.repositories.driver_repository import DriverRepository


class DriverService:

    # ------------------------------------------------------
    # MAIN METHODS (використовуються в контролерах)
    # ------------------------------------------------------
    @staticmethod
    def get_all(query=None, page=None, per_page=None):
        """
        Повертає водіїв.
        Підтримує:
            - пошук (query)
            - пагінацію (page, per_page)
        Повертає:
            (items, total_pages)
        """
        return DriverRepository.get_all(query=query, page=page, per_page=per_page)

    @staticmethod
    def get_by_id(driver_id):
        return DriverRepository.get_by_id(driver_id)

    @staticmethod
    def create(data):
        return DriverRepository.create(data)

    @staticmethod
    def update(driver_id, data):
        return DriverRepository.update(driver_id, data)

    @staticmethod
    def delete(driver_id):
        return DriverRepository.delete(driver_id)

    # ------------------------------------------------------
    # BACKWARD COMPATIBILITY (старі методи)
    # ------------------------------------------------------
    @staticmethod
    def get_all_drivers():
        drivers, _ = DriverRepository.get_all()
        return drivers

    @staticmethod
    def get_driver(did):
        return DriverRepository.get_by_id(did)

    @staticmethod
    def create_driver(data):
        return DriverRepository.create(data)

    @staticmethod
    def update_driver(did, data):
        return DriverRepository.update(did, data)

    @staticmethod
    def delete_driver(did):
        return DriverRepository.delete(did)
