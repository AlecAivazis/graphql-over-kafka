# external imports
import collections
from graphene import Field, List
from graphql.core.utils.ast_to_dict import ast_to_dict
from graphql.core.language.printer import print_ast
# local imports
from nautilus.network import query_model_service
from nautilus.api.objectTypes import ServiceObjectType
from nautilus.conventions.services import connection_service_name

class Connection(Field):
    """
        A field which encapsultes a connection between two objects. Optionally,
        this field takes a `service` argument which indicates that this connection
        is backed by a remote service. This will cause the field resolution to query
        the remote service for data. If a `service` is not specified, a resolver function
        must be present - either with the conventional name or explicity passed.
    """

    def __init__(self, target, service = None, relay = True, **kwds):

        # perform auto resolve when:
            # the connection is backed by a service
            # a resolver wasn't explicity specified
            # we are targetting a service object
        perform_resolve = 'resolver' not in kwds and \
                            not isinstance(target, str) and \
                            issubclass(target, ServiceObjectType)

        # if a resolve was not specified
        if perform_resolve:
            # save references to constructor arguments
            self.target = target
            self.support_relay = relay

            # set the resolver if a service was specified
            kwds['resolver'] = self.resolve_service

        # create a field that is a list of the target
        super().__init__(
            type = List(target),
            **kwds
        )

    def resolve_service(self, instance, args, info):
        '''
            This function grab the remote data that acts as the source for this
            connection.
        '''
        # note: it is safe to assume the target is a service object

        # if we are connecting two service objects
        if isinstance(instance, ServiceObjectType) or isinstance(instance, str):

            # the name of the service that manages the connection
            service_name = connection_service_name(self.target.service, instance.service)
            print("we need to resolve the connection through {!r}".format(service_name))

        # otherwise we are connecting a non service object with a service object

        # the potential pieces of data to retrieve about the object depends on
        # the target object type we are going to instantiate.
        # todo: avoid internal _meta pointer since its potentially weak
        targetFields = self.target._meta.fields

        # grab the fields that are not connections
        fields = [field.attname for field in targetFields if not isinstance(field, type(self))]

        # check if any args point to another servce indicating a join filter
        # for key, value in args.items():
            # the name of the connection between

        return (self.target(**result) for result in query_model_service(self.target.service, fields, filters = args))
