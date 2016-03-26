import unittest
from unittest.mock import MagicMock

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
        type = 'foo'
        payload = {'foo': 'bar'}
        # call the combined handler
        mergedActionHandler(type, payload)
        # make sure each mock was called
        handleMock1.assert_called_once_with(type, payload)
        handleMock2.assert_called_once_with(type, payload)
        handleMock3.assert_called_once_with(type, payload)
