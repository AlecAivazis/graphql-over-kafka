# external imports
from graphene import ObjectType, Field, String
from graphene.core.classtypes.objecttype import ObjectTypeOptions

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


class ServiceObjectType(ObjectType, metaclass = ServiceObjectTypeMeta):
    """
        This object type represents data maintained by a remote service.
        `Connection`s to and from other `ServiceObjectType`s are resolved
        through a specified a connection service assuming nautilus naming
        conventions.
    """

    primary_key = String()

    def resolve_primary_key(self, args, info):
        return '2'
