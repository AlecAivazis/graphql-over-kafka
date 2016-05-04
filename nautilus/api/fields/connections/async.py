# local imports
from .base import BaseConnection

class AsyncConnection(BaseConnection):
    """
        This Connection is very similar in function to the base class, however
        in order to resolve the various bits of the connection, this connection
        uses the event system to request/recieve information.
    """
    def resolve_service(self, instance, args, info):
        '''
            This function grabs the remote data that acts as the source for this
            connection by querying for the relevant fields from the event pool 
            and waiting for a reply.

            Note: it is safe to assume the target is a service object -
                strings have been coerced.
        '''

        # need to access the request handler dict used by the event handler
        # who defines/maintains that?