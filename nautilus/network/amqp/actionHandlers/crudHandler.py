def CRUDHandler(Model):
    """
        This action handler factory reaturns an action handler that
        responds to actions with CRUD types (following nautilus conventions)
        and performs the necessary mutation on the model's database.

        Args:
            Model (nautilus.BaseModel): The model to delete when the action
                received.

        Returns:
            function(type, payload): The action handler for this model
    """

    # import the necessary modules
    from nautilus.network import combine_action_handlers
    from . import updateHandler, createHandler, deleteHandler

    # combine them into one handler
    return combine_action_handlers(
        updateHandler(Model),
        createHandler(Model),
        deleteHandler(Model),
    )
