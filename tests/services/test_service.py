# external imports
import unittest
from unittest.mock import MagicMock
# local imports
import nautilus
from ..util import assert_called_once_with
from nautilus.api.endpoints import GraphQLRequestHandler

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

    def test_can_accept_name(self):
        class MyService(nautilus.Service):
            name = 'foo'

        assert MyService.name == 'foo', (
            "Service could not recieve custom name."
        )


    def test_can_initialize_with_schema(self):
        # create a mock schema
        schema = MagicMock()
        # make sure the internal schema is what we gave it
        assert self.service(schema=schema).schema == schema, (
            "Service could not be initialized with a specific schema"
        )


    def test_can_accept_config(self):
        # create a config object
        config = nautilus.Config(foo='bar')
        # make sure the config is what we gave it
        assert self.service(config=config).config == config, (
            "Service could not be initialized with a specific config."
        )


    def test_can_merge_config_from_init(self):
        # the config of the base class
        base_config = nautilus.Config(foo='bar')
        # the config to initialize with
        init_config = nautilus.Config(foo='baz', wakka='flokka')

        class MyConfiguredService(nautilus.Service):
            config = base_config

        # the mix of the two config
        mix_config = base_config.copy()
        mix_config.update(init_config)

        assert MyConfiguredService(config=init_config).config == mix_config, (
            "Service could not mix the initialized config onto the base one."
        )

    def test_has_request_handler(self):
        # check the value of the internal attribute
        assert issubclass(self.service()._api_request_handler_class, GraphQLRequestHandler), (
            "APIGateway did not have the right request handler class"
        )
