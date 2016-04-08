# external imports
import nautilus
# local imports
from .schema import schema

class {{name.title()}}(nautilus.APIGateway):
    schema = schema
