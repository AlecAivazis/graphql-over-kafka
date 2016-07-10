# external imports
import json
# local imports
from nautilus.conventions.actions import get_crud_action, success_status, change_action_status

def read_handler(Model, name=None, **kwds):
    """
        This factory returns an action handler that responds to read requests
        by resolving the payload as a graphql query against the internal schema.


        Args:
            Model (nautilus.BaseModel): The model to delete when the action
                received.

        Returns:
            function(type, payload): The action handler for this model
    """
    async def action_handler(service, action_type, payload, props, **kwds):
        # if the payload represents a new instance of `model`
        if action_type == get_crud_action('read', name or Model):
            try:
                # the props of the message
                message_props = {}
                # if there was a correlation id in the request
                if 'correlation_id' in props:
                    # make sure it ends up in the reply
                    message_props['correlation_id'] = props['correlation_id']

                # resolve the query using the service schema
                resolved = service.schema.execute(payload)

                # create the string response
                response = json.dumps({
                    'data': {key:value for key,value in resolved.data.items()},
                    'errors': resolved.errors
                })

                # publish the success event
                await service.event_broker.send(
                    payload=response,
                    action_type=change_action_status(action_type, success_status()),
                    **message_props
                )

            # if something goes wrong
            except Exception as err:
                # publish the error as an event
                await service.event_broker.send(
                    payload=str(err),
                    action_type=change_action_status(action_type, error_status()),
                    **message_props
                )


    # return the handler
    return action_handler
