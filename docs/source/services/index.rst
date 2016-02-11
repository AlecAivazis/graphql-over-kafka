Services
========

Services are the building block of nautilus clouds. Very simply, a
nautilus service is a standalone process that responds to actions sent
over the global event queue, maintains and mutates some internal state
according to the action, and provides a summary of that internal state via
a GraphQL API.

Nautilus provides extendible implementations of common services as well as a base
Service class which all act as good starting points for your own services:


.. autoclass:: nautilus.ModelService
    :members:


.. autoclass:: nautilus.ConnectionService
    :members:


.. autoclass:: nautilus.APIGateway
    :members:


.. autoclass:: nautilus.Service
    :members:
