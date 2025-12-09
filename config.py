import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'fleet_management.db')
SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
