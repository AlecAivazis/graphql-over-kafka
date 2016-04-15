# external imports
import unittest
import tornado.testing
import tornado.gen
from graphene import Schema, ObjectType, String, resolve_only_args
from graphql.core.execution.middlewares.utils import resolver_has_tag
from graphql.core.error import format_error
# local imports
import nautilus
from nautilus.api.executor import async_field, is_async_field

@tornado.gen.coroutine
def _coroutine():
    return 'hello'


class TestUtil(tornado.testing.AsyncTestCase):

    def setUp(self):
        # create an ioloop to use
        self.io_loop = self.get_new_ioloop()

        # import the executor
        from nautilus.api.executor import TornadoExecutor
        # create a schema with the executor attached
        self.schema = Schema(name='test_schema', executor=TornadoExecutor())

        # an object type to check
        class TestQuery(ObjectType):
            sync = String()
            async = String()
            fail = String()
            chained = String()

            @resolve_only_args
            def resolve_sync(self):
                return 'hello'

            @async_field
            def resolve_async(success, error):
                success('hello')

            @async_field
            def resolve_fail(success, error):
                error(Exception('hello'))

            @async_field
            @tornado.gen.coroutine
            def resolve_chained(success, error):
                result = yield _coroutine()

                success(result)



        # attach the query to the schema
        self.schema.query = TestQuery


    def test_can_tag_functions_as_async(self):
        @async_field
        def test_func(): 
            "a function to test"

        assert is_async_field(test_func), (
            "Test function could not be tagged as an aync field."
        )



    @tornado.testing.gen_test
    def test_can_execute_sync_query(self):

        # the query to test the schema
        test_query = "query{ sync }"
        # resolve the query in the schema
        resolved_query = yield self.schema.execute(test_query)

        # assert that there are no errors
        assert len(resolved_query.errors) == 0, (
            "Schema contained errors."
        )
        assert resolved_query.data['sync'] == 'hello', (
            "Sync query did not have the correct data value."
        )


    @tornado.testing.gen_test
    def test_can_execute_async_query(self):

        # the query to test the schema
        test_query = "query{ async }"
        # resolve the query in the schema
        resolved_query = yield self.schema.execute(test_query)

        # assert that there are no errors
        assert len(resolved_query.errors) == 0, (
            "Schema contained errors: " + ','.join(resolved_query.errors)
        )
        assert resolved_query.data['async'] == 'hello', (
            "Async query did not have the correct data value."
        )


    @tornado.testing.gen_test
    def test_async_query_can_call_errback(self):

        # the query to test the schema
        test_query = "query{ fail }"
        # resolve the query in the schema
        resolved_query = yield self.schema.execute(test_query)

        # assert that there are no errors
        assert len(resolved_query.errors) == 1, (
            "Schema did not contain errors."
        )
        # make sure the error text matches up
        assert format_error(resolved_query.errors[0])['message'] == 'hello', (
            "Error text does not match up with what I expected."
        )


    @tornado.testing.gen_test
    def test_async_query_can_call_chained(self):

        # the query to test the schema
        test_query = "query{ chained }"
        # resolve the query in the schema
        resolved_query = yield self.schema.execute(test_query)
        
        # assert that there are no errors
        assert len(resolved_query.errors) == 0, (
            "Schema contained errors: " + ','.join(resolved_query.errors)
        )
        assert resolved_query.data['chained'] == 'hello', (
            "Async query did not have the correct data value."
        )



