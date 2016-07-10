# external imports
import unittest
# local imports
import nautilus


class TestUtil(unittest.TestCase):
    """
        This test suite looks at the various utilities for manipulating
        models.
    """

    def test_root_query(self):
        # import the utility
        from nautilus.conventions.api import root_query

        # save the model to the test suite
        assert isinstance(root_query(), str), (
            "Could not a root query string for schema"
        )
