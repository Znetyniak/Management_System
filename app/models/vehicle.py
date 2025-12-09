from app.extensions import db

class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(120), nullable=False)
    model = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    vin = db.Column(db.String(100), unique=True, nullable=False)
    technical_state = db.Column(db.String(255), nullable=False)

    # Relationships
    trips = db.relationship('Trip', backref='vehicle', cascade='all, delete-orphan', lazy=True)
    maintenances = db.relationship('Maintenance', backref='vehicle', cascade='all, delete-orphan', lazy=True)
    expenses = db.relationship('Expense', backref='vehicle', cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return f"<Vehicle {self.brand} {self.model} ({self.vin})>"

    def to_dict(self):
        """
        Використовується у формах редагування (edit_car.html)
        """
        return {
            "id": self.id,
            "brand": self.brand,
            "model": self.model,
            "year": self.year,
            "vin": self.vin,
            "technical_state": self.technical_state
        }
