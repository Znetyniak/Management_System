from datetime import datetime
from app.services.expense_service import ExpenseService


class ExpensesReport:

    @staticmethod
    def expenses_summary(start_date=None, end_date=None):
        """
        Формує зведення витрат:

        Повертає:
        - total_amount: загальна сума витрат
        - details: список витрат
        - count: кількість записів
        """

        expenses = ExpenseService.get_all()   # завжди повертає список
        report = []
        total_amount = 0

        def normalize_date(dt):
            """Гарантує що exp.date — datetime, а не строка."""
            if isinstance(dt, datetime):
                return dt
            if isinstance(dt, str):
                try:
                    return datetime.fromisoformat(dt)
                except:
                    return None
            return None

        # парсимо фільтри
        if isinstance(start_date, str):
            try: 
                start_date = datetime.fromisoformat(start_date)
            except:
                start_date = None

        if isinstance(end_date, str):
            try:
                end_date = datetime.fromisoformat(end_date)
            except:
                end_date = None

        for exp in expenses:

            exp_date = normalize_date(exp.date)

            # фільтр по датах
            if start_date and exp_date and exp_date < start_date:
                continue
            if end_date and exp_date and exp_date > end_date:
                continue

            report.append({
                "id": exp.id,
                "vehicle_id": exp.vehicle_id,
                "type": exp.expense_type,     # правильне поле
                "amount": exp.amount,
                "date": exp_date,
                "description": exp.description
            })

            total_amount += exp.amount or 0

        return {
            "total_amount": total_amount,
            "details": report,
            "count": len(report)
        }
