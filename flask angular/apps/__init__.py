from flask import Blueprint

main_routes = Blueprint('main_routes', __name__)

from apps import routes  # Importing routes at the end to avoid circular imports
