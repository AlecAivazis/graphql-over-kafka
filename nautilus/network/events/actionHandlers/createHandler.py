# external imports
import json
# local imports
from nautilus.conventions.actions import (
    get_crud_action,
    change_action_status,
    success_status,
    error_status
)
from nautilus.models.serializers import ModelSerializer

def create_handler(Model, name=None, **kwds):
    """
        This factory returns an action handler that creates a new instance of
        the specified model when a create action is recieved, assuming the
        action follows nautilus convetions.

        Args:
            Model (nautilus.BaseModel): The model to create when the action
                received.

        Returns:
            function(action_type, payload): The action handler for this model
    """
    async def action_handler(service, action_type, payload, props, notify=True, **kwds):
        # if the payload represents a new instance of `Model`
        if action_type == get_crud_action('create', name or Model):
            # print('handling create for ' + name or Model)
            try:
                # the props of the message
                message_props = {}
                # if there was a correlation id in the request
                if 'correlation_id' in props:
                    # make sure it ends up in the reply
                    message_props['correlation_id'] = props['correlation_id']

                # for each required field
                for requirement in Model.required_fields():

                    # save the name of the field
                    field_name = requirement.name
                    # ensure the value is in the payload
                    # TODO: check all required fields rather than failing on the first
                    if not field_name in payload and field_name != 'id':
                        # yell loudly
                        raise ValueError(
                            "Required field not found in payload: %s" %field_name
                        )
                # print("attemptingt to create %s" % Model)
                # create a new model
                new_model = Model(**payload)

                # save the new model instance
                new_model.save()

                # if we need to tell someone about what happened
                if notify:
                    # publish the scucess event
                    await service.event_broker.send(
                        payload=ModelSerializer().serialize(new_model),
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
