# third party imports
from nautilus import ModelService
# third party imports
from sqlalchemy import Column, Text
from nautilus.models import HasID, BaseModel, CRUDNotificationCreator

class {{name.title()}}(CRUDNotificationCreator, BaseModel):
    pass


class ServiceConfig:
    databuse_url = 'sqlite:////tmp/{{name}}.db'


class {{name.title()}}(nautilus.ModelService):
    model = {{name.title()}}
    config = ServiceConfig
