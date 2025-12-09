from datetime import datetime

from app.extensions import db
from app.models.trip import Trip


class TripRepository:

    # -------------------------------------------------
    # GET ALL (search + pagination)
    # -------------------------------------------------
    @staticmethod
    def get_all(query=None, page=None, per_page=None):
        q = Trip.query

        # SEARCH by route
        if query:
            search = f"%{query}%"
            q = q.filter(Trip.route.ilike(search))

        # PAGINATION mode
        if page and per_page:
            pag = q.order_by(Trip.id).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            return pag.items, pag.pages

        # DEFAULT mode
        items = q.order_by(Trip.id).all()
        return items, 1

    # -------------------------------------------------
    # GET BY ID
    # -------------------------------------------------
    @staticmethod
    def get_by_id(trip_id):
        return Trip.query.get(trip_id)

    # -------------------------------------------------
    # CREATE
    # -------------------------------------------------
    @staticmethod
    def create(data):
        allowed = {"date", "route", "distance_km", "vehicle_id", "driver_id"}
        clean = {k: v for k, v in data.items() if k in allowed}

        # --- FIX: convert string → datetime ---
        if "date" in clean and clean["date"]:
            clean["date"] = datetime.fromisoformat(clean["date"])

        # --- Convert numeric fields ---
        if "distance_km" in clean and clean["distance_km"]:
            clean["distance_km"] = float(clean["distance_km"])

        if "vehicle_id" in clean and clean["vehicle_id"]:
            clean["vehicle_id"] = int(clean["vehicle_id"])

        if "driver_id" in clean and clean["driver_id"]:
            clean["driver_id"] = int(clean["driver_id"])

        trip = Trip(**clean)
        db.session.add(trip)
        db.session.commit()
        return trip

    # -------------------------------------------------
    # UPDATE
    # -------------------------------------------------
    @staticmethod
    def update(trip_id, data):
        trip = Trip.query.get(trip_id)
        if not trip:
            return None

        allowed = {"date", "route", "distance_km", "vehicle_id", "driver_id"}

        for k, v in data.items():
            if k not in allowed:
                continue

            # --- FIX: convert date string to datetime ---
            if k == "date" and v:
                v = datetime.fromisoformat(v)

            # --- Fix number fields ---
            if k == "distance_km" and v:
                v = float(v)

            if k == "vehicle_id" and v:
                v = int(v)

            if k == "driver_id" and v:
                v = int(v)

            setattr(trip, k, v)

        db.session.commit()
        return trip

    # -------------------------------------------------
    # DELETE
    # -------------------------------------------------
    @staticmethod
    def delete(trip_id):
        trip = Trip.query.get(trip_id)
        if trip:
            db.session.delete(trip)
            db.session.commit()
            return True
        return False
