# local imports
from nautilus.conventions.actions import (
    get_crud_action,
    change_action_status,
    success_status,
    error_status
)
from nautilus.models.serializers import ModelSerializer

def update_handler(Model):
    """
        This factory returns an action handler that updates a new instance of
        the specified model when a update action is recieved, assuming the
        action follows nautilus convetions.

        Args:
            Model (nautilus.BaseModel): The model to update when the action
                received.

        Returns:
            function(type, payload): The action handler for this model
    """
    async def action_handler(service, action_type, payload, notify=True, **kwds):
        # if the payload represents a new instance of `Model`
        if action_type == get_crud_action('update', Model):
            try:
                # grab the nam eof the primary key for the model
                pk_field = Model.primary_key()

                # assume we have an id to identify the model we are editing

                # grab the matching model
                model = Model.select().where(pk_field == payload[pk_field.name]).get()

                # remove the key from the payload
                payload.pop(pk_field, None)

                # for every key,value pair
                for key, value in payload.items():
                    # TODO: add protection for certain fields from being
                    # changed by the api
                    setattr(model, key, value)

                # save the updates
                model.save()

                # if we need to tell someone about what happened
                if notify:
                    # publish the scucess event
                    await service.event_broker.send(
                        body=ModelSerializer().serialize(model),
                        action_type=change_action_status(action_type, success_status())
                    )

            # if something goes wrong
            except Exception as err:
                # if we need to tell someone about what happened
                if notify:
                    # publish the error as an event
                    await service.event_broker.send(
                        body=str(err),
                        action_type=change_action_status(action_type, error_status())
                    )
                # otherwise we aren't supposed to notify
                else:
                    # raise the exception normally
                    raise err

    # return the handler
    return action_handler
