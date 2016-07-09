# external imports
import unittest
import json
# local imports
import nautilus
from nautilus import conventions
from nautilus.conventions import services as service_conventions
import nautilus.models as models
import nautilus.network.events.actionHandlers as action_handlers
from ..util import async_test, Mock

class TestUtil(unittest.TestCase):

    def setUp(self):
        # point the database to a in-memory sqlite database
        nautilus.database.init_db('sqlite:///test.db')

        # create a spy we can check for later
        self.spy = Mock()

        class TestModelService(nautilus.models.BaseModel):
            name = nautilus.models.fields.CharField()

        class TestService(nautilus.ModelService):
            model = TestModelService

        # save the class records to the suite
        self.model = TestModelService
        self.service = TestService()
        self.action_handler = self.service.action_handler()
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


    def test_can_summarize(self):

        # the target summary
        target = {
            'name': 'testModelService',
            'fields': [
                {
                    'name': 'name',
                    'type': 'String'
                }, {
                    'name': 'id',
                    'type': 'ID',
                }
            ]
        }
        # summarize the service
        summarized = self.service.summarize()

        # make sure the names match up
        assert target['name'] == summarized['name'], (
            "Summarzied service did not have the right name."
        )
        # make sure the field entries have the same length
        assert len(target['fields']) == len(summarized['fields']), (
            "Summarized service did not have the right number of fields."
        )
        # make sure the fields match
        for field in target['fields']:
            # grab the matching fields
            equiv = [sumField for sumField in summarized['fields'] \
                                    if sumField['name'] == field['name']][0]
            # make sure the two fields match
            assert equiv == field, (
                "Associated fields did not match"
            )


    @async_test
    async def test_action_handler_supports_crud(self):
        model_id = await self._verify_create_action_handler()
        await self._verify_update_action_handler(model_id)
        await self._verify_delete_action_handler(model_id)


    async def _verify_create_action_handler(self):
        # fire a create action
        await self.action_handler.handle_action(
            action_type=conventions.get_crud_action('create', self.model),
            payload=dict(name='foo'),
            props={},
            notify=False
        )

        # make sure the created record was found and save the id
        return self.model.get(self.model.name == 'foo').id


    async def _verify_update_action_handler(self, model_id):
        # fire an update action
        await self.action_handler.handle_action(
            action_type=conventions.get_crud_action('update', self.model),
            payload=dict(id=model_id, name='barz'),
            props={},
            notify=False
        )
        # check that a model matches
        self.model.get(self.model.name == 'barz')


    async def _verify_delete_action_handler(self, model_id):
        # fire a delete action
        await self.action_handler.handle_action(
            action_type=conventions.get_crud_action('delete', self.model),
            payload=model_id,
            props={},
            notify=False
        )
        # expect an error
        self.assertRaises(Exception, self.model.get, model_id)
