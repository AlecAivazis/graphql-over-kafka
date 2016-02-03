"""
    This service maintains sensors registered with Synca.
"""

# third party imports
from nautilus import Service
# local imports
from .actionHandler import actionHandler
from .schema import schema

class ServiceConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/service.db'

service = Service(schema=schema, actionHandler=actionHandler, configObject='server.ServiceConfig')
