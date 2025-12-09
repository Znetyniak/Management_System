from app import create_app
from app.extensions import db
from app.models.vehicle import Vehicle
from app.models.driver import Driver

def test_create_tables(tmp_path):
    app = create_app()
    with app.app_context():
        db.create_all()
        assert 'vehicles' in db.engine.table_names()
        assert 'drivers' in db.engine.table_names()
