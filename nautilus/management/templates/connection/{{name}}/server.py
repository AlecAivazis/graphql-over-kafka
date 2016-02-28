# third party imports
from nautilus import ConnectionService
# import the services to connect{% for service in services %}
from ..{{service}} import service as {{service}}_service{% endfor %}

class ServiceConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/{{name}}.db'

service = ConnectionService(
    configObject = ServiceConfig,
    services = [{% for service in services %}
                    {{service}}_service,{% endfor %}
                ]
)
