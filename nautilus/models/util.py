# local imports
from nautilus.conventions.services import connection_service_name, model_service_name
from nautilus.models import BaseModel, fields

def create_connection_model(service):
    """ Create an SQL Alchemy table that connects the provides services """
    # the services connected
    services = service._services

    # the mixins / base for the model
    bases = (BaseModel,)
    # the fields of the derived
    attributes = {model_service_name(service): fields.CharField() for service in services}

    # create an instance of base model with the right attributes
    return type(BaseModel)(connection_service_name(service), bases, attributes)
