# external imports
from types import new_class
from sqlalchemy.orm import mapper
from sqlalchemy import Table, Column, Integer, Text
# local imports
from nautilus.db import db
from nautilus.conventions.services import connection_service_name
from nautilus.models import BaseModel, CRUDNotificationCreator

def create_connection_model(services):
    """ Create an SQL Alchemy table that connects the provides services """

    # the mixins / base for the model
    bases = (BaseModel,)
    # the fields of the derived
    attributes = {service.name: Column(Text, nullable = False) for service in services}

    # create an instance of base model with the right attributes
    return type(BaseModel)(connection_service_name(*services), bases, attributes)
