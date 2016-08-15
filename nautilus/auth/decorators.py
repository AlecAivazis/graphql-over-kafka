# external imports
from aiohttp_session import get_session
from functools import wraps
# internal imports
from nautilus.conventions.auth import cookie_name

def login_required(handler):

    @wraps(handler)
    async def require_auth(request, *args, **kwds):
        # a redirect response
        from nautilus.network.http.responses import HttpFound

        # grab the current session
        session = await get_session(request)
        # if there is an authorized user associated with the session
        if cookie_name() in session:
            # call the wraper
            return handler(request, *args, **kwds)
        # otherwise the user is not logged in
        else:
            # the url to redirect the user to and loging
            login_url = "http://{}/login".format(
                service_location_by_name(auth_service_name())
            )
            # return a redirect response
            return HttpFound(location=login_url)


    return require_auth


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