from datetime import datetime

from app.extensions import db
from app.models.expense import Expense


class ExpenseRepository:

    # ----------------------------------------
    # GET ALL (search + optional pagination)
    # always returns: (items, pages)
    # ----------------------------------------
    @staticmethod
    def get_all(query=None, page=None, per_page=None):
        q = Expense.query

        # Search
        if query:
            search = f"%{query}%"
            q = q.filter(
                (Expense.expense_type.ilike(search)) |
                (Expense.description.ilike(search))
            )

        # Pagination
        if page and per_page:
            pag = q.order_by(Expense.id).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            return pag.items, pag.pages

        # Default non-paginated
        items = q.order_by(Expense.id).all()
        return items, 1

    # ----------------------------------------
    # GET BY ID
    # ----------------------------------------
    @staticmethod
    def get_by_id(expense_id):
        return Expense.query.get(expense_id)

    # ----------------------------------------
    # CREATE
    # ----------------------------------------
    @staticmethod
    def create(data):
        allowed = {"expense_type", "amount", "date", "description", "vehicle_id"}
        clean = {k: v for k, v in data.items() if k in allowed}

        # --- FIX: convert date string → datetime ---
        if "date" in clean and clean["date"]:
            clean["date"] = datetime.fromisoformat(clean["date"])

        # --- FIX: amount -> float ---
        if "amount" in clean and clean["amount"]:
            clean["amount"] = float(clean["amount"])

        # --- FIX: vehicle_id -> int ---
        if "vehicle_id" in clean and clean["vehicle_id"]:
            clean["vehicle_id"] = int(clean["vehicle_id"])

        expense = Expense(**clean)
        db.session.add(expense)
        db.session.commit()
        return expense

    # ----------------------------------------
    # UPDATE
    # ----------------------------------------
    @staticmethod
    def update(expense_id, data):
        expense = Expense.query.get(expense_id)
        if not expense:
            return None

        allowed = {"expense_type", "amount", "date", "description", "vehicle_id"}

        for k, v in data.items():
            if k not in allowed:
                continue

            # --- FIX: convert date ---
            if k == "date" and v:
                v = datetime.fromisoformat(v)

            # --- FIX: amount ---
            if k == "amount" and v:
                v = float(v)

            # --- FIX: vehicle_id ---
            if k == "vehicle_id" and v:
                v = int(v)

            setattr(expense, k, v)

        db.session.commit()
        return expense

    # ----------------------------------------
    # DELETE
    # ----------------------------------------
    @staticmethod
    def delete(expense_id):
        expense = Expense.query.get(expense_id)
        if expense:
            db.session.delete(expense)
            db.session.commit()
            return True
        return False
