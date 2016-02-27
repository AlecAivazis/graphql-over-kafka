# local imports
from nautilus.conventions.actions import getCRUDAction

def updateHandler(Model):
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
        if action_type == getCRUDAction('update', Model):

            # go over each primary key
            for key in Model.primary_keys():
                # if the key is in the payload
                if key in payload:
                    # then we can use it to identify the model we are editing

                    # figure out the primary key field
                    primary_key_field = getattr(Model, key)

                    # note: the payload is casted to the same type as the key for equality checks
                    # todo: add pk filter
                    try:
                        model = Model.query.filter(
                            primary_key_field == type(primary_key_field)(payload[key])
                        )
                    # if we couldn't cast the key
                    except TypeError:
                        pass

                    # remove the key from the payload
                    payload.pop(key, None)

                    # for every key,value pair
                    for key, value in payload.items():
                        # update the model's attribute
                        setattr(model, key, value)

                    # save the updates
                    model.save()

                    # don't look for any more identifiers
                    break

    # return the handler
    return action_handler
