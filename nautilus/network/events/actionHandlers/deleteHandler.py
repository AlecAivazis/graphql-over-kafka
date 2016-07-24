# local imports
from nautilus.conventions.actions import (
    get_crud_action,
    change_action_status,
    success_status,
    error_status
)
from nautilus.models.serializers import ModelSerializer

def delete_handler(Model, name=None, **kwds):
    """
        This factory returns an action handler that deletes a new instance of
        the specified model when a delete action is recieved, assuming the
        action follows nautilus convetions.

        Args:
            Model (nautilus.BaseModel): The model to delete when the action
                received.

        Returns:
            function(type, payload): The action handler for this model
    """
    # necessary imports
    from nautilus.database import db

    async def action_handler(service, action_type, payload, props, notify=True, **kwds):
        # if the payload represents a new instance of `model`
        if action_type == get_crud_action('delete', name or Model):
            try:
                # the props of the message
                message_props = {}
                # if there was a correlation id in the request
                if 'correlation_id' in props:
                    # make sure it ends up in the reply
                    message_props['correlation_id'] = props['correlation_id']
                # the id in the payload representing the record to delete
                record_id = payload['id'] if 'id' in payload else payload['pk']
                # get the model matching the payload
                try:
                    model_query = Model.select().where(Model.primary_key() == record_id)
                except KeyError:
                    raise RuntimeError("Could not find appropriate id to remove service record.")
                # remove the model instance
                model_query.get().delete_instance()
                # if we need to tell someone about what happened
                if notify:
                    # publish the success event
                    await service.event_broker.send(
                        payload='{"status":"ok"}',
                        action_type=change_action_status(action_type, success_status()),
                        **message_props
                    )

            # if something goes wrong
            except Exception as err:
                # if we need to tell someone about what happened
                if notify:
                    # publish the error as an event
                    await service.event_broker.send(
                        payload=str(err),
                        action_type=change_action_status(action_type, error_status()),
                        **message_props
                    )
                # otherwise we aren't supposed to notify
                else:
                    # raise the exception normally
                    raise err


    # return the handler
    return action_handler
