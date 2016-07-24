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
    summarize_crud_mutation,
    convert_typestring_to_api_native,
    build_native_type_dictionary,
    serialize_native_type
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

    def test_generate_api_schema_with_mutation(self):
        model_service = MockModelService()()
        # create mock summaries
        model_summary = model_service.summarize()
        mutation_summary = summarize_crud_mutation(model=model_service, method='create')

        # create the graphql schema
        schema = generate_api_schema(
            models=[model_summary],
            mutations=[mutation_summary]
        )

        # the list of mutations in the schema
        schema_mutations = [field.default_name for field in schema.mutation._meta.local_fields]

        # make sure the schema has the correct mutation list
        assert schema_mutations == ['createTestModel'], (
            "Generated schema did not have the correct mutations"
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
        mock_summary = summarize_crud_mutation(model=MockModelService(), method="delete")
        # create the mutation
        mutation = graphql_mutation_from_summary(mock_summary)

        # create a schema to test the mutation
        mock_schema = graphene.Schema()
        # get the corresponding object type
        mutation_object = mock_schema.T(mutation)
        mutation_fields = list(mutation_object.get_fields().keys())

        # there should be one field named status
        assert mutation_fields == ['status'], (
            "Delete mutation did not have correct output"
        )


    def test_graphql_mutation_with_object_io_from_summary(self):
        # create a mock mutation summary with a io that's an object
        mock_summary = summarize_crud_mutation(model=MockModelService(), method="create")
        # create the mutation
        mutation = graphql_mutation_from_summary(mock_summary)

        # create a schema to test the mutation
        mock_schema = graphene.Schema()
        # get the corresponding object type
        mutation_object = mock_schema.T(mutation)
        # make sure there is a resulting 'testModel' in the mutation
        assert 'testModel' in mutation_object.get_fields(), (
            "Generated create mutation  from summary does not have a service record in its output."
        )
        # the fields of the mutation result
        output_fields = set(mutation_object.get_fields()['testModel'].type.get_fields().keys())
        # make sure the object has the right types
        assert output_fields == {'date', 'name', 'id'}, (
            "Mutation output did not have the correct fields."
        )


    def test_walk_query(self):
        """
            This function is implicitly tested when checking parse_string
        """

    @async_test
    async def test_parse_mutation_string(self):
        # the query to parse
        query = """
            mutation {
                myMutation {
                    name
                }
            }
        """
        # the resolver for models
        async def model_resolver(object_name, fields, **filters):
            return {field: 'hello' for field in fields}

        async def connection_resolver(connection_name, object):
            return 'hello'

        async def mutation_resolver(mutation_name, args, fields):
            return {
                field: mutation_name for field in fields
            }

        # parse the string with the query
        result = await parse_string(query, model_resolver, connection_resolver, mutation_resolver)

        # make sure the value is correct
        assert result == {
            'errors': [],
            'mutation': {'myMutation': {'name': 'myMutation'}},
        }, (
            "Could not parse mutation string correctly."
        )


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

        async def mutation_resolver(mutation_name, args, fields):
            return 'hello'

        # parse the string with the query
        result = await parse_string(query, model_resolver, connection_resolver, mutation_resolver)

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


    def test_convert_typestring_to_api_native(self):
        # make sure it converts String to the correct class
        assert convert_typestring_to_api_native('String') == graphene.String, (
            "Could not convert String to native representation."
        )

    def test_serialize_native_type(self):
        # make sure it converts a native string to 'String'
        import nautilus.models.fields as fields
        assert serialize_native_type(fields.CharField()) == 'String', (
            "Could not serialize native type"
        )

    def test_build_native_type_dictionary(self): pass


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

