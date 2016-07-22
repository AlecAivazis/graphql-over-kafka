# external imports
import unittest
# local imports
import nautilus
from ..util import MockModelService


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

    def test_crud_mutation_name(self):
        # import the utility
        from nautilus.conventions.api import crud_mutation_name

        # a model service to mock
        mock = MockModelService()
        # make sure we can generate a mutation name, and that it's a string
        assert isinstance(crud_mutation_name(mock, 'create'), str), (
            "Could not generate string name for model service mutation"
        )
