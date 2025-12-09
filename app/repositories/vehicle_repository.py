from app.extensions import db
from app.models.vehicle import Vehicle


class VehicleRepository:

    # -------------------------------------------------
    # GET ALL (search + pagination)
    # -------------------------------------------------
    @staticmethod
    def get_all(query=None, page=None, per_page=None):
        q = Vehicle.query

        # SEARCH by brand / model / vin
        if query:
            search = f"%{query}%"
            q = q.filter(
                Vehicle.brand.ilike(search) |
                Vehicle.model.ilike(search) |
                Vehicle.vin.ilike(search)
            )

        # PAGINATION
        if page and per_page:
            pag = q.order_by(Vehicle.id).paginate(page=page, per_page=per_page, error_out=False)
            return pag.items, pag.pages

        # DEFAULT (without pagination)
        items = q.order_by(Vehicle.id).all()
        return items, 1

    # -------------------------------------------------
    # GET BY ID
    # -------------------------------------------------
    @staticmethod
    def get_by_id(vehicle_id):
        return Vehicle.query.get(vehicle_id)

    # -------------------------------------------------
    # CREATE
    # -------------------------------------------------
    @staticmethod
    def create(data):
        allowed = {"brand", "model", "year", "vin", "technical_state"}
        clean = {k: v for k, v in data.items() if k in allowed}

        vehicle = Vehicle(**clean)
        db.session.add(vehicle)
        db.session.commit()
        return vehicle

    # -------------------------------------------------
    # UPDATE
    # -------------------------------------------------
    @staticmethod
    def update(vehicle_id, data):
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return None

        allowed = {"brand", "model", "year", "vin", "technical_state"}
        for k, v in data.items():
            if k in allowed:
                setattr(vehicle, k, v)

        db.session.commit()
        return vehicle

    # -------------------------------------------------
    # DELETE
    # -------------------------------------------------
    @staticmethod
    def delete(vehicle_id):
        vehicle = Vehicle.query.get(vehicle_id)
        if vehicle:
            db.session.delete(vehicle)
            db.session.commit()
            return True
        return False
