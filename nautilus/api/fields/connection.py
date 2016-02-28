# external imports
import collections
from graphene import Field, List, String
from graphql.core.utils.ast_to_dict import ast_to_dict
from graphql.core.language.printer import print_ast
# local imports
from nautilus.auth import current_user
from nautilus.network import query_service
from nautilus.api.objectTypes import ServiceObjectType
from nautilus.api.objectTypes.serviceObjectType import serivce_objects
from nautilus.conventions.services import connection_service_name
from nautilus.api import convert_sqlalchemy_type
from nautilus.api.filter import args_for_model


class Connection(Field):
    """
        A field that encapsultes a connection with another GraphQL object.

        Args:

            target (str or ObjectType): The target object type. If target is a
                SerivceObjectType then the remote data lookup is automated using the
                target object's meta service attribute.

            relationship (str: "one" or "many"): The kind of relationship that this
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

        # the field to use as the list
        list_wrapper = List(target)

        # if we're not supposed to perform the resolve
        if not perform_resolve:
            # just instantiate a field with the wrapper
            super().__init__(type = list_wrapper, **kwds)
            # and don't do anything else
            return

        # we are supposed to perform the resolve

        # save references to constructor arguments
        self.target = target
        self.relationship = relationship

        # set the resolver if a service was specified
        kwds['resolver'] = self.resolve_service

        # if the target is a service service model
        if hasattr(self.target, 'service') and hasattr(self.target.service, 'model'):
            # add the model's args to the field
            kwds['args'] = args_for_model(self.target.service.model)

        # if we are supposed to resolve only a single element
        if relationship == 'one':
            # then the field should be a direct reference to the target
            super().__init__(type = target, **kwds)
        # otherwise we are going to be resolving many elements
        else:
            # use the list wrapper as the field type
            super().__init__(type = list_wrapper, **kwds)



    def resolve_service(self, instance, query_args, info):
        '''
            This function grab the remote data that acts as the source for this
            connection.
        '''
        # note: it is safe to assume the target is a service object

        # the target class for the connection
        target = self.target

        # if we were given a string to target
        if isinstance(target, str):
            # if the string points to a service object we recognize
            if target in serivce_objects:
                # grab the service object with the matching name
                target = serivce_objects[target]
            # otherwise the string target does not designate a service object
            else:
                # yell loudly
                raise ValueError("Please provide a string designating a " + \
                                    "ServiceObjectType as the target for " + \
                                    "a connection.")

        # make a normal dictionary out of the immutable one we were given
        args = query_args \
                    if isinstance(query_args, dict) \
                    else query_args.to_data_dict()

        ## resolve the connection if necessary
        target_service_name = target.service.name \
                                    if hasattr(target.service, 'name') \
                                    else target.service

        # if we are connecting two service objects, we need to go through a connection table
        if isinstance(instance, ServiceObjectType) or isinstance(instance, str):
            # the target service
            instance_service_name = instance.service.name \
                                            if hasattr(instance.service, 'name') \
                                            else instance.service

            # the name of the service that manages the connection
            connection_service = connection_service_name(target_service_name,
                                                            instance_service_name)

            # look for connections originating from this object
            join_filter = {}
            join_filter[instance_service_name] = instance.primary_key

            # query the connection service for related data
            related = query_service(
                connection_service,
                [target_service_name],
                join_filter
            )

            # if there were no related fields
            if len(related) == 0:
                return None

            # grab the list of primary keys from the remote service
            join_ids = [ entry[target_service_name] for entry in related ]

            # add the private key filter to the filter dicts
            args['pk_in'] = join_ids


        ## query the target service

        # only query the backend service for the fields that are not connections
        fields = [field.attname for field in target.true_fields()]

        # grab the final list of entries
        results = query_service(target_service_name, fields, filters = args)

        # there are no results
        if len(results) == 0:
            return []
        # if there is more than one result for a "one" relation
        elif len(results) > 1 and self.relationship == 'one':
            # yell loudly
            raise Exception("Inconsistent state reached: multiple entries " + \
                                        "resolving a foreign key reference")


        ## remove instances of the target that the user is not allowed to see

        # if we need to apply some sort of authorization
        if hasattr(target, 'auth'):
            # apply the authorization criteria to the result
            results = [result for result in results \
                                if target.auth(target(**result), current_user)]


        ## deal with target relationship types

        # if the filter got rid of all of the results
        if len(results) == 0:
            # the user isn't allowed to see the related data so return nothing
            return None

        # todo: think about doing this at the join step
        # (how to specify both sides of relationship in one spot)
        # if we are on the `one` side of the relationship
        elif self.relationship == 'one':
            # pull the first item out of the list
            return target(**results[0])

        # create instances of the target class for every result
        return (target(**result) for result in results)
