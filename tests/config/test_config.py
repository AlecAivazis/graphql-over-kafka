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

    def test_can_accept_multiple_arguments(self):
        # create a config object with two arguments
        config = Config({'foo': 'bar'}, {'bar': 'baz'})
        # make sure both applied
        assert config['foo'] == 'bar' and config['bar'] == 'baz', (
            "Config could not mix in multiple values."
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


    def test_can_accept_config_object(self):
        # create a config object
        config1 = Config(foo='bar')
        # create a config object out of that object
        config2 = Config(config1)
        # validate the config object
        self.check_configuration(config2,
            "Configuration object could not accept other config objects."
        )


    def test_can_update_with_another_config(self):
        # create a config object
        config1 = Config(foo='bar')
        # create a config object out of that object
        config2 = Config(bar='baz')

        # merge the two configs
        config1.update({'bar':'baz'})
        # make sure one can be applied on the other
        assert config1 == {'foo': 'bar', 'bar': 'baz'}, (
            "Config could not be updated with another."
        )


    def test_can_accept_none(self):
        # create a config with nothing
        config = Config(None)
        # make sure it created an empty config
        assert config == {}, (
            "Config(None) did not create an empty config."
        )
