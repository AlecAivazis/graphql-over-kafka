def crud_handler(Model, name=None, **kwds):
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
    from nautilus.network.events import combine_action_handlers
    from . import update_handler, create_handler, delete_handler, read_handler

    # combine them into one handler
    return combine_action_handlers(
        create_handler(Model, name=name),
        read_handler(Model, name=name),
        update_handler(Model, name=name),
        delete_handler(Model, name=name),
    )
