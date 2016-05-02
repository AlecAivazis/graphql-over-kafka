# local imports
from nautilus.conventions.actions import get_crud_action, change_action_status
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
    def action_handler(service, action_type, payload, **kwds):
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

                # publish the scucess event
                service.event_broker.publish(
                    ModelSerializer().serialize(model),
                    route=change_action_status(action_type, 'success')
                )

            # if something goes wrong
            except Exception as err:
                # publish the error as an event
                service.event_broker.publish(
                    str(err),
                    route=change_action_status(action_type, 'error')
                )

    # return the handler
    return action_handler
