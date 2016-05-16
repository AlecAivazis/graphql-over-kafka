# external imports
import unittest
import tornado.testing
from graphene import Schema, ObjectType, String
# local imports
import nautilus

class TestUtil(tornado.testing.AsyncTestCase):

    def setUp(self):
        # create a nautilus schema to test
        self.schema = nautilus.api.AsyncSchema()
        # create an ioloop to use
        self.io_loop = self.get_new_ioloop()



    @tornado.testing.gen_test
    def test_does_not_auto_camel_case(self):

        # a query to test with a snake case field
        class TestQuery(ObjectType):
            test_field = String()

            def resolve_test_field(self, args, info):
                return 'hello'

        # assign the query to the schema
        self.schema.query = TestQuery

        # the query to test
        test_query = "query {test_field}"

        # execute the query
        resolved_query = self.schema.execute(test_query)

        assert 'test_field' in resolved_query.data, (
            "Schema did not have snake_case field."
        )

        assert resolved_query.data['test_field'] == 'hello', (
            "Snake_case field did not have the right value"
        )

