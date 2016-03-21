# external imports
from graphene import ObjectType, Field, String
from graphene.relay import Node
from graphene.core.classtypes.objecttype import ObjectTypeOptions
# local imports
from nautilus.api.filter import args_for_model
from nautilus.network import query_service

VALID_ATTRS = ('service',)

# collect the created service objects in a list
serivce_objects = {}

class ServiceObjectTypeOptions(ObjectTypeOptions):

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.valid_attrs += VALID_ATTRS
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
                # for each argument corresponding to a service field
                # TODO: this can probably be done with a better method than
                # args_for_model
                for key, value in args_for_model(service.model).items():
                    # ignore dynamically created fields
                    # TODO: make this cleaner
                    if 'pk' not in key and 'in' not in key and 'id' not in key:
                        # add an attribute to the cls that matches the argument
                        attributes[key] = value

        # create the nex class records
        return super().__new__(cls, name, bases, attributes, **kwds)


    def __init__(self, name, bases, dict):
        # bubble upwards
        super().__init__(name, bases, dict)
        # add the object to the registry
        serivce_objects[name] = self


class ServiceObjectType(Node, metaclass = ServiceObjectTypeMeta):
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
        # figure out the connections for this service
        connection = [connection for connection in type(self).connections() \
                                    if connection.attname == attr]
        # if the attribute that was asked for was a connection
        if connection:
            # return the resolved value
            return connection[0].resolver(self, {}, {})
        else:
            # Default behaviour
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
        service_fields = [arg for arg in args_for_model(cls.service.model).items() \
                            if 'pk' not in arg and 'in' not in arg \
                            and 'id' not in arg]

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

