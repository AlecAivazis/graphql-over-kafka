import unittest
from ..util import Mock

class TestUtil(unittest.TestCase):

    def test_can_merge_action_handlers(self):
        # import the function to be tested
        from nautilus.network.events.util import combine_action_handlers

        # create some handler mocks to make sure they were tested
        handleMock1 = Mock()
        handleMock2 = Mock()
        handleMock3 = Mock()

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
        mergedActionHandler(Mock(), action_type, payload)
        # make sure each mock was called
        handleMock1.assert_called(action_type, payload)
        handleMock2.assert_called(action_type, payload)
        handleMock3.assert_called(action_type, payload)
