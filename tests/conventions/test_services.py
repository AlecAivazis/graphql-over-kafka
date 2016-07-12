# external imports
import unittest
# local imports
import nautilus
from nautilus.conventions import services as conventions
from ..util import MockModel


class TestUtil(unittest.TestCase):
    """
        This test suite looks at the various utilities for manipulating
        models.
    """

    def test_model_service_name(self):
        # a model to test with
        class TestModel(nautilus.models.BaseModel):
            name = nautilus.models.fields.CharField()
        TestModel = MockModel()
        # generate a service from the model
        class TestService(nautilus.ModelService):
            model = TestModel
        # make sure we could generate a name for it
        assert isinstance(conventions.model_service_name(TestService), str), (
            "Could not generate name for model service"
        )

    def test_model_service_name_accepts_numbers(self):
        # a model to test with
        class TestModel(nautilus.models.BaseModel):
            name = nautilus.models.fields.CharField()
        # generate a service from the model
        class TestService1(nautilus.ModelService):
            model = TestModel

        # figure out the conventional name for the service
        service_name = conventions.model_service_name(TestService1)

        # make sure we could generate a name for it
        assert (
            isinstance(service_name, str) and
            '1' in service_name
        ), (
            "Could not generate name for model service when it has a number."
        )


    def test_auth_service_name(self):
        # make sure we can generate a name for the auth service
        assert isinstance(conventions.auth_service_name(), str), (
            "Could not generate name for auth service."
        )


    def test_api_gateway_name(self):
        # make sure we can generate a name for the auth service
        assert isinstance(conventions.api_gateway_name(), str), (
            "Could not generate name for auth service."
        )


    def test_connection_service_name(self):
        # two models to test

        # a connection service for both
        class Connection(nautilus.ConnectionService):
            to_service = ('TestService1',)
            from_service = ('TestService2',)
        # make sure we could make a name
        assert isinstance(conventions.connection_service_name(Connection()), str), (
            "Could not generate name for connection service"
        )