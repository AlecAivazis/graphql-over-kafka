import unittest
from unittest.mock import MagicMock
from ..util import assert_called_once_with

class TestUtil(unittest.TestCase):

    def test_can_merge_action_handlers(self):
        # import the function to be tested
        from nautilus.network.events.util import combine_action_handlers

        # create some handler mocks to make sure they were tested
        handleMock1 = MagicMock()
        handleMock2 = MagicMock()
        handleMock3 = MagicMock()

        async def asyncHandler1():
            handleMock1()
        async def asyncHandler2():
            handleMock2()
        async def asyncHandler3():
            handleMock3()

        # merge a series of mock handlers
        mergedActionHandler = combine_action_handlers(
            asyncHandler1,
            asyncHandler2,
            asyncHandler3,
        )

        # the type and payload to pass to the merged handler
        action_type = 'foo'
        payload = {'foo': 'bar'}

        # call the combined handler
        mergedActionHandler(MagicMock(), action_type, payload)
        # make sure each mock was called
        assert_called_once_with(handleMock1, action_type, payload)
        assert_called_once_with(handleMock2, action_type, payload)
        assert_called_once_with(handleMock3, action_type, payload)
