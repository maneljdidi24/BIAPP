from flask import Blueprint

access_routes = Blueprint('access_routes', __name__)

from apps import routes  # Importing routes at the end to avoid circular imports
