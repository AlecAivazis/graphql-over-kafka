from tornado.web import RequestHandler as TornadoRequestHandler

class RequestHandler(TornadoRequestHandler):
    """
        The base class for nautilus http request handlers.

        Example:

            import nautilus
            from nautilus.network.http import RequestHandler

            service = nautilus.Service(...)

            @service.route('/')
            class MyRequestHandler(RequestHandler):
                def get(self):
                    self.finish('hello')
    """

    def post(self):
        self.check_xsrf_cookie()

    def options(self):
        # no body
        self.set_status(204)
        self.finish()
