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


Designating a GraphQL Equivalent of an SQLAlchemy Type
-------------------------------------------------------

Due to the early age of the Graphene/GraphQL community, not all SQLAlchemy types
have conversions already specified. If you encounter such a type, consider
posting a PR. If that's not your style, you can always register it yourself:


.. autofunction:: nautilus.api.convert_sqlalchemy_type


.. code-block:: python

    from nautilus.models import BaseModel
    from nautilus.api import convert_sqlalchemy_type
    from sqlalchemy import Column
    from sqlalchemy.dialects.postgresql import UUID
    from graphene.core.types.scalars import String

    class Product(BaseModel):
        id = Column(UUID, primary_key = True)

    @convert_sqlalchemy_type.register(UUID)
    def convert_column_to_string(type, column):
        return String(description = column.doc)
