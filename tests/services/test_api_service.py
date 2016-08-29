# external imports
import unittest
from collections.abc import Callable
# local imports
import nautilus

class TestUtil(unittest.TestCase):

    def setUp(self):
        # create a service without an explict name
        class MyService(nautilus.APIGateway):

            @nautilus.auth_criteria('TestService')
            def test_auth(self, model, user):
                pass


        # save the service record to the test suite
        self.service = MyService

    def test_has_conventional_name(self):
        # make sure the name of the service matches convention
        assert self.service.name == nautilus.conventions.services.api_gateway_name(), (
            "APIGateway did not have a name matching the convention."
        )

    def test_has_user_password_as_model(self):
        # make sure the service model is the correct on
        assert self.service().model == nautilus.auth.models.UserPassword, (
            "APIGateway did not have the correct underlying model"
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


    def test_requires_valid_secret_key(self): pass


    def test_raises_error_for_invalid_secret_key(self): pass


    def test_views_have_proper_cors_headers(self): pass


    def test_can_find_service_auth_criteria(self):
        # the auth criteria of the mocked service
        auth_criteria = self.service().auth_criteria

        # and it's the only one
        assert len(auth_criteria) == 1, (
            "There is an incorrect number of entries in the auth criteria map"
        )
        # check that the target service is in the dictionary
        assert 'TestService' in auth_criteria, (
            "Could not find service auth criteria in service dictionary"
        )
        # and that it's callable
        assert isinstance(auth_criteria['TestService'], Callable), (
            "Auth criteria handler was not callable."
        )
