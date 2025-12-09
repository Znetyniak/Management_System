from flask import Blueprint

# --------------------------------------------------------
# BLUEPRINTS (ПРАВИЛЬНА ВЕРСІЯ — БЕЗ template_folder)
# --------------------------------------------------------

auth_bp = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth'
)

store_bp = Blueprint(
    'store',
    __name__,
    url_prefix='/store'
)

admin_bp = Blueprint(
    'admin',
    __name__,
    url_prefix='/admin'
)

# --------------------------------------------------------
# ІМПОРТ КОНТРОЛЕРІВ
# --------------------------------------------------------

from app.controllers import auth_controller
from app.controllers import store_controller
from app.controllers import admin_controller
