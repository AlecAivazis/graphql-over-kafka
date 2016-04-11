# external imports
from graphene import String
from graphene.relay import Node
from graphene.core.classtypes.objecttype import ObjectTypeOptions
# local imports
from nautilus.api import fields_for_model
from nautilus.network import query_service

# collect the created service objects in a list
serivce_objects = {}

class ServiceObjectTypeOptions(ObjectTypeOptions):

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.valid_attrs += ('service',)
        self.service = None

    def contribute_to_class(self, cls, name):
        # bubble up the chain
        super().contribute_to_class(cls, name)
        # add the service to the class record
        cls.service = self.service


class ServiceObjectTypeMeta(type(Node)):

    options_class = ServiceObjectTypeOptions

    def construct(self, *args, **kwds):
        # pass the service to the class record
        self.service = self._meta.service
        # return the full class record
        return super().construct(*args, **kwds)


    def __new__(cls, name, bases, attributes, **kwds):

        # if there is a Meta class defined
        if 'Meta' in attributes:
            # if the meta class designates a service
            service = attributes['Meta'].service
            # and that service has a model attributes
            if hasattr(service, 'model'):
                # add the appropriates fields to the class record for the given
                # model
                attributes.update(fields_for_model(service.model))


        # create the nex class records
        return super().__new__(cls, name, bases, attributes, **kwds)


    def __init__(self, name, bases, dict):
        # bubble upwards
        super().__init__(name, bases, dict)
        # add the object to the registry
        serivce_objects[name] = self


class ServiceObjectType(Node, metaclass=ServiceObjectTypeMeta):
    """
        This object type represents data maintained by a remote service.
        `Connection`s to and from other `ServiceObjectType`s are resolved
        through a specified a connection service assuming nautilus naming
        conventions.
    """

    primary_key = String()

    def __getattr__(self, attr):
        """
            This is overwritten to check for connection fields which don't
            make it to the class record.
        """
        try:
            # figure out the connections for this service
            connection = [connection for connection in type(self).connections() \
                                        if connection.attname == attr][0]
            # resolve the connection
            return connection.resolver(self, {}, {})

        # if there was no connection
        except KeyError:
            # then we're looking at an attribute we dont know about
            raise AttributeError


    @classmethod
    def get_node(cls, id, info):
        """
            Returns the node with the corresponding id by querying the
            appropriate service.
        """
        from nautilus.conventions import model_service_name

        # the name of the service to query
        service_name = model_service_name(cls.service)
        # the filter to apply to the query to retrieve the object by id
        object_filter = {
            'primary_key': id,
        }

        # the fields of the service to request
        service_fields = fields_for_model(cls.service.model).keys()

        # query the connection service for related data
        return query_service(
            service_name,
            [service_fields],
            object_filter
        )[0]


    @classmethod
    def true_fields(cls):
        """
            Returns the list of fields that are not connections.

            Returns:
                (list of fields): The list of fields of this object that are
                    not connections to other objects.
        """
        from nautilus.api.fields import Connection
        # todo: avoid internal _meta pointer since its potentially weak
        fields = cls._meta.fields
        # grab the fields that are not connections
        return [field for field in fields if not isinstance(field, Connection)]


    @classmethod
    def connections(cls):
        """
            Returns the list of fields that are connections.

            Returns:
                (list of fields): The list of fields of this object that are
                    connections to other objects.
        """
        from nautilus.api.fields import Connection
        # todo: avoid internal _meta pointer since its potentially weak
        fields = cls._meta.fields
        # grab the fields that are not connections
        return [field for field in fields if isinstance(field, Connection)]
