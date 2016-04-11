# external imports
import unittest
# local imports
from nautilus.models import BaseModel, fields
from nautilus.conventions.schema import root_query


class TestUtil(unittest.TestCase):
    """
        This test suite looks at the various utilities for manipulating
        models.
    """

    def test_model_string(self):

        class TestModel(BaseModel):
            first_name = fields.CharField()

        # save the model to the test suite
        assert isinstance(root_query(), str), (
            "Could not a root query string for schema"
        )
