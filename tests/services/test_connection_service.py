# external imports
import unittest
# local imports
from nautilus import conventions
from nautilus.conventions import services as service_conventions
from nautilus.conventions.services import model_service_name
import nautilus
from ..util import Mock, async_test

class TestUtil(unittest.TestCase):

    def setUp(self):
        # point the database to a in-memory sqlite database
        nautilus.database.init_db('sqlite:///test.db')

        # create a spy we can check for later
        self.spy = Mock()

        # save the names of the connected services to the suite
        self.service1 = 'TestService1'
        self.service2 = 'TestService2'

        class TestConnectionService(nautilus.ConnectionService):
            from_service = (self.service1,)
            to_service = (self.service2,)

        self.services = [self.service1, self.service2]

        self.service = TestConnectionService()
        self.model = self.service.model

        # create the test table
        self.model.create_table(True)

        # save the attribute we'll use to test against
        self.service1_value = getattr(self.model, model_service_name(self.service1))


    def tearDown(self):
        self.model.drop_table()


    def test_must_provide_services(self):
        # this should throw an exception
        def test_empty_class():
            class TestConnectionService(nautilus.ConnectionService): pass
            # instantiate the incorrect service
            TestConnectionService()

        # expect an error
        self.assertRaises(ValueError, test_empty_class)


    def test_connection_model(self):
        # the fields of the underlying service model
        model_fields = {field.name for field in self.service.model.fields()}

        # the target field names
        target_fields = {
            'id',
            model_service_name(self.service1),
            model_service_name(self.service2)
        }
        # for each model managed by this service
        assert model_fields == target_fields, (
            "Connection model did not have the correct fields"
        )


    def test_has_correct_name(self):
        assert self.service.name == 'testConnectionService', (
            "Connection service did not have the correct name."
        )


    def test_has_valid_schema(self):
        assert hasattr(self.service, 'schema') and self.service.schema, (
            "Model Service did not have a schema."
        )
        # the field to query
        field_name = service_conventions.model_service_name(self.service1)
        # the query to test the schema
        query = """
            query {
                all_models {
                    %s
                }
            }
        """ % field_name

        parsed_query = self.service.schema.execute(query)
        # make sure there are no errors
        assert parsed_query.errors == [], (
            "Model service schema is invalid: " + str(parsed_query.errors)
        )
        assert len(parsed_query.data) > 0, (
            "Model could not be retrieved with schema."
        )

    @async_test
    async def test_action_handler_supports_crud(self):
        await self._verify_action_handler_create()
        await self._verify_action_handler_update()
        await self._verify_action_handler_delete()


    def test_connecting_models_with_same_name(self):
        def create_false_service():

            # create a conenction based on those two services
            class Connection(nautilus.ConnectionService):
                additional_action_handler = self.spy
                from_service = ('TestService1',)
                to_service = ('TestService1',)

            # instantiate the connection
            Connection()

        # make sure the
        self.assertRaises(Exception, create_false_service)


    @async_test
    async def test_listens_for_related_deletes(self):
        # the model connecting the two
        connection_model = self.model()
        setattr(connection_model, model_service_name(self.service1), 1)
        setattr(connection_model, model_service_name(self.service2), 1)
        connection_model.save()

        # make sure the connection model can be found
        assert self.model.get(self.service1_value == 1), (
            "Test record could not be created before deleting."
        )

        # the action data for a related delete
        action_type = conventions.get_crud_action(
            'delete',
            self.service1,
            status='success'
        )
        payload = dict(id=1)

        # instantiate an action handler to test
        handler = self.service.action_handler()
        # fire the action
        await handler.handle_action(
            action_type=action_type,
            payload=payload,
            props={},
            notify=False
        )

        # make sure the model can't be found
        self.assertRaises(Exception, self.model.get, self.service1_value == 1)


    def test_can_summarize(self):

        # the target summary
        target = {
            'name': 'testConnectionService',
            'connection': {
                'from': {
                    'service': 'testService1'
                },
                'to': {
                    'service': 'testService2'
                }
            },
        }
        # summarize the service
        summarized = self.service.summarize()

        # make sure the name matches
        assert summarized['name'] == target['name'], (
            "Summarized connection service doesn't have the right name."
        )
        # make sure the connection info lines up
        assert summarized['connection'] == target['connection'], (
            "Summarized connection info was incorrect."
        )



    ### Utilities / Test tasks

    async def _verify_action_handler_create(self):
        action_type = conventions.get_crud_action('create', self.service.model)
        payload = {
            model_service_name(self.service1): 'foo',
            model_service_name(self.service2): 'bar'
        }
        # create an instance of the action handler
        handler = self.service.action_handler()
        # fire a create action
        await handler.handle_action(
            action_type=action_type,
            payload=payload,
            props={},
            notify=False
        )
        # the query to find a matching model
        matching_model = self.service1_value == 'foo'
        # make sure the created record was found and save the id
        self.model_id = self.model_id = self.model.get(matching_model).id


    async def _verify_action_handler_update(self):
        payload = {'id':self.model_id, model_service_name(self.service1): 'bars'}
        # create an instance of the action handler
        handler = self.service.action_handler()
        # call the service action handler
        await handler.handle_action(
            action_type=conventions.get_crud_action('update', self.model),
            props={},
            payload=payload,
            notify=False
        )
        # check that a model matches
        self.model.get(self.service1_value == 'bars')

    async def _verify_action_handler_delete(self):
        # create an instance of the action handler
        handler = self.service.action_handler()
        # call the service action handler
        await handler.handle_action(
            action_type=conventions.get_crud_action('delete', self.model),
            payload=self.model_id,
            props={},
            notify=False
        )
        # expect an error
        self.assertRaises(Exception, self.model.get, self.model_id)
