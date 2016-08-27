# internal imports
from nautilus.conventions.auth import cookie_name # this fixes a circular reference......

def auth_criteria(service):
    """
        This decorator marks the function as the auth specifacation for a
        particular service.

        Args:
            service (str): The service that the function authorizes
    """
    def decorate(handler):
        # add the flag that marks this function for a service
        handler._service_auth = service

        # return the decorated function
        return handler

    return decorate