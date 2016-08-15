# local imports
from nautilus.conventions.actions import query_action_type, change_action_status, success_status
from nautilus.api.util import parse_string

async def query_handler(service, action_type, payload, props, **kwds):
    """
        This action handler interprets the payload as a query to be executed
        by the api gateway service.
    """
    # check that the action type indicates a query
    if action_type == query_action_type():
        print('encountered query event {!r} '.format(payload))
        # perform the query
        result = await parse_string(payload,
            service.object_resolver,
            service.connection_resolver,
            service.mutation_resolver,
            obey_auth=False
        )

        # the props for the reply message
        reply_props = {'correlation_id': props['correlation_id']} if 'correlation_id' in props else {}

        # publish the success event
        await service.event_broker.send(
            payload=result,
            action_type=change_action_status(action_type, success_status()),
            **reply_props
        )
