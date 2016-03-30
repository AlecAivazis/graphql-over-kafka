# external imports
import unittest
# local imports
from nautilus.config import Config

class TestUtil(unittest.TestCase):

    def check_configuration(self, config, message="Wrong configuration."):
        # make sure the configuration object looks like we expect
        assert config == {'foo': 'bar'} , message


    def test_can_read_keys_as_attribute(self):
        # create a config object to test
        config = Config(foo='bar')
        # validate the config object
        assert config.foo == 'bar', (
            "Attribute could not be read"
        )


    def test_can_set_keys_as_attrbutes(self):
        # create a config object to test
        config = Config(foo='bar')
        # update the attrbute
        config.foo = 'quz'
        # validate the config object
        assert config['foo'] == 'quz', (
            "Attributes could not be updated."
        )


    def test_can_accept_kwds(self):
        # create a config object to test
        config = Config(foo='bar')
        # validate the config object
        self.check_configuration(config,
            "Configuration object could not accept keywords."
        )


    def test_can_accept_dict(self):
        # the configuration dictionary
        config_dict = dict(foo='bar')
        # create a config object out of the dictionary
        config = Config(config_dict)
        # validate the config object
        self.check_configuration(config,
            "Configuration object could not accept dictionaries."
        )


    def test_can_accept_type(self):
        # the configuration type
        class ConfigType:
            foo = 'bar'
            # add a function to the test too
            def func(self): pass

        # create the config object from the type
        config = Config(ConfigType)
        # validate the config object
        self.check_configuration(config,
            "Configuration object could not accept types."
        )
