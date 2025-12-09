from flask import Blueprint, jsonify, request
from app.services.vehicle_service import VehicleService
from app.services.driver_service import DriverService
from app.services.trip_service import TripService
from app.services.expense_service import ExpenseService
from app.services.maintenance_service import MaintenanceService
from app.reports.usage_report import UsageReport

api_bp = Blueprint("api", __name__, url_prefix="/api")

# ---------------------------------------------------------
# VEHICLES API
# ---------------------------------------------------------
@api_bp.get("/vehicles")
def api_get_vehicles():
    vehicles = VehicleService.get_all_drivers() if hasattr(VehicleService, "get_all_drivers") else VehicleService.get_all()
    vehicles = vehicles[0] if isinstance(vehicles, tuple) else vehicles

    return jsonify([
        {
            "id": v.id,
            "brand": v.brand,
            "model": v.model,
            "vin": v.vin,
            "year": v.year
        }
        for v in vehicles
    ])


@api_bp.get("/vehicles/<int:vid>")
def api_get_vehicle(vid):
    v = VehicleService.get_by_id(vid)
    if not v:
        return jsonify({"error": "Vehicle not found"}), 404

    return jsonify({
        "id": v.id,
        "brand": v.brand,
        "model": v.model,
        "vin": v.vin,
        "year": v.year
    })


@api_bp.post("/vehicles")
def api_create_vehicle():
    data = request.json
    new_vehicle = VehicleService.create(data)
    return jsonify({"status": "created", "id": new_vehicle.id})


# ---------------------------------------------------------
# DRIVERS API
# ---------------------------------------------------------
@api_bp.get("/drivers")
def api_get_drivers():
    drivers, _ = DriverService.get_all()
    return jsonify([
        {
            "id": d.id,
            "full_name": d.full_name,
            "license_number": d.license_number
        }
        for d in drivers
    ])


@api_bp.get("/drivers/<int:did>")
def api_get_driver(did):
    d = DriverService.get_by_id(did)
    if not d:
        return jsonify({"error": "Driver not found"}), 404
    return jsonify({
        "id": d.id,
        "full_name": d.full_name,
        "license_number": d.license_number
    })


# ---------------------------------------------------------
# TRIPS API
# ---------------------------------------------------------
@api_bp.get("/trips")
def api_get_trips():
    raw = TripService.get_all_trips()
    trips = raw[0] if isinstance(raw, tuple) else raw

    return jsonify([
        {
            "id": t.id,
            "vehicle_id": t.vehicle_id,
            "driver_id": t.driver_id,
            "distance": t.distance,
            "status": t.status
        }
        for t in trips
    ])


# ---------------------------------------------------------
# EXPENSES API
# ---------------------------------------------------------
@api_bp.get("/expenses")
def api_get_expenses():
    raw = ExpenseService.get_all()
    expenses = raw[0] if isinstance(raw, tuple) else raw

    return jsonify([
        {
            "id": e.id,
            "vehicle_id": e.vehicle_id,
            "amount": e.amount,
            "type": e.expense_type,
            "date": str(e.date)
        }
        for e in expenses
    ])


# ---------------------------------------------------------
# MAINTENANCE API
# ---------------------------------------------------------
@api_bp.get("/maintenance")
def api_get_maintenance():
    raw = MaintenanceService.get_all()
    maints = raw[0] if isinstance(raw, tuple) else raw

    return jsonify([
        {
            "id": m.id,
            "vehicle_id": m.vehicle_id,
            "type": m.maintenance_type,
            "date": str(m.date),
            "next_date": str(m.next_date)
        }
        for m in maints
    ])


# ---------------------------------------------------------
# REPORT — USAGE (MINIMAL REST REPORT)
# ---------------------------------------------------------
@api_bp.get("/reports/usage")
def api_report_usage():
    start = request.args.get("from")
    end = request.args.get("to")
    vehicle_id = request.args.get("vehicle_id")

    report = UsageReport.vehicle_utilization(
        start_date=start,
        end_date=end,
        vehicle_id=vehicle_id
    )

    return jsonify(report)
