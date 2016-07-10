from nautilus.conventions.actions import roll_call_type

async def roll_call_handler(service, action_type, payload, props, **kwds):
    """
        This action handler responds to the "roll call" emitted by the api
        gateway when it is brought up with the normal summary produced by
        the service.
    """
    # if the action type corresponds to a roll call
    if action_type == roll_call_type():
        # then announce the service
        await service.announce()
