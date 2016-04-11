# local imports
from nautilus.conventions.actions import get_crud_action

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
    def action_handler(action_type, payload):
        # if the payload represents a new instance of `Model`
        if action_type == get_crud_action('update', Model):

            # grab the nam eof the primary key for the model
            pk_field = Model.primary_key()

            # if the key is in the payload
            if pk_field.name in payload:
                # then we can use it to identify the model we are editing

                # grab the matching model
                model = Model.select().where(pk_field == payload[pk_field.name]).get()

                # remove the key from the payload
                payload.pop(pk_field, None)

                # for every key,value pair
                for key, value in payload.items():
                    # update the model's attribute
                    setattr(model, key, value)

                # save the updates
                model.save()

    # return the handler
    return action_handler
