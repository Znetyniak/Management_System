from app.extensions import db
from app.models.driver import Driver


class DriverRepository:

    # ----------------------------------------
    # GET ALL (search + optional pagination)
    # always returns: (items, pages)
    # ----------------------------------------
    @staticmethod
    def get_all(query=None, page=None, per_page=None):
        q = Driver.query

        # Search
        if query:
            search = f"%{query}%"
            q = q.filter(
                Driver.full_name.ilike(search)
            )

        # Pagination mode
        if page and per_page:
            pag = q.order_by(Driver.id).paginate(page=page, per_page=per_page, error_out=False)
            return pag.items, pag.pages

        # Default non-paginated
        items = q.order_by(Driver.id).all()
        return items, 1

    # ----------------------------------------
    # GET BY ID
    # ----------------------------------------
    @staticmethod
    def get_by_id(driver_id):
        return Driver.query.get(driver_id)

    # ----------------------------------------
    # CREATE
    # ----------------------------------------
    @staticmethod
    def create(data):
        allowed = {"full_name", "license_number", "experience_years", "medical_check"}
        clean = {k: v for k, v in data.items() if k in allowed}

        driver = Driver(**clean)
        db.session.add(driver)
        db.session.commit()
        return driver

    # ----------------------------------------
    # UPDATE
    # ----------------------------------------
    @staticmethod
    def update(driver_id, data):
        driver = Driver.query.get(driver_id)
        if not driver:
            return None

        allowed = {"full_name", "license_number", "experience_years", "medical_check"}
        for k, v in data.items():
            if k in allowed:
                setattr(driver, k, v)

        db.session.commit()
        return driver

    # ----------------------------------------
    # DELETE
    # ----------------------------------------
    @staticmethod
    def delete(driver_id):
        driver = Driver.query.get(driver_id)
        if driver:
            db.session.delete(driver)
            db.session.commit()
            return True
        return False
