# app/controllers/admin_controller.py
from flask import render_template, request, redirect, url_for, flash, session
from functools import wraps

from app.controllers import admin_bp

# Services
from app.services.vehicle_service import VehicleService
from app.services.driver_service import DriverService
from app.services.trip_service import TripService
from app.services.expense_service import ExpenseService
from app.services.maintenance_service import MaintenanceService


# -------------------------------------------------------
#   ADMIN ACCESS DECORATOR
# -------------------------------------------------------
def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Login required!", "warning")
            return redirect(url_for("auth.login"))

        if session.get("role") != "admin":
            flash("Access denied!", "danger")
            return redirect(url_for("store.dashboard"))

        return func(*args, **kwargs)
    return wrapper


# -------------------------------------------------------
#   UNIVERSAL HELPERS
# -------------------------------------------------------

def _normalize_list(res):
    """res may be list OR (items, pages). Always returns list."""
    if isinstance(res, tuple) and len(res) == 2:
        return res[0]
    return res


def _normalize_paginated(res):
    """res may be list OR (items, pages). Always returns (items, pages)."""
    if isinstance(res, tuple) and len(res) == 2:
        return res
    return res, 1


# -------------------------------------------------------
#   ADMIN DASHBOARD
# -------------------------------------------------------
@admin_bp.route("/dashboard")
@admin_only
def dashboard():
    return render_template("Admin/dashboard.html")


# =======================================================
#   VEHICLES CRUD + BULK DELETE
# =======================================================
@admin_bp.route("/manage_cars")
@admin_only
def manage_cars():
    q = request.args.get("q", "")
    page = request.args.get("page", 1, type=int)
    per_page = 10

    res = VehicleService.get_all(q, page, per_page)
    vehicles, pages = _normalize_paginated(res)

    return render_template(
        "Admin/manage_cars.html",
        vehicles=vehicles,
        q=q,
        page=page,
        pages=pages,
    )


@admin_bp.route("/add_car", methods=["GET", "POST"])
@admin_only
def add_car():
    if request.method == "POST":
        try:
            VehicleService.create(request.form)
            flash("Vehicle created!", "success")
            return redirect(url_for("admin.manage_cars"))
        except Exception as e:
            flash(f"Error creating vehicle: {e}", "danger")

    return render_template("Admin/add_car.html", form={})


@admin_bp.route("/edit_car/<int:vid>", methods=["GET", "POST"])
@admin_only
def edit_car(vid):
    vehicle = VehicleService.get_by_id(vid)

    if request.method == "POST":
        try:
            VehicleService.update(vid, request.form)
            flash("Vehicle updated!", "success")
            return redirect(url_for("admin.manage_cars"))
        except Exception as e:
            flash(f"Error updating vehicle: {e}", "danger")

    form = vehicle.to_dict() if vehicle else {}
    return render_template("Admin/edit_car.html", vehicle=vehicle, form=form)


@admin_bp.route("/delete_car/<int:vid>", methods=["POST"])
@admin_only
def delete_car(vid):
    try:
        VehicleService.delete(vid)
        flash("Vehicle deleted!", "danger")
    except Exception as e:
        flash(f"Error deleting vehicle: {e}", "danger")
    return redirect(url_for("admin.manage_cars"))


# --------------------------
# BULK DELETE (Delete selected)
# --------------------------
@admin_bp.route("/delete_selected_cars", methods=["POST"])
@admin_only
def delete_selected_cars():
    ids = request.form.get("ids", "")
    id_list = [i for i in ids.split(",") if i.isdigit()]

    if not id_list:
        flash("No vehicles selected.", "warning")
        return redirect(url_for("admin.manage_cars"))

    deleted = 0
    for vid in id_list:
        if VehicleService.delete(vid):
            deleted += 1

    flash(f"Deleted {deleted} vehicle(s).", "success")
    return redirect(url_for("admin.manage_cars"))


# =======================================================
#   DRIVERS CRUD
# =======================================================
@admin_bp.route("/manage_drivers")
@admin_only
def manage_drivers():
    drivers = _normalize_list(DriverService.get_all())
    return render_template("Admin/manage_drivers.html", drivers=drivers)


@admin_bp.route("/add_driver", methods=["GET", "POST"])
@admin_only
def add_driver():
    if request.method == "POST":
        try:
            DriverService.create(request.form)
            flash("Driver added!", "success")
            return redirect(url_for("admin.manage_drivers"))
        except Exception as e:
            flash(f"Error adding driver: {e}", "danger")

    return render_template("Admin/add_driver.html")


