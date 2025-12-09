import os
from datetime import datetime, timedelta

from app import create_app
from app.extensions import db

from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.models.trip import Trip
from app.models.expense import Expense
from app.models.maintenance import Maintenance


# -----------------------------------------------------
# CREATE APP + CONTEXT
# -----------------------------------------------------
app = create_app()
app.app_context().push()


# -----------------------------------------------------
# RESET DATABASE
# -----------------------------------------------------
def reset_db():
    db_path = os.path.join(os.path.dirname(__file__), "fleet_management.db")

    if os.path.exists(db_path):
        os.remove(db_path)
        print("🗑 Removed old database")

    db.create_all()
    print("📦 Created new database schema")


# -----------------------------------------------------
# SEED FUNCTION
# -----------------------------------------------------
def seed():

    print("\n🔄 Resetting database...")
    reset_db()

    # -------------------------------------------------
    # USERS
    # -------------------------------------------------
    admin = User(
        full_name="Admin",
        email="i.znetyniak.o@gmail.com",
        password="12398745a",
        role="admin"
    )

    user = User(
        full_name="Regular User",
        email="user@example.com",
        password="user12345",
        role="user"
    )

    db.session.add_all([admin, user])
    db.session.commit()
    print("👑 Added admin + user")

    # -------------------------------------------------
    # VEHICLES
    # -------------------------------------------------
    v1 = Vehicle(
        brand="Toyota",
        model="Corolla",
        year=2018,
        vin="VIN0001",
        technical_state="Good"
    )

    v2 = Vehicle(
        brand="BMW",
        model="X5",
        year=2020,
        vin="VIN0002",
        technical_state="Excellent"
    )

    db.session.add_all([v1, v2])
    db.session.commit()
    print("🚗 Added vehicles")

    # -------------------------------------------------
    # DRIVERS
    # -------------------------------------------------
    d1 = Driver(
        full_name="John Doe",
        license_number="LIC1001",
        experience_years=5,
        medical_check="2024-05-01"
    )

    d2 = Driver(
        full_name="Alex Smith",
        license_number="LIC1002",
        experience_years=2,
        medical_check="2024-03-20"
    )

    db.session.add_all([d1, d2])
    db.session.commit()
    print("👷 Added drivers")

    # -------------------------------------------------
    # TRIPS
    # -------------------------------------------------
    t1 = Trip(
        date=datetime.utcnow(),
        route="Madrid → Barcelona",
        distance_km=620,
        vehicle_id=v1.id,
        driver_id=d1.id
    )

    t2 = Trip(
        date=datetime.utcnow() - timedelta(days=2),
        route="Valencia → Madrid",
        distance_km=350,
        vehicle_id=v2.id,
        driver_id=d2.id
    )

    db.session.add_all([t1, t2])
    db.session.commit()
    print("🛣 Added trips")

    # -------------------------------------------------
    # EXPENSES
    # -------------------------------------------------
    e1 = Expense(
        expense_type="Fuel",
        amount=50.0,
        date=datetime.utcnow(),
        description="Gasoline refill",
        vehicle_id=v1.id
    )

    e2 = Expense(
        expense_type="Service",
        amount=120.0,
        date=datetime.utcnow() - timedelta(days=5),
        description="Oil change",
        vehicle_id=v2.id
    )

    db.session.add_all([e1, e2])
    db.session.commit()
    print("💰 Added expenses")

    # -------------------------------------------------
    # MAINTENANCE
    # -------------------------------------------------
    m1 = Maintenance(
        maintenance_type="Oil change",
        date=datetime.utcnow() - timedelta(days=30),
        next_date=datetime.utcnow() + timedelta(days=60),
        vehicle_id=v1.id
    )

    m2 = Maintenance(
        maintenance_type="Tire rotation",
        date=datetime.utcnow() - timedelta(days=10),
        next_date=datetime.utcnow() + timedelta(days=90),
        vehicle_id=v2.id
    )

    db.session.add_all([m1, m2])
    db.session.commit()
    print("🔧 Added maintenance")

    print("\n✅ DONE! Database successfully seeded.\n")


# -----------------------------------------------------
# RUN
# -----------------------------------------------------
if __name__ == "__main__":
    seed()
