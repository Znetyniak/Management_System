from app.extensions import db
from app.models.maintenance import Maintenance
from datetime import datetime


class MaintenanceRepository:

    # -------------------------------------------------
    # INTERNAL HELPERS
    # -------------------------------------------------
    @staticmethod
    def _parse_date(value):
        """Приймає строку '2025-10-20' → datetime або None."""
        if not value:
            return None

        if isinstance(value, datetime):
            return value

        try:
            return datetime.strptime(value, "%Y-%m-%d")
        except:
            return None

    # -------------------------------------------------
    # GET ALL
    # -------------------------------------------------
    @staticmethod
    def get_all(query=None, page=None, per_page=None):
        q = Maintenance.query

        if query:
            search = f"%{query}%"
            q = q.filter(Maintenance.maintenance_type.ilike(search))

        q = q.order_by(Maintenance.id)

        if page and per_page:
            pag = q.paginate(page=page, per_page=per_page, error_out=False)
            return pag.items, pag.pages

        items = q.all()
        return items, 1

    # -------------------------------------------------
    # GET BY ID
    # -------------------------------------------------
    @staticmethod
    def get_by_id(mid):
        return Maintenance.query.get(mid)

    # -------------------------------------------------
    # CREATE
    # -------------------------------------------------
    @staticmethod
    def create(data):
        allowed = {"maintenance_type", "date", "next_date", "vehicle_id"}
        clean = {k: v for k, v in data.items() if k in allowed}

        # Convert dates
        clean["date"] = MaintenanceRepository._parse_date(clean.get("date"))
        clean["next_date"] = MaintenanceRepository._parse_date(clean.get("next_date"))

        # Convert vehicle_id to int
        if "vehicle_id" in clean and clean["vehicle_id"]:
            clean["vehicle_id"] = int(clean["vehicle_id"])

        # Validate maintenance_type
        if not clean.get("maintenance_type"):
            raise ValueError("Maintenance type is required.")

        m = Maintenance(**clean)
        db.session.add(m)
        db.session.commit()
        return m

    # -------------------------------------------------
    # UPDATE
    # -------------------------------------------------
    @staticmethod
    def update(mid, data):
        m = Maintenance.query.get(mid)
        if not m:
            return None

        allowed = {"maintenance_type", "date", "next_date", "vehicle_id"}

        for k, v in data.items():
            if k not in allowed:
                continue

            if k in ("date", "next_date"):
                v = MaintenanceRepository._parse_date(v)

            if k == "vehicle_id" and v:
                v = int(v)

            setattr(m, k, v)

        db.session.commit()
        return m

    # -------------------------------------------------
    # DELETE
    # -------------------------------------------------
    @staticmethod
    def delete(mid):
        m = Maintenance.query.get(mid)
        if m:
            db.session.delete(m)
            db.session.commit()
            return True
        return False
