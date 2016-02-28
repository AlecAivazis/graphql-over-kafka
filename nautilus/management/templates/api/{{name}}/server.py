# external imports
from nautilus import APIGateway
# local imports
from .schema import schema

# create a nautilus service with just the schema
service = APIGateway(schema=schema)
