# external imports
from graphene import ObjectType
from graphene.core.classtypes.objecttype import ObjectTypeOptions

VALID_ATTRS = ('service',)

class ServiceObjectTypeOptions(ObjectTypeOptions):

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.valid_attrs += VALID_ATTRS
        self.service = None

    def contribute_to_class(self, cls, name):
        super().contribute_to_class(cls, name)
        cls.service = self.service

class ServiceObjectTypeMeta(type(ObjectType)):

    options_class = ServiceObjectTypeOptions

    def construct(cls, *args, **kwds):
        cls.service = cls._meta.service
        return super().construct(*args, **kwds)


class ServiceObjectType(ObjectType, metaclass = ServiceObjectTypeMeta):
    """
        This object type represents data maintained by a remote service.
        `Connection`s to and from other `ServiceObjectType`s are resolved
        through a specified a connection service assuming nautilus naming
        conventions.
    """