@admin_bp.route("/edit_driver/<int:did>", methods=["GET", "POST"])
@admin_only
def edit_driver(did):
    driver = DriverService.get_by_id(did)

    if request.method == "POST":
        try:
            DriverService.update(did, request.form)
            flash("Driver updated!", "success")
            return redirect(url_for("admin.manage_drivers"))
        except Exception as e:
            flash(f"Error updating driver: {e}", "danger")

    return render_template(
        "Admin/edit_driver.html",
        driver=driver,
        form=driver.to_dict() if driver else {},
    )


# =======================================================
#   TRIPS CRUD
# =======================================================
@admin_bp.route("/manage_trips")
@admin_only
def manage_trips():
    trips = _normalize_list(TripService.get_all())
    return render_template("Admin/manage_trips.html", trips=trips)


@admin_bp.route("/add_trip", methods=["GET", "POST"])
@admin_only
def add_trip():
    vehicles = _normalize_list(VehicleService.get_all())
    drivers = _normalize_list(DriverService.get_all())

    if request.method == "POST":
        try:
            TripService.create(request.form)
            flash("Trip added!", "success")
            return redirect(url_for("admin.manage_trips"))
        except Exception as e:
            flash(f"Error adding trip: {e}", "danger")

    return render_template("Admin/add_trip.html", vehicles=vehicles, drivers=drivers)


@admin_bp.route("/edit_trip/<int:tid>", methods=["GET", "POST"])
@admin_only
def edit_trip(tid):
    trip = TripService.get_by_id(tid)

    vehicles = _normalize_list(VehicleService.get_all())
    drivers = _normalize_list(DriverService.get_all())

    if request.method == "POST":
        try:
            TripService.update(tid, request.form)
            flash("Trip updated!", "success")
            return redirect(url_for("admin.manage_trips"))
        except Exception as e:
            flash(f"Error updating trip: {e}", "danger")

    return render_template(
        "Admin/edit_trip.html",
        trip=trip,
        vehicles=vehicles,
        drivers=drivers,
        form=trip.to_dict() if trip else {},
    )


# =======================================================
#   EXPENSES CRUD
# =======================================================
@admin_bp.route("/manage_expenses")
@admin_only
def manage_expenses():
    expenses = _normalize_list(ExpenseService.get_all())
    return render_template("Admin/manage_expenses.html", expenses=expenses)


@admin_bp.route("/add_expense", methods=["GET", "POST"])
@admin_only
def add_expense():
    vehicles = _normalize_list(VehicleService.get_all())

    if request.method == "POST":
        try:
            ExpenseService.create(request.form)
            flash("Expense added!", "success")
            return redirect(url_for("admin.manage_expenses"))
        except Exception as e:
            flash(f"Error adding expense: {e}", "danger")

    return render_template("Admin/add_expense.html", vehicles=vehicles)


@admin_bp.route("/edit_expense/<int:eid>", methods=["GET", "POST"])
@admin_only
def edit_expense(eid):
    expense = ExpenseService.get_by_id(eid)
    vehicles = _normalize_list(VehicleService.get_all())

    if request.method == "POST":
        try:
            ExpenseService.update(eid, request.form)
            flash("Expense updated!", "success")
            return redirect(url_for("admin.manage_expenses"))
        except Exception as e:
            flash(f"Error updating expense: {e}", "danger")

    return render_template(
        "Admin/edit_expense.html",
        expense=expense,
        vehicles=vehicles,
        form=expense.to_dict() if expense else {},
    )


# =======================================================
#   MAINTENANCE CRUD
# =======================================================
@admin_bp.route("/manage_maintenances")
@admin_only
def manage_maintenances():
    maint = _normalize_list(MaintenanceService.get_all())
    return render_template("Admin/manage_maintenances.html", maintenances=maint)


@admin_bp.route("/add_maintenance", methods=["GET", "POST"])
@admin_only
def add_maintenance():
    vehicles = _normalize_list(VehicleService.get_all())

    if request.method == "POST":
        try:
            MaintenanceService.create(request.form)
            flash("Maintenance added!", "success")
            return redirect(url_for("admin.manage_maintenances"))
        except Exception as e:
            flash(f"Error adding maintenance: {e}", "danger")

    return render_template("Admin/add_maintenance.html", vehicles=vehicles)


@admin_bp.route("/edit_maintenance/<int:mid>", methods=["GET", "POST"])
@admin_only
def edit_maintenance(mid):
    maintenance = MaintenanceService.get_by_id(mid)
    vehicles = _normalize_list(VehicleService.get_all())

    if request.method == "POST":
        try:
            MaintenanceService.update(mid, request.form)
            flash("Maintenance updated!", "success")
            return redirect(url_for("admin.manage_maintenances"))
        except Exception as e:
            flash(f"Error updating maintenance: {e}", "danger")

    return render_template(
        "Admin/edit_maintenance.html",
        maintenance=maintenance,
        vehicles=vehicles,
        form=maintenance.to_dict() if maintenance else {},
    )
