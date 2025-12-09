from app.extensions import db
from datetime import datetime

class Maintenance(db.Model):
    __tablename__ = 'maintenances'

    id = db.Column(db.Integer, primary_key=True)

    # Уникаємо "type" -> maintenance_type
    maintenance_type = db.Column(db.String(150), nullable=False)

    date = db.Column(db.DateTime, default=datetime.utcnow)
    next_date = db.Column(db.DateTime, nullable=True)

    # Foreign key
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)

    # ----------------------------------------------------
    # REPRESENTATION
    # ----------------------------------------------------
    def __repr__(self):
        return f"<Maintenance {self.maintenance_type} ({self.date})>"

    # ----------------------------------------------------
    # to_dict (для форм і редагування)
    # ----------------------------------------------------
    def to_dict(self):
        return {
            "id": self.id,
            "maintenance_type": self.maintenance_type,
            "date": self.date.strftime("%Y-%m-%d") if self.date else "",
            "next_date": self.next_date.strftime("%Y-%m-%d") if self.next_date else "",
            "vehicle_id": self.vehicle_id,
        }
