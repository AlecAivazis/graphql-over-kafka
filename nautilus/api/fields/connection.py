# external imports
import collections
from graphene import Field, List
from graphql.core.utils.ast_to_dict import ast_to_dict
from graphql.core.language.printer import print_ast
# local imports
from nautilus.network import query_service
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

    def __init__(self, target, relationship = 'many', service = None, relay = True, **kwds):

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
            self.relationship = relationship

            # set the resolver if a service was specified
            kwds['resolver'] = self.resolve_service

        # create a field that is a list of the target
        super().__init__(
            # a connection is normally a list unless we are encapsulating a foreign key
            type = target if perform_resolve and relationship == 'one' else List(target),
            **kwds
        )

    def resolve_service(self, instance, query_args, info):
        '''
            This function grab the remote data that acts as the source for this
            connection.
        '''
        # note: it is safe to assume the target is a service object

        # make a normal dictionary out of the immutable dictionary
        args = query_args.to_data_dict()

        # if we are connecting two service objects, we need to go through a connection table
        if isinstance(instance, ServiceObjectType) or isinstance(instance, str):

            # the target service
            target_service = self.target.service

            # the name of the service that manages the connection
            service_name = connection_service_name(target_service, instance.service)

            # look for connections originating from this object
            join_filter = {}
            join_filter[instance.service] = instance.primary_key
            # grab the list of primary keys from the remote service
            join_ids = [ entry[target_service] \
                            for entry in query_service(service_name, [target_service], join_filter) ]

            # add the private key filter to the filter dicts
            args['pk_in'] = join_ids

        # the potential pieces of data to retrieve about the object depends on
        # the target object type we are going to instantiate.
        # todo: avoid internal _meta pointer since its potentially weak
        targetFields = self.target._meta.fields

        # grab the fields that are not connections
        fields = [field.attname for field in targetFields if not isinstance(field, type(self))]

        # grab the final list of entries
        results = query_service(self.target.service, fields, filters = args)

        # todo: think about doing this at the join step (how to specify both sides of relationship in one spot)
        # if we are on the `one` side of the relationship
        if self.relationship == 'one':
            # if there is more than one result
            if len(results) > 1:
                # yell loudly
                raise Exception("Inconsistent state reached: multiple entries resolving a foreign key reference")
            # otherwise there is only one result
            else:
                # pull the first item out of the list
                return self.target(**results[0])

        # create instances of the target class for every result
        return (self.target(**result) for result in results)
