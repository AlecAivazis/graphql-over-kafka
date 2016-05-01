Action Handlers
================

Action handlers describe how your service mutates its internal state in
response to the arrival of an action from the queue. They are defined as
a function of two arguments: ``action_type`` and ``payload``. ``Action_type`` is a string that
classifies the event and ``payload`` is a dictionary representing the
data associated with the event. For example,


.. code-block:: python

    def action_handler(action_type, payload, dispatcher):
        # if the payload represents a new recipe to add to the list
        if action_type == 'create_recipe':
            # create a new instance of the recipe model
            recipe = Recipe(**payload)
            # save the new model
            recipe.save()
        # otherwise if the payload is the id of a recipe to be deleted
        elif action_type == 'delete_recipe':
            # find the matching recipe
            recipe = Recipe.query.first(Recipe.id == payload)
            # remove the recipe from the database
            recipe.remove()


Action Handlers are defined within the service:

.. code-block:: python


    class MyService(Service):

        def action_handler(self, action_type, payload, dispatcher):
            # ...


Reusing and Combining Action Handlers
---------------------------------------

As your services get more complex, you'll want to split your action handler into
separate functions which each get called. Nautilus provides a function called
``combine_action_handlers`` which serves just this case:

.. autofunction:: nautilus.network.amqp.combine_action_handlers

.. code-block:: python

    from nautilus.network import combine_action_handlers

    def action_handler1(action_type, payload, dispatcher):
        print("first handler fired!")

    def action_handler2(action_type, payload, dispatcher):
        print("second handler fired!")

    combined_handler = combine_action_handlers(
        action_handler1,
        action_handler2
    )

In order to do this within your service, you'll need to wrap it in a property:

.. code-block:: python

    from nautilus import Service
    from nautilus.network import combine_action_handlers

    class MyService(Service):

        @property
        def action_handler(self):
            # assuming action_handlers 1 and 2 were defined as above
            return combine_action_handlers(
                action_handler1,
                action_handler2
            )



Provided Action Handlers
-------------------------

Nautilus provides some action handlers to mix with your own services when creating
custom solutions.

Factories
^^^^^^^^^^^^^^^^^^^^^^^^^^

The following are functions that take a paramter and return an an action creator.

.. autofunction:: nautilus.network.amqp.crud_handler
.. autofunction:: nautilus.network.amqp.create_handler
.. autofunction:: nautilus.network.amqp.update_handler
.. autofunction:: nautilus.network.amqp.delete_handler
