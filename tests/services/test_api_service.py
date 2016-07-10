# external imports
import unittest
# local imports
import nautilus

class TestUtil(unittest.TestCase):

    def setUp(self):
        # create a service without an explict name
        class MyService(nautilus.APIGateway): pass
        # save the service record to the test suite
        self.service = MyService

    def test_has_conventional_name(self):
        # make sure the name of the service matches convention
        assert self.service.name == nautilus.conventions.services.api_gateway_name(), (
            "APIGateway did not have a name matching the convention."
        )

    def test_has_custom_request_handler(self):
        # import the module to test
        from nautilus.api.endpoints.requestHandlers.apiQuery import APIQueryHandler
        # check the value of the internal attribute
        assert self.service().api_request_handler_class == APIQueryHandler, (
            "APIGateway did not have the right query handler class"
        )

    def test_has_custom_action_handler(self):
        import nautilus.network.events.consumers.api as api_handler
        # check the value of the internal attribute
        assert self.service().action_handler == api_handler.APIActionHandler, (
            "APIGateway did not have the right action handler class"
        )


    def test_views_have_proper_cors_headers(self): pass


