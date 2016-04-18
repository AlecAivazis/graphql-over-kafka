# third party imports
import nautilus
from nautilus.models import BaseModel, fields

class {{name.title()}}(BaseModel):
    pass

class ServiceConfig:
    database_url = 'sqlite:///{{name}}.db'

class {{name.title()}}Service(nautilus.ModelService):
    model = {{name.title()}}
    config = ServiceConfig
