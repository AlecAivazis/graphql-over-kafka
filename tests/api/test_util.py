# external imports
import unittest
import graphene
import json
# local imports
import nautilus
import nautilus.models as models
from ..util import MockModel, async_test, MockModelService, MockConnectionService
from nautilus.conventions.api import crud_mutation_name
from nautilus.conventions.actions import get_crud_action
from nautilus.api.util import (
    create_model_schema,
    fields_for_model,
    parse_string,
    graphql_type_from_summary,
    graphql_mutation_from_summary,
    generate_api_schema,
    summarize_mutation,
    summarize_mutation_io,
    summarize_crud_mutation
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


    def test_graphql_mutation_from_summary(self):
        # create a mock mutation summary
         mock_summary = summarize_crud_mutation(model=MockModelService(), method="create")
         # create the mutation
         mutation = graphql_mutation_from_summary(mock_summary)

         print(mutation)


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


    def test_can_summarize_mutation(self):
        # summarize a mock mutation
        summarized = summarize_mutation(
            mutation_name='test_mutation',
            event='foo.bar',
            inputs=['foo','bar'],
            outputs=['bar','baz']
        )
        # check that it matches what we expect
        expected = {
            'name': 'test_mutation',
            'event': 'foo.bar',
            'isAsync': False,
            'inputs': ['foo','bar'],
            'outputs': ['bar','baz']
        }
        # make sure the two match
        assert summarized == expected, (
            "Summarized mutation did not match expectation."
        )


    def test_can_summarize_async_mutation(self):
        # summarize a mock mutation
        summarized = summarize_mutation(
            'test_mutation',
            'foo.bar',
            isAsync=True,
            inputs=['foo','bar'],
            outputs=['bar','baz']
        )

        # check that it matches what we expect
        expected = {
            'name': 'test_mutation',
            'event': 'foo.bar',
            'isAsync': True,
            'inputs':['foo','bar'],
            'outputs': ['bar','baz']
        }
        # make sure the two match
        assert summarized == expected, (
            "Summarized async mutation did not match expectation. Found {}, expected {}"\
                .format(summarized, expected)
        )


    def test_mutation_io_summary(self):
        # make sure we can summary a mutation io
        summarized = summarize_mutation_io(name="foo", type="bar")
        # make sure its a string
        assert summarized == {
            "name": "foo",
            "type": "bar",
            "required": False
        }, (
            "Summarized mutation io did not have the correct form."
        )


    def test_mutation_required_io_summary(self):
        # make sure we can summary a mutation io
        summarized = summarize_mutation_io(name="foo", type="bar", required=True)
        # make sure its a string
        assert summarized == {
            "name": "foo",
            "type": "bar",
            "required": True
        }, (
            "Required summarized mutation io did not have the correct form."
        )


    def test_can_summarize_crud_mutation(self):
        # a model service to test with
        mock = MockModelService()
        # make sure we can generate a create mutation
        self._verify_crud_mutation(model=mock, action='create')



    def test_can_summarize_crud_mutation(self):
        # a model service to test with
        mock = MockModelService()
        # make sure we can generate a delete mutation
        self._verify_crud_mutation(model=mock, action='delete')



    def test_can_summarize_crud_mutation(self):
        # a model service to test with
        mock = MockModelService()
        # make sure we can generate a update mutation
        self._verify_crud_mutation(model=mock, action='update')


    ## Utilities

    def _verify_crud_mutation(self, model, action):
        # create the mutation
        summarized = summarize_crud_mutation(model=model, method=action)
        # make sure the name matches the convention
        assert summarized['name'] == crud_mutation_name(model=model, action=action), (
            "Summarized %s mutation did not have the right name" % action
        )
        # make sure the event is what we expect
        assert summarized['event'] == get_crud_action(model=model, method=action), (
            "Summarized %s mutation did not have the right event type" % action
        )

