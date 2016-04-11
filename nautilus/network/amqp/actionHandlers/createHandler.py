# local imports
from nautilus.conventions.actions import get_crud_action, change_action_status
from nautilus.models.serializers import ModelSerializer

def create_handler(Model):
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
    def action_handler(action_type, payload, dispatcher):

        # if the payload represents a new instance of `Model`
        if action_type == get_crud_action('create', Model):

            try:
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

                # create a new model
                new_model = Model(**payload)

                # save the new model instance
                new_model.save()

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
