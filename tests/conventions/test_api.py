# external imports
import unittest
# local imports
import nautilus
from nautilus.models import BaseModel, fields


class TestUtil(unittest.TestCase):
    """
        This test suite looks at the various utilities for manipulating
        models.
    """

    def test_model_string(self):
        # import the utility
        from nautilus.conventions.api import root_query

        class TestModel(BaseModel):
            first_name = fields.CharField()

        # save the model to the test suite
        assert isinstance(root_query(), str), (
            "Could not a root query string for schema"
        )
