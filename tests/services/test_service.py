# external imports
import unittest
from unittest.mock import MagicMock
# local imports
import nautilus
from ..util import assert_called_once_with

class TestUtil(unittest.TestCase):

    def setUp(self):
        # create a service without an explict name
        class MyService(nautilus.Service): pass
        # save the service record to the test suite
        self.service = MyService

    def test_has_default_name(self):
        # make sure the name matches
        assert self.service.name == 'MyService', (
            "Service did not have the correct name."
        )

    def test_can_accept_action_handler(self):

        def foo(): pass

        assert self.service(action_handler=foo).action_handler == foo, (
            "Service could not be initialized with a specific action_handler"
        )

    def test_can_initialize_with_schema(self):
        # create a mock schema
        schema = MagicMock()
        # make sure the internal schema is what we gave it
        assert self.service(schema=schema).schema == schema, (
            "Service could not be initialized with a specific schema"
        )
