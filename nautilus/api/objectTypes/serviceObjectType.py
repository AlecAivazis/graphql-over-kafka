# external imports
from graphene import ObjectType, Field, String
from graphene.core.classtypes.objecttype import ObjectTypeOptions
# local imports
from nautilus.api.filter import args_for_model

VALID_ATTRS = ('service',)

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

class ServiceObjectTypeMeta(type(ObjectType)):

    options_class = ServiceObjectTypeOptions

    def construct(cls, *args, **kwds):
        # pass the service to the class record
        cls.service = cls._meta.service
        # return the full class record
        return super().construct(*args, **kwds)

    def __new__(cls, name, bases, attributes, **kwds):

        # if there is a Meta class defined
        if 'Meta' in attributes:
            # if the meta class designates a service
            service = attributes['Meta'].service
            # and that service has a model attributes
            if hasattr(service, 'model'):
                for key,value in args_for_model(service.model).items():
                    if 'pk' not in key and 'in' not in key:
                        attributes[key] = value

        # create the nex class records
        return super().__new__(cls, name, bases, attributes, **kwds)


class ServiceObjectType(ObjectType, metaclass = ServiceObjectTypeMeta):
    """
        This object type represents data maintained by a remote service.
        `Connection`s to and from other `ServiceObjectType`s are resolved
        through a specified a connection service assuming nautilus naming
        conventions.
    """

    primary_key = String()

    @classmethod
    def true_fields(self):
        """
            Returns the list of fields that are not connections.

            Returns:
                (list of fields): The list of fields of this object that are
                    not connections to other objects.
        """

        from nautilus.api.fields import Connection

        # todo: avoid internal _meta pointer since its potentially weak
        targetFields = self._meta.fields

        # grab the fields that are not connections
        return [field for field in targetFields if not isinstance(field, Connection)]
