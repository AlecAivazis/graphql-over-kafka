# local imports
from nautilus.conventions.actions import get_crud_action

def deleteHandler(Model):
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
    from nautilus.db import db

    def action_handler(action_type, payload):
        # if the payload represents a new instance of `model`
        if action_type == get_crud_action('delete', Model):

            # for now only handle a single selector specified by a string
            if not isinstance(payload, str):
                return

            # go over each primary key
            for key in Model.primary_keys():
                # find the model with the matching primary key
                # the primary key field
                primaryKey = getattr(Model, key)
                try:
                    # note: the payload is casted to the same type as the key for equality checks
                    model = Model.query.filter(primaryKey == type(primaryKey)(payload))
                except TypeError:
                    # we couldn't cast the key so its not the right one. don't do anything
                    pass

                # remove the model from the databaes
                # todo: move this inside base model? Can a model remove itself?
                db.session.delete(model)
                db.session.commit()


    # return the handler
    return action_handler
