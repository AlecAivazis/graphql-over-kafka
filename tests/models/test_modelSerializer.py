# external imports
import unittest
from unittest.mock import MagicMock

class TestUtil(unittest.TestCase):

    def test_can_serialize_custom_objects(self):
        # import the model serializer
        from nautilus.models.serializers import ModelSerializer
        # import the normal json module
        import json

        # the dummy dict to use as a serialization example
        inner_dict = {
            "foo": "bar"
        }

        class CustomClass:
            """ The class to test serialization with """
            def _json(self):
                return inner_dict

        # serialize an instance of the custom class
        serialized = ModelSerializer().serialize(CustomClass())

        assert isinstance(serialized, str), (
            "ModelSerializer did not return a string."
        )

        assert serialized == json.dumps(inner_dict), (
            'ModelSerializer did not return the correct string.'
        )
