# external imports
import unittest
# local imports
import nautilus
from nautilus.models import BaseModel, fields


class TestUtil(unittest.TestCase):
    """
        This test suite looks at the various utilities for manipulating
        models.
    """

    def test_model_string(self):
        # import the utility
        from nautilus.conventions.api import root_query

        class TestModel(BaseModel):
            first_name = fields.CharField()

        # save the model to the test suite
        assert isinstance(root_query(), str), (
            "Could not a root query string for schema"
        )


    def test_throws_when_service_node_name_unknown(self):
        # import the utility
        from nautilus.conventions.api import service_node_name

        # attempt
        try:
            # to create the service node name
            service_node_name(unittest.mock.MagicMock)
        # if there is a value error
        except ValueError:
            # test passed
            pass


    def test_create_model_service_node_name(self):
        # import the utility
        from nautilus.conventions.api import model_service_node_name

        # a model service to test
        class TestModelService(nautilus.ModelService): pass

        # make sure it matches what it should
        assert model_service_node_name(TestModelService) == 'testModelService', (
            "Could not create api node name from model service."
        )


    def test_create_connection_service_node_name(self):
        # import the utility
        from nautilus.conventions.api import model_service_node_name

        # a model service to test
        class TestModelService1(nautilus.ModelService): pass
        # a model service to test
        class TestModelService2(nautilus.ModelService): pass
        # a model service to test
        class TestConnectionService(nautilus.ConnectionService):
            to_service = TestModelService1
            from_service = TestModelService2

        # make sure it matches what it should
        assert model_service_node_name(TestConnectionService) == 'testConnectionService', (
            "Could not create api node name from connection service."
        )
