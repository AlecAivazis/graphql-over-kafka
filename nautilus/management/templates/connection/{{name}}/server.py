# third party imports
import nautilus
from nautilus import ConnectionService
# import the services to connect{% for service in services %}
from ..{{service}} import {{service.title()}}Service{% endfor %}

class ServiceConfig:
    database_url = 'sqlite:////tmp/{{name}}.db'

class {{name.title()}}(nautilus.ConnectionService):
    services = [{% for service in services %}{{service}}_service,{% endfor %}]
    config = ServiceConfig
