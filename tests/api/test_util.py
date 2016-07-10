# external imports
import unittest
import graphene
# local imports
import nautilus
import nautilus.models as models
from ..util import MockModel, async_test, MockModelService, MockConnectionService
from nautilus.api.util import (
    create_model_schema,
    fields_for_model,
    parse_string,
    graphql_type_from_summary,
    generate_api_schema
)

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


    def test_generate_api_schema(self):
        # create mock summaries
        model_summary = MockModelService()().summarize()
        connection_summary = MockConnectionService()().summarize()
        # create the graphql schema
        schema = generate_api_schema([model_summary], [connection_summary])

        # grab the object type corresponding to our mock
        field = [field for field in schema.query._meta.local_fields if field.default_name == 'testModel']
        # make sure such an object type exists
        assert field, (
            "No object type added to api schema"
        )


    def test_graphql_type_from_summary(self):
        # a mock model service summary
        summary = MockModelService()().summarize()

        # create the graphql type from the summary
        graphql_type = graphql_type_from_summary(summary, [])
        # grab a list of the fields of the generated type
        fields = {field.default_name for field in graphql_type._meta.local_fields}

        # make sure they are what we expect
        assert fields == {'id', 'name', 'date'} , (
            "Generated graphql type does not have the correct fields"
        )


    def test_graphql_type_from_summary_with_connections(self):
        # mock summaries
        summary = MockModelService()().summarize()
        connection_summary = MockConnectionService()().summarize()

        # create the graphql type from the summary
        graphql_type = graphql_type_from_summary(summary, [connection_summary])
        # grab a list of the fields of the generated type
        fields = {field.default_name for field in graphql_type._meta.local_fields}

        # make sure they are what we expect
        assert fields == {'id', 'name', 'date', 'testConnection'} , (
            "Generated graphql type with connection does not have the correct fields"
        )



    def test_walk_query(self): pass


    @async_test
    async def test_parse_string(self):
        # the query to parse
        query = """
            query {
                model {
                    name
                }
            }
        """
        # the resolver for models
        async def model_resolver(object_name, fields, **filters):
            return {field: 'hello' for field in fields}

        async def connection_resolver(connection_name, object):
            return 'hello'

        # parse the string with the query
        result = await parse_string(query, model_resolver, connection_resolver)

        # make sure the value is correct
        assert result == {
            'errors': [],
            'data': {'model': {'name': 'hello'}},
        }, (
            "Could not parse string correctly."
        )


    def test_fields_for_model(self):
        # a mock to test with
        model = MockModel()
        # create the dictionary of fields for the model
        fields = fields_for_model(model)

        assert 'name' in fields and 'date' in fields and 'id' in fields , (
            "Could not create correct fields for model"
        )
        assert isinstance(fields['date'], graphene.String) , (
            "Field summary did not have the correct type"
        )
