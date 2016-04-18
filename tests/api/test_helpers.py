# external imports
import unittest
# local imports
import nautilus
import nautilus.models as models

class TestUtil(unittest.TestCase):

    def test_create_model_schema(self):

        # the model to test
        class TestModel(models.BaseModel):
            test_field = models.fields.CharField()

        # create a graphql schema from the model
        schema = nautilus.api.helpers.create_model_schema(TestModel)
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

