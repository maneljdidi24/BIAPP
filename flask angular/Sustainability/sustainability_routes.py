from . import sustainability_routes
from .Performance.Element.element_routes import element_routes
from .Performance.Topic.topic_routes import topic_routes
from .Performance.Performance.performance_routes import performance_routes


sustainability_routes.register_blueprint(element_routes, url_prefix='/element')
sustainability_routes.register_blueprint(topic_routes, url_prefix='/topic')
sustainability_routes.register_blueprint(performance_routes, url_prefix='/performance')

