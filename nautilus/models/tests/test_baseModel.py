import unittest
from unittest.mock import MagicMock

import nautilus.models as models


class TestUtil(unittest.TestCase):
    """
        This test suite checks for the various bits of introspective
        functinality supported by the base model.
    """

    def setUp(self):

        class User(models.BaseModel):
            name = models.fields.CharField(null=False, unique=True)
            date = models.fields.CharField(null=False)

        self.Model = User


    def test_can_retrieve_columns(self):
        assert self.Model.columns == ['name', 'date'], (
            'Model could not retrieve columns'
        )


    def test_can_retrieve_primary_keys(self):
        assert self.Model.primary_keys == ['name'], (
            'Model could not return primary keys'
        )


    def test_can_retrieve_requried_fields(self):
        assert self.Model.required_fields == ['date'], (
            'Model could not retrieve required fields.'
        )


    def test_can_be_serialized_using_model_encoder(self):
        # import the model serializer
        from nautilus.models import ModelSerializer
        import json


        model = self.Model(name="foo", date="bar")

        serialized = ModelSerializer().serialize(model)

        assert serialized == json.dumps({
            "name": "foo", "date": "bar"
        }), (
            'Model was not correctly serialized'
        )



