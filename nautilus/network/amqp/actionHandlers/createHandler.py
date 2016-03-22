# local imports
from nautilus.conventions.actions import get_crud_action

def createHandler(Model):
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
    def action_handler(action_type, payload):
        # if the payload represents a new instance of `Model`
        if action_type == get_crud_action('create', Model):
            # for each required field
            for requirement in Model.requiredFields():
                # ensure the value is in the payload
                if not requirement in payload:
                    print("Required field not found in payload: {}".format(requirement))
                    # todo: check all required fields rather than failing on the first
                    return

            # create a new model
            new_model = Model(**payload)

            # save the new model instance
            new_model.save()

    # return the handler
    return action_handler
