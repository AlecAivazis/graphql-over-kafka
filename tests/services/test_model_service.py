# external imports
import unittest
# local imports
import nautilus
import nautilus.models as models
import nautilus.network.amqp.actionHandlers as action_handlers

class TestUtil(unittest.TestCase):

    def setUp(self):

        class TestModel(nautilus.models.BaseModel):
            name = nautilus.models.fields.CharField()

        class TestService(nautilus.ModelService):
            model = TestModel

        # save the class records to the suite
        self.model = TestModel
        self.service = TestService()


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

        # parse the query with the service's schema
        parsed_query = self.service.api_schema.execute(query)

        print(parsed_query.data, parsed_query.errors)
        # make sure there are no errors
        assert parsed_query.errors == [], (
            "Model service schema is invalid."
        )
        schema = self.service.schema
        

    def test_can_provide_addtnl_action_handler(self): pass


    def test_action_handler_handles_crud(self): pass
