# app/controllers/auth_controller.py

from flask import render_template, request, redirect, url_for, flash, session
from functools import wraps

from app.controllers import auth_bp
from app.models.user import User
from app.extensions import db


# ----------------------------------------------------
# LOGIN REQUIRED DECORATOR
# ----------------------------------------------------
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("You must log in first.", "warning")
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)
    return wrapper


# ----------------------------------------------------
# ROLE REDIRECTION
# ----------------------------------------------------
def redirect_by_role():
    # можна змінити на admin.dashboard якщо хочеш
    return redirect(url_for("store.dashboard"))


# ----------------------------------------------------
# LOGIN
# ----------------------------------------------------
@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    # Якщо вже залогінений → Store
    if "user_id" in session:
        return redirect_by_role()

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        # Пошук користувача
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("User not found.", "danger")
            return redirect(url_for("auth.login"))

        if user.password != password:
            flash("Wrong password.", "danger")
            return redirect(url_for("auth.login"))

        # УСПІШНИЙ ВХІД — зберігаємо всю потрібну інформацію
        session["user_id"] = user.id
        session["role"] = user.role
        session["user_name"] = user.full_name   # ← ВАЖЛИВО, navbar читає саме ЦЕ

        flash(f"Welcome, {user.full_name}!", "success")
        return redirect_by_role()

    return render_template("Auth/login.html")


# ----------------------------------------------------
# SIGNUP
# ----------------------------------------------------
@auth_bp.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        # Перевірка
        if not full_name or not email or not password:
            flash("All fields are required.", "warning")
            return redirect(url_for("auth.signup"))

        if User.query.filter_by(email=email).first():
            flash("This email is already registered.", "danger")
            return redirect(url_for("auth.signup"))

        # Створення нового користувача
        new_user = User(
            full_name=full_name,
            email=email,
            password=password,
            role="user"
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("Auth/signup.html")


# ----------------------------------------------------
# LOGOUT
# ----------------------------------------------------
@auth_bp.route('/logout')
@login_required
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
