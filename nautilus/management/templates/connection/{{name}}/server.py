# third party imports
from nautilus import ConnectionService

# import the services to connect
{% for service in services %}
from ..{{service}} import service as {{service.title()}}Service{% endfor %}

class ServiceConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/sensorProductConnection.db'

service = ConnectionService(
    configObject = ServiceConfig,
    services = [{% for service in services %}
                    {{service.title()}}Service,{% endfor %}
                ],
)
