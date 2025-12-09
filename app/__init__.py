import os
from flask import Flask
from app.extensions import db, migrate

def create_app():
    app = Flask(__name__, instance_relative_config=False)

    # -----------------------------------------------
    #  ФІКС: ВИКОРИСТОВУЄМО САМЕ ТВОЮ РЕАЛЬНУ БАЗУ
    # -----------------------------------------------
    REAL_DB_PATH = "/Users/ihor/Desktop/fleet_management_full_project/fleet_management.db"

    app.config['SECRET_KEY'] = 'dev_key_change_me'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{REAL_DB_PATH}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # INIT EXTENSIONS
    db.init_app(app)
    migrate.init_app(app, db)

    # REGISTER BLUEPRINTS
    from app.controllers import auth_bp, store_bp, admin_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(store_bp)
    app.register_blueprint(admin_bp)

    # ---------------------------------------------------
    # 🔥 REGISTER REST API BLUEPRINT
    # ---------------------------------------------------
    from app.controllers.api_controller import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route('/')
    def index():
        return "<h2>Fleet Management System is running</h2>"

    return app
