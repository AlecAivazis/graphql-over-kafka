from .query import *

def get_current_event_broker():
    """
        This function returns the event broker associated with the current
        ioloop.

        Note: this is not necessarily tied to the particular service - there 
        could be multiple services listening on the same ioloop.
    """
    # import the tornado module here to prevent namespace clutter
    import tornado
    # for now, assume there is a service attached to the ioloop
    return tornado.ioloop.IOLoop.current().service.event_broker