# local imports
from nautilus.conventions.services import connection_service_name
from nautilus.models import BaseModel, fields

def create_connection_model(models):
    """ Create an SQL Alchemy table that connects the provides services """

    # the mixins / base for the model
    bases = (BaseModel,)
    # the fields of the derived
    attributes = {model.model_name.lower(): fields.CharField() for model in models}

    # create an instance of base model with the right attributes
    return type(BaseModel)(connection_service_name(*models), bases, attributes)
