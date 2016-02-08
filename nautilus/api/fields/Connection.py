# external imports
import collections
from graphene import Field, List
from graphql.core.utils.ast_to_dict import ast_to_dict
from graphql.core.language.printer import print_ast
# local imports
from nautilus.network import query_model_service

class Connection(Field):
    """
        A field which encapsultes a connection between two objects. Optionally,
        this field takes a `service` argument which indicates that this connection
        is backed by a remote service. This will cause the field resolution to query
        the remote service for data. If a `service` is not specified, a resolver function
        must be present - either with the conventional name or explicity passed.
    """

    def __init__(self, target, service = None, relay = True, **kwds):

        # save the provided datum
        self.service = service
        self.target = target

        # if a resolve was not specified
        if 'resolver' not in kwds:
            # set the resolver if a service was specified
            kwds['resolver'] = self.resolve_service if service else None

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
        # the potential pieces of data to retrieve about the object depends on
        # the target object type we are going to instantiate.
        # todo: avoid internal _meta pointer since its potentially weak
        targetFields = self.target._meta.fields

        # grab the fields that are not connections
        fields = [field.attname for field in targetFields if not isinstance(field, type(self))]

        # check if any args point to another servce indicating a join filter


        return (self.target(**result) for result in query_model_service(self.service, fields, filters = args))
