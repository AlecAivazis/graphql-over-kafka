# external imports
import unittest
from unittest.mock import MagicMock
# local imports
from nautilus import conventions
from nautilus.conventions import services as service_conventions
import nautilus
from ..util import assert_called_once_with

class TestUtil(unittest.TestCase):

    def setUp(self):
        # point the database to a in-memory sqlite database
        nautilus.database.init_db('sqlite:///test.db')

        # create a spy we can check for later
        self.spy = MagicMock()

        class ModelTest1(nautilus.models.BaseModel):
            name = nautilus.models.fields.CharField()

        class ModelTest2(nautilus.models.BaseModel):
            name = nautilus.models.fields.CharField()

        class TestService1(nautilus.ModelService):
            model = ModelTest1

        class TestService2(nautilus.ModelService):
            model = ModelTest2

        class TestConnectionService(nautilus.ConnectionService):
            additional_action_handler = self.spy
            services = [
                TestService1,
                TestService2
            ]

        # save the class records to the suite
        self.service1 = TestService1
        self.service2 = TestService2
        self.services = [self.service1, self.service2]
        self.base_models = [ModelTest1, ModelTest2]
        self.service = TestConnectionService()
        self.model = self.service.model

        # create the test table
        self.model.create_table(True)
        self.service1.model.create_table(True)
        self.service2.model.create_table(True)

        # save the attribute we'll use to test against
        self.service1_value = getattr(self.model, self.service1.model.model_name.lower())


    def tearDown(self):
        self.model.drop_table()
        self.service1.model.drop_table()
        self.service2.model.drop_table()


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
        model_fields = {field.name for field in self.service.get_models()[0].fields()}
        # the target field names
        target_fields = {
            'id',
            self.service1.model.model_name.lower(),
            self.service2.model.model_name.lower()
        }
        # for each model managed by this service
        assert model_fields == target_fields, (
            "Connection model did not have the correct fields"
        )


    def test_has_conventional_name(self):
        assert self.service.name == \
                    service_conventions.connection_service_name(*self.base_models), (
            "Connection service did not have the correct name."
        )


    def test_has_valid_schema(self):
        assert hasattr(self.service, 'schema') and self.service.schema, (
            "Model Service did not have a schema."
        )
        # the name of the service model
        model_name = self.service1.model.model_name.lower()
        # the field to query
        field_name = model_name[0].lower() + model_name[1:]
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

    #
    def test_can_provide_addtnl_action_handler(self):
        # make sure there is a handler to call
        assert hasattr(self.service, 'action_handler'), (
            "Test Service does not have an action handler"
        )
        # values to test against
        action_type = 'asdf'
        payload = 'asdf'

        mock = MagicMock()

        # call the service action handler
        self.service.action_handler(action_type, payload, dispatcher=mock)

        # make sure the spy was called correctly
        assert_called_once_with(
            self.spy,
            action_type,
            payload,
            dispatcher=mock,
            spy_name="Test service spy"
        )


    def test_action_handler_supports_crud(self):
        self._verify_action_handler_create()
        self._verify_action_handler_update()
        self._verify_action_handler_delete()


    def test_connecting_models_with_same_name(self):
        def create_false_service():
            # create one model
            class TestServiceModel(nautilus.models.BaseModel):
                name = nautilus.models.fields.CharField()

            # and two services based off of the same model (have same model_name)
            class TestService1(nautilus.ModelService):
                model = TestServiceModel
            class TestService2(nautilus.ModelService):
                model = TestServiceModel

            # create a conenction based on those two services
            class Connection(nautilus.ConnectionService):
                additional_action_handler = self.spy
                services = [TestService1, TestService2]

            # instantiate the connection
            Connection()

        # make sure the
        self.assertRaises(Exception, create_false_service)


    def test_listens_for_related_deletes(self):
        # make an instance of model1 to connect
        model1 = self.service1.model(name='foo')
        model1.save()
        # make an instance of model2 to connect
        model2 = self.service2.model(name='bar')
        model2.save()
        # the model connecting the two
        connection_model = self.model()
        setattr(connection_model, self.service1.model.model_name.lower(), model1.id)
        setattr(connection_model, self.service2.model.model_name.lower(), model2.id)
        connection_model.save()

        # make sure the connection model can be found
        assert self.model.get(self.service1_value == model1.id), (
            "Test record could not be created before deleting."
        )

        # the action data for a related delete
        action_type = conventions.get_crud_action(
            'delete',
            self.service1.model,
            status='success'
        )
        payload = dict(id=model1.id)

        # fire the action
        self.service.action_handler(action_type, payload, dispatcher=MagicMock())

        # make sure the model can't be found
        self.assertRaises(Exception, self.model.get, self.service1_value == model1.id)


    ### Utilities / Test tasks

    def _verify_action_handler_create(self):
        action_type = conventions.get_crud_action('create', self.service.model)
        payload = {
            self.service1.model.model_name.lower(): 'foo',
            self.service2.model.model_name.lower(): 'bar'
        }
        # fire a create action
        self.service.action_handler(action_type, payload, dispatcher=MagicMock())
        # the query to find a matching model
        matching_model = self.service1_value == 'foo'
        # make sure the created record was found and save the id
        self.model_id = self.model_id = self.model.get(matching_model).id


    def _verify_action_handler_update(self):
        payload = {'id':self.model_id, self.service1.model.model_name.lower(): 'bars'}
        # fire an update action
        self.service.action_handler(
            conventions.get_crud_action('update', self.model),
            payload,
            dispatcher=MagicMock()
        )
        # check that a model matches
        self.model.get(self.service1_value == 'bars')


    def _verify_action_handler_delete(self):
        # fire a delete action
        self.service.action_handler(
            conventions.get_crud_action('delete', self.model),
            self.model_id,
            dispatcher=MagicMock()
        )
        # expect an error
        self.assertRaises(Exception, self.model.get, self.model_id)
