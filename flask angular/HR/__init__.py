from flask import Blueprint

hr_routes = Blueprint('hr_routes', __name__)

from apps import routes  # Importing routes at the end to avoid circular imports
