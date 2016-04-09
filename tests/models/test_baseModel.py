# external imports
import unittest
# local imports
import nautilus.models as models


class TestUtil(unittest.TestCase):
    """
        This test suite checks for the various bits of introspective
        functinality supported by the base model.
    """

    def setUp(self):

        self.spy = unittest.mock.MagicMock()
        class TestUser(models.BaseModel):
            name = models.fields.CharField(null=True)
            date = models.fields.CharField(null=False)

            @classmethod
            def __mixin__(cls):
                # call the spy
                self.spy()

        self.Model = TestUser

    def test_can_retrieve_fields(self):
        # the name of the columns in the models
        column_names = {field.name for field in self.Model.fields()}
        # check the value
        assert column_names == {'name', 'date', 'id'}, (
            'Model could not retrieve columns'
        )


    def test_can_retrieve_primary_key(self):
        assert self.Model.primary_key().name == 'id', (
            'Model could not return primary keys'
        )


    def test_can_retrieve_requried_fields(self):
        # grab the names of the required fields
        required_field_names = {field.name for field in self.Model.required_fields()}
        # make sure it is what it should be
        assert required_field_names == {'id', 'date'}, (
            'Model could not retrieve required fields.'
        )


    def test_can_be_serialized_using_model_encoder(self):
        # import the model serializer
        from nautilus.models import ModelSerializer
        import json
        # create an instance of a model that we can serialize
        model = self.Model(name="foo", date="bar")
        # serialize the model
        serialized = ModelSerializer().serialize(model)
        # check that the serialized model can be hydrated as expected
        assert json.loads(serialized) == {
            "name": "foo", "date": "bar", 'id': None
        }, (
            'Model was not correctly serialized'
        )

    def test_can_add_on_creation_handler(self):
        assert self.spy.called, (
            "mixin spy wasn't called."
        )
