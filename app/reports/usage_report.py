from datetime import datetime
from app.services.vehicle_service import VehicleService
from app.services.trip_service import TripService


class UsageReport:

    @staticmethod
    def vehicle_utilization(start_date=None, end_date=None, vehicle_id=None):
        """
        Формує звіт по використанню авто.
        Фільтри:
        - start_date (YYYY-MM-DD)
        - end_date (YYYY-MM-DD)
        - vehicle_id (int)
        """

        # -------------------------------------------------
        # 1. Завантажуємо автомобілі
        # -------------------------------------------------
        raw = VehicleService.get_all()

        if isinstance(raw, tuple):     # (items, pages)
            vehicles = raw[0]
        else:
            vehicles = raw

        # -------------------------------------------------
        # 2. Завантажуємо всі поїздки одразу (ефективніше)
        # -------------------------------------------------
        all_trips = TripService.get_all_trips()

        # -------------------------------------------------
        # 3. Парсимо дати
        # -------------------------------------------------
        def parse_date(value):
            if not value:
                return None
            try:
                return datetime.fromisoformat(value)
            except Exception:
                return None

        start = parse_date(start_date)
        end = parse_date(end_date)

        report = []

        # -------------------------------------------------
        # 4. Формування звіту
        # -------------------------------------------------
        for v in vehicles:

            # Фільтр за авто
            if vehicle_id and str(v.id) != str(vehicle_id):
                continue

            # Вибираємо всі поїздки цього авто
            v_trips = [t for t in all_trips if t.vehicle_id == v.id]

            # Фільтрація по датах
            filtered_trips = []
            for t in v_trips:
                t_date = getattr(t, "date", None)

                # Перетворюємо str → datetime
                if isinstance(t_date, str):
                    try:
                        t_date = datetime.fromisoformat(t_date)
                    except:
                        t_date = None

                if start and t_date and t_date < start:
                    continue
                if end and t_date and t_date > end:
                    continue

                filtered_trips.append(t)

            # Загальна дистанція
            total_distance = sum((t.distance_km or 0) for t in filtered_trips)

            # Додаємо до звіту
            report.append({
                "vehicle_id": v.id,
                "brand": v.brand,
                "model": v.model,
                "vin": v.vin,
                "trip_count": len(filtered_trips),
                "total_distance": total_distance
            })

        return report
