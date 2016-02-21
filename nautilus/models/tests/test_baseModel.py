import unittest
from unittest.mock import MagicMock

class TestUtil(unittest.TestCase):

    def test_can_be_serialized_using_model_encoder(self):

        # import the model serializer
        from sqlalchemy import Column, Text
        from nautilus.models import ModelSerializer, BaseModel
        import json

        class Model(BaseModel):
            name =  Column(Text, primary_key = True)

        model = Model(name="foo")

        serialized = ModelSerializer().serialize(model)

        assert serialized == json.dumps({"name": "foo"}), (
            'Model was not correctly serialized'
        )




