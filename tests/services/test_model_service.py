# external imports
import unittest
from unittest.mock import MagicMock
# local imports
import nautilus
from nautilus import conventions
from nautilus.conventions import services as service_conventions
import nautilus.models as models
import nautilus.network.amqp.actionHandlers as action_handlers
from ..util import assert_called_once_with

class TestUtil(unittest.TestCase):

    def setUp(self):
        # point the database to a in-memory sqlite database
        nautilus.database.init_db('sqlite:///test.db')

        # create a spy we can check for later
        self.spy = MagicMock()

        class TestModelService(nautilus.models.BaseModel):
            name = nautilus.models.fields.CharField()

        class TestService(nautilus.ModelService):
            model = TestModelService
            additional_action_handler = self.spy

        # save the class records to the suite
        self.model = TestModelService
        self.service = TestService()
        self.service_record = TestService

        # create the test table
        self.model.create_table(True)


    def tearDown(self):
        self.model.drop_table()


    def test_must_provide_a_model(self):
        # this should throw an exception
        def test_empty_class():
            class TestModel(nautilus.ModelService): pass
            # instantiate the incorrect service
            TestModel()

        # expect an error
        self.assertRaises(ValueError, test_empty_class)


    def test_has_conventional_name(self):
        assert self.service_record.name == \
                    service_conventions.model_service_name(self.model), (
            "Model service did not have the correct name."
        )


    def test_has_valid_schema(self):
        assert hasattr(self.service, 'schema') and self.service.schema, (
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

        parsed_query = self.service.schema.execute(query)

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

        # mock the dispatcher
        mock = MagicMock()

        # call the service action handler
        self.service.action_handler(
            action_type,
            payload,
            dispatcher=mock
        )

        # make sure the spy was called correctly
        assert_called_once_with(
            self.spy,
            action_type,
            payload,
            spy_name="Test service spy",
            dispatcher=mock
        )


    def test_action_handler_supports_crud(self):
        self.verify_create_action_handler()
        self.verify_update_action_handler()
        self.verify_delete_action_handler()


    def verify_create_action_handler(self):
        # fire a create action
        self.service.action_handler(
            conventions.get_crud_action('create', self.model),
            dict(name='foo'),
            dispatcher=MagicMock()
        )
        # make sure the created record was found and save the id
        self.model_id = self.model.get(self.model.name == 'foo').id


    def verify_update_action_handler(self):
        # fire an update action
        self.service.action_handler(
            conventions.get_crud_action('update', self.model),
            dict(id=self.model_id, name='barz'),
            dispatcher=MagicMock()
        )
        # check that a model matches
        self.model.get(self.model.name == 'barz')


    def verify_delete_action_handler(self):
        # fire a delete action
        self.service.action_handler(
            conventions.get_crud_action('delete', self.model),
            payload=self.model_id,
            dispatcher=MagicMock()
        )
        # expect an error
        self.assertRaises(Exception, self.model.get, self.model_id)
