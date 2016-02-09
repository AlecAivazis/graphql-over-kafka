def CRUDHandler(Model):
    """
        This action handler factory reaturns an action handler that
        responds to actions with CRUD types (following nautilus conventions)
        and performs the necessary mutation on the model's database.

        Args:
            Model (nautilus.BaseModel): The model to delete when the action
                received.

        Returns:
            function: The action handler for this model
    """

    # import the necessary modules
    from nautilus.network import combineActionHandlers
    from . import updateHandler, createHandler, deleteHandler

    # combine them into one handler
    return combineActionHandlers(
        updateHandler(Model),
        createHandler(Model),
        deleteHandler(Model),
    )