# external imports
import unittest
# local imports
import nautilus
import nautilus.models as models
from nautilus.api.helpers import create_model_schema
from nautilus.api.helpers import summarize_service

class TestUtil(unittest.TestCase):

    def test_create_model_schema(self):

        # the model to test
        class TestModel(models.BaseModel):
            test_field = models.fields.CharField()

        # create a graphql schema from the model
        schema = create_model_schema(TestModel)
        # the fields in the schema
        schema_fields = schema.introspect()['__schema']['types'][0]['fields']
        # make sure there is only one field
        self.assertRaises(IndexError, lambda: schema_fields[1])

        # the single field in the schema
        field = schema_fields[0]
        # make sure that field matches the convention
        assert field['name'] == nautilus.conventions.schema.root_query(), (
            'The generated schema does not have a field named `all_models`'
        )

        # grab the arguments for the field
        arg_names = {arg['name'] for arg in field['args']}

        # make sure the test field is present
        assert 'test_field' in arg_names, (
            "The generated schema cannot be filterd for model fields."
        )


    def test_can_summarize_model_service(self):
        # a model to test
        class MockModel(nautilus.models.BaseModel):
            name = nautilus.models.CharField()

        # a model service to test
        class MockModelService(nautilus.ModelService):
            model = MockModel

        # the target summary
        target = {
            'name': 'MockModel',
            'fields': {
                'name': 'String',
            }
        }
        # make sure it matches the result
        assert summarize_service(MockModelService) == target, (
            "Model service could not be correctly summarized."
        )


    def test_can_summarize_connection_service(self):
        # a model to test
        class MockModel1(nautilus.models.BaseModel):
            name = nautilus.models.CharField()
        class MockModelService1(nautilus.ModelService):
            model = MockModel1
        # a model to test
        class MockModel2(nautilus.models.BaseModel):
            name = nautilus.models.CharField()
        class MockModelService2(nautilus.ModelService):
            model = MockModel2
        # a connection service
        class MockConnectionService(nautilus.ConnectionService):
            from_service = MockModelService1
            to_service = MockModelService2

        # the target summary
        target = {
            'name': 'MockConnectionService',
            'connection': {
                'from': {
                    'service': 'MockModelService1'
                },
                'to': {
                    'service': 'MockModelService2'
                }
            }
        }
        # make sure it matches the result
        assert summarize_service(MockConnectionService) == target, (
            "Model service could not be correctly summarized."
        )


    def test_can_summarize_auth_service(self):
        # an auth service to test
        class MockAuth(nautilus.AuthService): pass

        # the target summary
        target = {
            'name': conventions.services.auth_service_name,
        }
        # make sure it matches the result
        assert summarize_service(MockAuth) == target, (
            "Auths service could not be summarized"
        )
