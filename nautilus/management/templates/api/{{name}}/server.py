# external imports
from nautilus import APIGateway
# local imports
from .schema import schema

class {{name.title()}}(nautilus.APIGateway):
    schema = schema
