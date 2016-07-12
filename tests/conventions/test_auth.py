# external imports
import unittest
# local imports
from nautilus.conventions.auth import cookie_name


class TestUtil(unittest.TestCase):
    """
        This test suite looks at the various utilities for manipulating
        models.
    """

    def test_cookie_name(self):

        # save the model to the test suite
        assert isinstance(cookie_name(), str), (
            "Could not generate string for model"
        )
