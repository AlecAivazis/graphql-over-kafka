# third party imports
import nautilus
from nautilus.models import BaseModel, CRUDNotificationCreator, fields

class {{name.title()}}(CRUDNotificationCreator, BaseModel):
    pass


class ServiceConfig:
    databuse_url = 'sqlite:////tmp/{{name}}.db'


class {{name.title()}}Service(nautilus.ModelService):
    model = {{name.title()}}
    config = ServiceConfig
