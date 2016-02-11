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
        A field that encapsultes a connection with another GraphQL object.

        Args:

            target (string or ObjectType): The target object type. If target is a
                SerivceObjectType then the remote data lookup is automated using the
                target object's meta service attribute.

            relationship (string: "one" or "many"): The kind of relationship that this
                connection encapsultes. If set to "many" the connection will result in
                a list whereas if it is set to "one" the connection will result in the
                object type itself.


        Example:

            For an example, see the getting started guide.

    """

    def __init__(self, target, relationship = 'many', **kwds):

        # perform auto resolve when:
            # the connection is backed by a service
            # a resolver wasn't explicity specified
            # we are targetting a service object
        perform_resolve = 'resolver' not in kwds and \
                            ( isinstance(target, str) or \
                            issubclass(target, ServiceObjectType) )

        # if a resolve was not specified
        if perform_resolve:
            # save references to constructor arguments
            self.target = target
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
        target = self.target

        # if we are targetting a string
        if isinstance(self.target, str):
            # todo: find a non-weak version of _type_names
            # grab the equivalent class from the schema
            target = info.schema.graphene_schema._types_names[self.target]

        # make a normal dictionary out of the immutable dictionary
        args = query_args.to_data_dict()

        # if we are connecting two service objects, we need to go through a connection table
        if isinstance(instance, ServiceObjectType) or isinstance(instance, str):

            # the target service
            target_service = target.service

            # the name of the service that manages the connection
            service_name = connection_service_name(target_service, instance.service)

            # look for connections originating from this object
            join_filter = {}
            join_filter[instance.service] = instance.primary_key
            # query the connection service for related data
            related = query_service(service_name, [target_service], join_filter)

            # if there were no related fields
            if len(related) == 0:
                return None

            # grab the list of primary keys from the remote service
            join_ids = [ entry[target_service] for entry in related ]

            # add the private key filter to the filter dicts
            args['pk_in'] = join_ids

        # the potential pieces of data to retrieve about the object depends on
        # the target object type we are going to instantiate.
        # todo: avoid internal _meta pointer since its potentially weak
        targetFields = target._meta.fields

        # grab the fields that are not connections
        fields = [field.attname for field in targetFields if not isinstance(field, type(self))]

        # grab the final list of entries
        results = query_service(target.service, fields, filters = args)

        # there are no results
        if len(results) == 0:
            return None

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
                return target(**results[0])

        # create instances of the target class for every result
        return (target(**result) for result in results)
