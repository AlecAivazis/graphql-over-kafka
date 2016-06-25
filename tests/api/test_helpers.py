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
        assert field['name'] == nautilus.conventions.api.root_query(), (
            'The generated schema does not have a field named `all_models`'
        )

        # grab the arguments for the field
        arg_names = {arg['name'] for arg in field['args']}

        # make sure the test field is present
        assert 'test_field' in arg_names, (
            "The generated schema cannot be filterd for model fields."
        )


    def test_can_summarize_service(self):
        # the service to summarize
        class MockService(nautilus.Service):
            pass
        # the target summary
        target = {
            'name': 'mockService',
        }

        # summarize the service
        summarized = summarize_service(MockService)
        # make sure the names match up
        assert target['name'] == summarized['name'], (
            "Summarzied service did not have the right name."
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
            'name': 'mockModelService',
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
        summarized = summarize_service(MockModelService)
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


    def test_can_summarize_connection_service(self):
        # a model to test
        class Model1(nautilus.models.BaseModel):
            name = nautilus.models.CharField()
        class ModelService1(nautilus.ModelService):
            model = Model1
        # a model to test
        class Model2(nautilus.models.BaseModel):
            name = nautilus.models.CharField()
        class ModelService2(nautilus.ModelService):
            model = Model2
        # a connection service
        class ConnectionService(nautilus.ConnectionService):
            from_service = ModelService1
            to_service = ModelService2

        # the target summary
        target = {
            'name': 'connectionService',
            'connection': {
                'from': {
                    'service': 'modelService1'
                },
                'to': {
                    'service': 'modelService2'
                }
            }
        }
        # make sure it matches the result
        assert summarize_service(ConnectionService) == target, (
            "Connection service could not be correctly summarized."
        )


    def test_can_summarize_auth_service(self):
        # an auth service to test
        class Auth(nautilus.AuthService): pass

        # the target summary
        target = {
            'name': nautilus.conventions.services.auth_service_name(),
        }
        # make sure it matches the result
        assert summarize_service(Auth) == target, (
            "Auth service could not be summarized"
        )
