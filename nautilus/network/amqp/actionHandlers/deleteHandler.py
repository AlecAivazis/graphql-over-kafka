# local imports
from nautilus.conventions.actions import get_crud_action, change_action_status
from nautilus.models.serializers import ModelSerializer

def delete_handler(Model):
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

    def action_handler(action_type, payload, dispatcher):
        # if the payload represents a new instance of `model`
        if action_type == get_crud_action('delete', Model):
            try:
                # get the model matching the payload
                model_query = Model.select().where(Model.primary_key() == payload)
                # remove the model instance
                model_query.get().delete_instance()

                # publish the scucess event
                dispatcher.publish(
                    ModelSerializer().serialize(model),
                    route=change_action_status(action_type, 'success')
                )

            # if something goes wrong
            except Exception as err:
                # publish the error as an event
                dispatcher.publish(
                    str(err),
                    route=change_action_status(action_type, 'error')
                )


    # return the handler
    return action_handler
