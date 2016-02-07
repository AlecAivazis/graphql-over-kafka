from .crudHandler import CRUDHandler
from .createHandler import createHandler
from .updateHandler import updateHandler
from .deleteHandler import deleteHandler

def noop_handler(type, payload):
    return
