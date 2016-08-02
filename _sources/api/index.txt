API Gateway
================

In order to reduce coupling between the individual services that make up
your application, the api provided by an APIGateway service builds its
graphql schema by waiting for services annouce their contributions
when starting up and piecing together the complete summary of data
availible from the backend services.


.. autoclass:: nautilus.APIGateway
    :members:



Filtering the API
------------------

The API for ``ModelService`` s (and other services based on them like ``ConnectionService``) have a few different filter arguments depending on the
type of the attribute. The following filters show on both the API gateway as
well as the inidividual service apis:

+-----------+-------------------------+--------------------+-------------------------------------------------+
| Filter    |   Value type            |   Attribute type   |  Returns                                        |
+-----------+-------------------------+--------------------+-------------------------------------------------+
| <attr>    |  same as attribute      |    literal         |  all records with the matching attribute value  |
+-----------+-------------------------+--------------------+-------------------------------------------------+
| <attr>_in | list of attribute type  |    literal         |  all records with a value in the specified list |
+-----------+-------------------------+--------------------+-------------------------------------------------+
| first     | integer                 |    any             |  return the first N records                     |
+-----------+-------------------------+--------------------+-------------------------------------------------+
| last      | integer                 |    any             |  return the last N records                      |
+-----------+-------------------------+--------------------+-------------------------------------------------+
| offset    | integer                 |    any             |  start the count filters at a given offset      |
+-----------+-------------------------+--------------------+-------------------------------------------------+


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
    def convert_field_to_string(field):
        return String(description = field.doc)
