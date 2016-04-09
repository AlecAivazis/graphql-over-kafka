# external imports
import unittest
from unittest.mock import MagicMock
# local imports
import nautilus
from ..util import assert_called_once_with

class TestUtil(unittest.TestCase):

    def setUp(self):
        # create a service without an explict name
        class MyService(nautilus.APIGateway): pass
        # save the service record to the test suite
        self.service = MyService

    def test_has_conventional_name(self):
        # make sure the name of the service matches convention
        assert self.service.name == nautilus.conventions.services.api_gateway_name(), (
            "APIGateway did not have a name matching the convention."
        )
