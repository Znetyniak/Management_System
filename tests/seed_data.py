from app import create_app
from app.extensions import db

from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.models.trip import Trip
from app.models.expense import Expense
from app.models.maintenance import Maintenance

from datetime import datetime, timedelta


app = create_app()

with app.app_context():

    # Очистка бази перед заповненням (опціонально)
    db.drop_all()
    db.create_all()

    # --------------------------
    #  VEHICLES
    # --------------------------
    vehicles = [
        Vehicle(brand="BMW", model="X5", year=2018, vin="BMWX5VIN123", technical_state="Good"),
        Vehicle(brand="Audi", model="A6", year=2020, vin="AUDIA61234", technical_state="Excellent"),
        Vehicle(brand="Mercedes", model="GLE", year=2019, vin="MBGLE9988", technical_state="Good"),
        Vehicle(brand="Toyota", model="Corolla", year=2017, vin="TOYCRL5511", technical_state="Normal"),
        Vehicle(brand="Ford", model="Transit", year=2016, vin="FDTRN9912", technical_state="Needs service"),
    ]

    db.session.add_all(vehicles)
    db.session.commit()

    # --------------------------
    #  DRIVERS
    # --------------------------
    drivers = [
        Driver(full_name="John Doe", license_number="DR12345", experience_years=5, medical_check="2024-01-10"),
        Driver(full_name="Alice Cooper", license_number="DR98211", experience_years=3, medical_check="2023-12-05"),
        Driver(full_name="Bob Marley", license_number="DR55229", experience_years=7, medical_check="2024-06-12"),
        Driver(full_name="Emma Stone", license_number="DR12888", experience_years=2, medical_check="2023-10-22"),
    ]

    db.session.add_all(drivers)
    db.session.commit()

    # --------------------------
    #  TRIPS
    # --------------------------
    trips = [
        Trip(route="Madrid → Barcelona", distance_km=620, vehicle_id=1, driver_id=1),
        Trip(route="Madrid → Valencia", distance_km=350, vehicle_id=2, driver_id=2),
        Trip(route="Barcelona → Girona", distance_km=110, vehicle_id=3, driver_id=3),
        Trip(route="Sevilla → Malaga", distance_km=205, vehicle_id=4, driver_id=4),
    ]

    db.session.add_all(trips)
    db.session.commit()

    # --------------------------
    #  EXPENSES
    # --------------------------
    expenses = [
        Expense(type="Fuel", amount=120.50, vehicle_id=1),
        Expense(type="Repair", amount=350.00, vehicle_id=3),
        Expense(type="Insurance", amount=500.00, vehicle_id=2),
        Expense(type="Fuel", amount=75.20, vehicle_id=4),
        Expense(type="Maintenance", amount=200.00, vehicle_id=5),
    ]

    db.session.add_all(expenses)
    db.session.commit()

    # --------------------------
    #  MAINTENANCE
    # --------------------------
    maint_list = [
        Maintenance(type="Oil change", date=datetime.now(), next_date=datetime.now() + timedelta(days=180), vehicle_id=1),
        Maintenance(type="Brake check", date=datetime.now(), next_date=datetime.now() + timedelta(days=90), vehicle_id=2),
        Maintenance(type="Tire replacement", date=datetime.now(), next_date=datetime.now() + timedelta(days=365), vehicle_id=3),
    ]

    db.session.add_all(maint_list)
    db.session.commit()

    print("Тестові дані успішно додані!")
