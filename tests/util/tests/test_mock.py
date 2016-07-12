# external imports
import unittest
# local imports
from tests.util.mock import Mock

class TestUtil(unittest.TestCase):

    def setUp(self):
        # create a mock
        self.mock = Mock()

    def test_must_be_called_more_than_once(self):
        try:
            # check that the mock has been called
            self.mock.assert_called()
        # it throws an assertion error
        except AssertionError:
            pass


    def test_default_fails_multiple_calls(self):
        # call the mock twice
        self.mock()
        self.mock()

        # expect this check to fail
        try:
            # check that the mock has been called
            self.mock.assert_called()
        # it throws an assertion error
        except AssertionError:
            pass


    def test_can_check_for_args(self):
        # pass some args to the mock
        self.mock('bar', 'baz')
        # verify that the mock was called with the args
        self.mock.assert_called('bar', 'baz')


    def test_can_check_for_kwds(self):
        # pass some kwds to the mock
        self.mock(foo='bar')
        # verify that th emock was called with the args
        self.mock.assert_called(foo='bar')
