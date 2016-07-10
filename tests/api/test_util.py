# external imports
import unittest
# local imports
import nautilus
import nautilus.models as models
from nautilus.api.util import create_model_schema
from ..util import MockModel

class TestUtil(unittest.TestCase):

    def test_create_model_schema(self):

        # create a graphql schema from the model
        schema = create_model_schema(MockModel())

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
        assert 'name' in arg_names, (
            "The generated schema cannot be filterd for model fields."
        )


    def test_generate_api_schema(self): pass


    def test_graphql_type_from_summary(self): pass


    def test_walk_query(self): pass


    def test_parse_string(self): pass


    def test_fields_for_model(self): pass
