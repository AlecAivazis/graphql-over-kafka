# external imports
import unittest
# local imports
import nautilus.models as models
from nautilus.contrib.graphene_peewee import PeeweeObjectType
from ...util import MockModel

class TestUtil(unittest.TestCase):

    def setUp(self):

        # the base model to test
        TestModel = MockModel()

        # the object type based on the models
        class TestObjectType(PeeweeObjectType):
            class Meta:
                model = TestModel

        # save the mocks to the test case
        self.model = TestModel
        self.object_type = TestObjectType


    def test_generated_object_has_model_fields(self):
        # the list of fields in the service object
        service_object_fields = {field.default_name \
                                    for field in self.object_type._meta.fields}
        # the list of fields in the models
        model_fields = {field.name for field in self.model.fields()}
        # make sure the two lists are the same
        assert model_fields == service_object_fields, (
            "PeeweeObjectType does not have the same fields as the model"
        )
