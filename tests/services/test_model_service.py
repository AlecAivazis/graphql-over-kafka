# external imports
import unittest
from unittest.mock import MagicMock
# local imports
import nautilus
import nautilus.models as models
import nautilus.network.amqp.actionHandlers as action_handlers
from ..util import assert_called_once_with

class TestUtil(unittest.TestCase):

    def setUp(self):
        # create a spy we can check for later
        self.spy = MagicMock()

        class TestModel(nautilus.models.BaseModel):
            name = nautilus.models.fields.CharField()

        class TestService(nautilus.ModelService):
            model = TestModel
            additonal_action_handler = self.spy

        # save the class records to the suite
        self.model = TestModel
        self.service = TestService()

        # create the test table
        self.model.create_table(True)


    def tearDown(self):
        self.model.drop_table()


    def test_must_provide_a_model(self):
        # this should throw an exception
        def test_empty_class():
            class TestModel(nautilus.ModelService): pass
            # instantiate the incorrect service
            model = TestModel()

        # expect an error
        self.assertRaises(AssertionError, test_empty_class)


    def test_has_valid_schema(self):
        assert hasattr(self.service, 'api_schema') and self.service.api_schema, (
            "Model Service did not have a schema."
        )

        # the query to test the schema
        query = """
            query {
                all_models {
                    name
                }
            }
        """

        parsed_query = self.service.api_schema.execute(query)

        # make sure there are no errors
        assert parsed_query.errors == [], (
            "Model service schema is invalid."
        )
        assert len(parsed_query.data) > 0, (
            "Model could not be retrieved with schema."
        )


    def test_can_provide_addtnl_action_handler(self):
        # make sure there is a handler to call
        assert hasattr(self.service, 'action_handler'), (
            "Test Service does not have an action handler"
        )
        # values to test against
        action_type = 'asdf'
        payload = 'asdf'

        # call the service action handler
        self.service.action_handler(action_type, payload)

        # make sure the spy was called correctly
        assert_called_once_with(
            self.spy,
            action_type,
            payload,
            spy_name="Test service spy"
        )


    def test_action_handler_handles_crud(self): pass
