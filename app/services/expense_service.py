from app.repositories.expense_repository import ExpenseRepository
from app.repositories.vehicle_repository import VehicleRepository
import datetime


class ExpenseService:

    # ------------------------------------------------------
    # MAIN METHODS (використовуються у контролерах)
    # ------------------------------------------------------
    @staticmethod
    def get_all(query=None, page=None, per_page=None):
        """
        Отримати витрати.
        Підтримка:
            - пошуку query
            - пагінації page / per_page
        Повертає: (items, pages)
        """
        return ExpenseRepository.get_all(query=query, page=page, per_page=per_page)

    @staticmethod
    def get_by_id(expense_id):
        return ExpenseRepository.get_by_id(expense_id)

    @staticmethod
    def create(data):
        """
        Створити витрату.
        Перевіряємо, чи існує автомобіль.
        """
        vehicle = VehicleRepository.get_by_id(data.get("vehicle_id"))
        if not vehicle:
            raise ValueError("Vehicle not found")

        return ExpenseRepository.create(data)

    @staticmethod
    def update(expense_id, data):
        return ExpenseRepository.update(expense_id, data)

    @staticmethod
    def delete(expense_id):
        return ExpenseRepository.delete(expense_id)

    @staticmethod
    def total_month():
        """
        Повертає суму витрат за поточний місяць.
        Використовується у Store Dashboard.
        """
        expenses, _ = ExpenseRepository.get_all()

        today = datetime.date.today()
        month = today.month
        year = today.year

        total = 0

        for e in expenses:
            date_field = getattr(e, "date", None)
            amount_field = getattr(e, "amount", 0)

            if not date_field:
                continue

            # Якщо дата — datetime → приводимо до date
            if isinstance(date_field, datetime.datetime):
                df = date_field.date()
            else:
                df = date_field

            # Порівнюємо
            if df.month == month and df.year == year:
                total += amount_field

        return total

    # ------------------------------------------------------
    # OLD METHODS (СУМІСНІСТЬ)
    # ------------------------------------------------------
    @staticmethod
    def get_all_expenses():
        expenses, _ = ExpenseRepository.get_all()
        return expenses

    @staticmethod
    def get_expense(eid):
        return ExpenseRepository.get_by_id(eid)

    @staticmethod
    def create_expense(data):
        return ExpenseService.create(data)

    @staticmethod
    def update_expense(eid, data):
        return ExpenseService.update(eid, data)

    @staticmethod
    def delete_expense(eid):
        return ExpenseService.delete(eid)
