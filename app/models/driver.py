from app.extensions import db

class Driver(db.Model):
    __tablename__ = 'drivers'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    license_number = db.Column(db.String(100), unique=True, nullable=False)
    experience_years = db.Column(db.Integer, nullable=False)
    medical_check = db.Column(db.String(120), nullable=False)   # або Date — як захочеш

    # Зв’язок з Trip
    trips = db.relationship(
        'Trip',
        backref='driver',
        cascade='all, delete-orphan',
        lazy=True
    )

    # ----------------------------------------------------
    # STRING REPRESENTATION
    # ----------------------------------------------------
    def __repr__(self):
        return f"<Driver {self.full_name} | License {self.license_number}>"

    # ----------------------------------------------------
    # to_dict (для форм, редагування, JSON)
    # ----------------------------------------------------
    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "license_number": self.license_number,
            "experience_years": self.experience_years,
            "medical_check": self.medical_check,
        }
