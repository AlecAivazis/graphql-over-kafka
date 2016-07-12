# external imports
import unittest
# local imports
from nautilus.conventions.models import get_model_string, normalize_string
from ..util import MockModel

class TestUtil(unittest.TestCase):
    """
        This test suite looks at the various utilities for manipulating
        models.
    """

    def test_model_string(self):

        model = MockModel()

        # save the model to the test suite
        assert isinstance(get_model_string(model), str), (
            "Could not generate string for model"
        )

    def test_normalize_string_handles_ClassCase(self):
        string = 'FooBar'

        assert normalize_string(string) == 'fooBar', (
            "ClassCase string could not be normalized"
        )