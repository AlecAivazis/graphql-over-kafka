import unittest
from ..util import Mock, async_test

class TestUtil(unittest.TestCase):

    @async_test
    async def test_can_merge_action_handlers(self):
        # import the function to be tested
        from nautilus.network.events.util import combine_action_handlers

        # create some handler mocks to make sure they were tested
        handleMock1 = Mock()
        handleMock2 = Mock()
        handleMock3 = Mock()

        async def asyncHandler1(*args):
            handleMock1(*args)
        async def asyncHandler2(*args):
            handleMock2(*args)
        async def asyncHandler3(*args):
            handleMock3(*args)

        # merge a series of mock handlers
        mergedActionHandler = combine_action_handlers(
            asyncHandler1,
            asyncHandler2,
            asyncHandler3,
        )

        # the type and payload to pass to the merged handler
        action_type = 'foo'
        payload = {'foo': 'bar'}

        spy = Mock()

        # call the combined handler
        await mergedActionHandler(spy, action_type, payload, {})
        # make sure each mock was called
        handleMock1.assert_called(spy, action_type, payload, {})
        handleMock2.assert_called(spy, action_type, payload, {})
        handleMock3.assert_called(spy, action_type, payload, {})
