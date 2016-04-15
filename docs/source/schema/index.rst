Service API
================

For the most part, the generation of a Graphql schema takes care of itself
thanks to the excellent Graphene community. To reduce the overall boilerplate,
Nautilus provides a schema factory that generates a schema to match a model:


.. autofunction:: nautilus.api.create_model_schema


Summarizing an External Service in A Schema
---------------------------------------------

Although a service should never rely on information that it does not maintain,
there are very rare cases (like the api gateway) where it is necessary to show
another service's data in a schema. In this case, nautilus provides a special
base class for the object type that represents remote data.


.. autoclass:: nautilus.api.ServiceObjectType
    :members:


Designating a GraphQL Equivalent of a Nautilus Field
-------------------------------------------------------

If you create (or find) a custom field that is compatible with peewee, the ORM
used by nautilus internally, you might find the need to provide a custom handler
in order for the schema generator to be able to convert it to the correct GraphQL
type. 


.. autofunction:: nautilus.contrib.graphene_peewee.converter

This function follows the [singledispatch] pattern. Registering a new type looks 
something like:

.. code-block:: python

    from awesomepackage import AwesomeField
    from nautilus.contrib.graphene_peewee import converter

    @converter.register(AwesomeField)
    def convert_column_to_string(type, column):
        return String(description = column.doc)
