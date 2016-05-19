# local imports
import nautilus
from nautilus.network import query_service
from nautilus.conventions.services import connection_service_name
from nautilus.api.objectTypes import ServiceObjectType
from .base import BaseConnection

class Connection(BaseConnection):
    """
        This connection resolves data by making direct (http) requests
        to the appropriate services.
    """

    def resolve_service(self, args, context, info):
        '''
            This function grab the remote data that acts as the source for this
            connection.

            Note: it is safe to assume the target is a service object -
                strings have been coerced.
        '''
        # note: it is safe to assume the target is a service object
        ## resolve the connection if necessary
        target_service_name = self._service_name(self.target)

        # if we are connecting two service objects, we need to go through a connection table
        if isinstance(self, ServiceObjectType):

            # the target service
            instance_service_name = self._service_name(self)

            # the name of the service that manages the connection
            connection_service = connection_service_name(target_service_name,
                                                         instance_service_name)
            # the primary key of the instance we are refering from
            instance_pk = getattr(self, self.service.model.primary_key().name)
            # look for connections originating from this object
            join_filter = {instance_service_name: instance_pk}

            # query the connection service for related data
            related = query_service(
                connection_service,
                [target_service_name],
                filters=join_filter
            )

            # if there were no related fields
            if len(related) == 0:
                return []

            # grab the list of primary keys from the remote service
            join_ids = [entry[target_service_name] for entry in related]
            # add the private key filter to the filter dicts
            args['pk_in'] = join_ids

        ## query the target service

        # only query the backend service for the fields that are not connections
        fields = [field.attname for field in self.target.true_fields()]
        # grab the final list of entries
        results = query_service(target_service_name, fields, filters=args)

        # there are no results
        if len(results) == 0:
            # return an empty result
            return []
        # if there is more than one result for a "one" relation
        elif len(results) > 1 and self.relationship == 'one':
            # yell loudly
            raise ValueError("Inconsistent state reached: multiple entries " + \
                                        "resolving a foreign key reference")

        ## remove instances of the target that the user is not allowed to see
        # if we need to apply some sort of authorization
        if hasattr(self.target, 'auth'):

            try:
                # grab the current user from the request_context
                current_user = context.current_user
            # if there is no user
            except AttributeError:
                raise Exception("User is not accessible.")

            # if the current reqeust is not logged in
            if not current_user:
                # yell loudly
                raise nautilus.auth.AuthorizationError("User is not logged in.")

            # apply the authorization criteria to the result
            results = [
                result for result in results \
                if self.target.auth(
                    self.target(**result),
                    current_user.decode('utf-8'))
            ]

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
            return self.target(**results[0])

        # create instances of the target class for every result
        return [self.target(**result) for result in results]

