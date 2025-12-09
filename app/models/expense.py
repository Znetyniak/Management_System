from app.extensions import db
from datetime import datetime

class Expense(db.Model):
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)

    # Краще уникати назви "type", використовуємо expense_type
    expense_type = db.Column(db.String(150), nullable=False)

    amount = db.Column(db.Float, nullable=False)

    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(255), nullable=True)

    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)

    def __repr__(self):
        return f"<Expense {self.expense_type} {self.amount}>"

    def to_dict(self):
        return {
            "id": self.id,
            "expense_type": self.expense_type,
            "amount": self.amount,
            "date": self.date.strftime('%Y-%m-%d') if self.date else "",
            "description": self.description,
            "vehicle_id": self.vehicle_id
        }
