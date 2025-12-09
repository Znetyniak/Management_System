from app.services.maintenance_service import MaintenanceService
from datetime import datetime


class MaintenanceReport:

    @staticmethod
    def maintenance_summary(start_date=None, end_date=None, vehicle_id=None, type_filter=None):
        """
        Формує повний звіт ТО з фільтрами:
        - start_date, end_date   — фільтр по даті
        - vehicle_id             — фільтр по авто
        - type_filter            — фільтр по типу ТО

        Повертає:
        - records       → список ТО
        - count         → кількість записів
        - per_vehicle   → ТО по авто
        - per_type      → ТО по типах
        """

        raw = MaintenanceService.get_all()
        maint = raw[0] if isinstance(raw, tuple) else raw   # <-- CRITICAL FIX

        # ---- safe date parser ----
        def parse_date(v):
            if not v:
                return None
            try:
                return datetime.fromisoformat(str(v))
            except:
                return None

        start = parse_date(start_date)
        end = parse_date(end_date)

        records = []
        per_vehicle = {}
        per_type = {}

        for m in maint:

            # ----- Фільтр по авто -----
            if vehicle_id and str(m.vehicle_id) != str(vehicle_id):
                continue

            # ----- Фільтр по типу -----
            if type_filter and m.maintenance_type != type_filter:
                continue

            # ----- Фільтр по даті -----
            m_date = parse_date(m.date)

            if start and m_date and m_date < start:
                continue
            if end and m_date and m_date > end:
                continue

            record = {
                "id": m.id,
                "vehicle_id": m.vehicle_id,
                "type": m.maintenance_type,
                "date": m.date,
                "next_date": m.next_date,
                "description": getattr(m, "description", "")
            }

            records.append(record)

            # статистика по авто
            per_vehicle[m.vehicle_id] = per_vehicle.get(m.vehicle_id, 0) + 1

            # статистика по типах ТО
            per_type[m.maintenance_type] = per_type.get(m.maintenance_type, 0) + 1

        return {
            "records": records,
            "count": len(records),
            "per_vehicle": per_vehicle,
            "per_type": per_type
        }
