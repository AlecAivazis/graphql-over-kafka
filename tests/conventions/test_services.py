# external imports
import unittest
# local imports
import nautilus
from nautilus.conventions import services as conventions


class TestUtil(unittest.TestCase):
    """
        This test suite looks at the various utilities for manipulating
        models.
    """

    def test_model_service_name(self):
        # a model to test with
        class TestModel(nautilus.models.BaseModel):
            name = nautilus.models.fields.CharField()
        # generate a service from the model
        class TestService(nautilus.ModelService):
            model = TestModel
        # make sure we could generate a name for it
        assert isinstance(conventions.model_service_name(TestService), str), (
            "Could not generate name for model service"
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
        class TestServiceModel1(nautilus.models.BaseModel):
            name = nautilus.models.fields.CharField()
        class TestServiceModel2(nautilus.models.BaseModel):
            name = nautilus.models.fields.CharField()

        # a service out of each
        class TestService1(nautilus.ModelService):
            model = TestServiceModel1
        class TestService2(nautilus.ModelService):
            model = TestServiceModel2

        # a connection service for both
        class Connection(nautilus.ConnectionService):
            services = [TestService1, TestService2]

        # make sure we could make a name
        assert isinstance(conventions.connection_service_name(Connection), str), (
            "Could not generate name for connection service"
        )
