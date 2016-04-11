import unittest
from unittest.mock import MagicMock
from ..util import assert_called_once_with

class TestUtil(unittest.TestCase):

    def test_can_merge_action_handlers(self):
        # import the function to be tested
        from nautilus.network.util import combine_action_handlers

        # create some handler mocks to make sure they were tested
        handleMock1 = MagicMock()
        handleMock2 = MagicMock()
        handleMock3 = MagicMock()
        # merge a series of mock handlers
        mergedActionHandler = combine_action_handlers(
            handleMock1,
            handleMock2,
            handleMock3,
        )

        # the type and payload to pass to the merged handler
        action_type = 'foo'
        payload = {'foo': 'bar'}

        # call the combined handler
        mergedActionHandler(action_type, payload)
        # make sure each mock was called
        assert_called_once_with(handleMock1, action_type, payload)
        assert_called_once_with(handleMock2, action_type, payload)
        assert_called_once_with(handleMock3, action_type, payload)
