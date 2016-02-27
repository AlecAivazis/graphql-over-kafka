# third party imports
from nautilus import ModelService
# third party imports
from sqlalchemy import Column, Text
from nautilus.models import HasID, BaseModel, CRUDNotificationCreator

class {{name.title()}}(CRUDNotificationCreator, HasID, BaseModel):
    pass


class ServiceConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/data.db'


service = ModelService(
    configObject = ServiceConfig,
    model = {{name.title()}},
)
