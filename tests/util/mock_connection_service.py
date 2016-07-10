import nautilus

def MockConnectionService():

    """
        This function returns a nautilus model to use throughout the test suite.
    """

    class TestConnection(nautilus.ConnectionService):
        from_service = ('TestService',)
        to_service = ('AnotherTestService')

    # return the mocked model
    return TestConnection