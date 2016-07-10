# external imports
import unittest
# local imports
import nautilus.models as models
from ..util import MockModel


class TestUtil(unittest.TestCase):
    """
        This test suite checks for the various bits of introspective
        functinality supported by the base model.
    """

    def setUp(self):

        self.spy = unittest.mock.MagicMock()

        # create a mock model
        self.model_record = MockModel()
        # create the test table
        self.model_record.create_table(True)

        self.model = self.model_record()


    def tearDown(self):
        self.model_record.drop_table()


    def test_can_be_saved_and_retrieved(self):
        # fill the model with test values
        self.model.name = 'foo'
        self.model.date = 'bar'
        # save it to the database
        self.model.save()

        # make sure we can get the corresponding record
        self.model_record.get(self.model_record.id == self.model.id)


    def test_can_retrieve_fields(self):
        # the name of the columns in the models
        column_names = {field.name for field in self.model_record.fields()}
        # check the value
        assert column_names == {'name', 'date', 'id'}, (
            'Model could not retrieve columns'
        )


    def test_can_retrieve_primary_key(self):
        assert self.model_record.primary_key().name == 'id', (
            'Model could not return primary keys'
        )


    def test_can_retrieve_requried_fields(self):
        class TestModel(self.model_record):
            foo = models.fields.CharField(null=False)

        # grab the names of the required fields
        required_field_names = {field.name for field in TestModel().required_fields()}
        # make sure it is what it should be
        assert required_field_names == {'id', 'foo'}, (
            'Model could not retrieve required fields.'
        )


    def test_can_be_serialized_using_model_encoder(self):
        # import the model serializer
        from nautilus.models import ModelSerializer
        import json
        # create an instance of a model that we can serialize
        model = self.model_record(name="foo", date="bar")
        # serialize the model
        serialized = ModelSerializer().serialize(model)
        # check that the serialized model can be hydrated as expected
        assert json.loads(serialized) == {
            "name": "foo", "date": "bar", 'id': None
        }, (
            'Model was not correctly serialized'
        )
