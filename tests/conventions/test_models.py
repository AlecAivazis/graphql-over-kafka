# external imports
import unittest
# local imports
from nautilus.models import BaseModel, fields
from nautilus.conventions.models import get_model_string


class TestUtil(unittest.TestCase):
    """
        This test suite looks at the various utilities for manipulating
        models.
    """

    def test_model_string(self):

        class TestModel(BaseModel):
            first_name = fields.CharField()

        # save the model to the test suite
        assert isinstance(get_model_string(TestModel), str), (
            "Could not generate string for model"
        )
