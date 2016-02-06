# local imports
from nautilus.network import combineActionHandlers

def CRUDActionHandler(Model):
    """
        This action handler factory reaturns an action handler that
        responds to actions with CRUD types (following nautilus conventions)
        and performs the necessary mutation on the model's database.
    """
    # import the various crud handlers
    from . import editActionHandler, createActionHandler, deleteActionHandler
    # combine them into one handler
    return combineActionHandlers(
        editActionHandler(Model),
        createActionHandler(Model),
        deleteActionHandler(Model),
    )
