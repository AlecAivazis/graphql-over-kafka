# external imports
import unittest
from graphene import Schema, ObjectType, String, resolve_only_args
# local imports
import nautilus

class TestUtil(unittest.TestCase):

    def setUp(self):

        # import the executor
        from nautilus.api.executor import TornadoExecutor
        # create a schema with the executor attached
        self.schema = Schema(name='test_schema', executor=TornadoExecutor())

        # an object type to check
        class TestQuery(ObjectType):
            sync = String()
            async = String()

            @resolve_only_args
            def resolve_sync(self):
                return 'hello'


            @resolve_only_args
            def resolve_async(self):
                return 'hello'

        # attach the query to the schema
        self.schema.query = TestQuery


    def test_can_execute_sync_query(self):

        # the query to test the schema
        test_query = "query{ sync }"
        # resolve the query in the schema
        resolved_query = self.schema.execute(test_query)

        # assert that there are no errors
        assert len(resolved_query.errors) == 0, (
            "Schema contained errors."
        )

        assert resolved_query.data['sync'] == 'hello', (
            "Resolved query did not have the correct data value."
        )


    def test_can_execute_async_query(self):

        # the query to test the schema
        test_query = "query{ async }"
        # resolve the query in the schema
        resolved_query = self.schema.execute(test_query)

        # assert that there are no errors
        assert len(resolved_query.errors) == 0, (
            "Schema contained errors."
        )

        assert resolved_query.data['async'] == 'hello', (
            "Resolved query did not have the correct data value."
        )