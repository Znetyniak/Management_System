from app.extensions import db
from datetime import datetime

class Trip(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    route = db.Column(db.String(255), nullable=False)
    distance_km = db.Column(db.Float, nullable=True)

    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=False)

    # RELATIONSHIPS ARE IN VEHICLE AND DRIVER MODELS

    # ----------------------------------------------------
    # REPRESENTATION
    # ----------------------------------------------------
    def __repr__(self):
        return f"<Trip {self.route} ({self.date})>"

    # ----------------------------------------------------
    # to_dict (для форм і редагування)
    # ----------------------------------------------------
    def to_dict(self):
        return {
            "id": self.id,
            "route": self.route,
            "distance_km": self.distance_km if self.distance_km is not None else "",
            "date": self.date.strftime("%Y-%m-%d") if self.date else "",
            "vehicle_id": self.vehicle_id,
            "driver_id": self.driver_id,
        }
