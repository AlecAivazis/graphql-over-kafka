# external imports
import unittest
from graphene import Schema, ObjectType, String, resolve_only_args
# local imports
import nautilus

class TestUtil(unittest.TestCase):

    def setUp(self):
        # create a nautilus schema to test
        self.schema = nautilus.api.AsyncSchema()


    def test_has_tornado_executor(self):
        # the class of the intended executor
        from nautilus.api.executor import TornadoExecutor
        # make sure the executor is a subclass of the async one
        assert isinstance(self.schema.executor, TornadoExecutor), (
            "Schema did not have the proper type for its executor."
        )