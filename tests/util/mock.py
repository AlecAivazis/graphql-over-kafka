class Mock:
    """
        This class attempts to implement most common data structure interfaces
        as well as provide an introspective API on actions performed in order
        to facilitate testing.
    """

    def __init__(self):
        # the information about each call of the mock
        self._call_list = []


    def assert_called(self, *args, **kwds):
        """
            This function returns true if the mock has been called the
            designated number of times with the given arguments.
        """
        # compute the length of the call list
        ncalls = len(self._call_list)
        # make sure the mock was called at all
        assert ncalls > 0, (
            "Mock was never called."
        )
        # make sure its the correct value
        assert ncalls == 1, (
            "Mock was not called the correct number of times. " + \
            "Expected {} and found {}.".format(1, ncalls)
        )

        # use the first call to verify the criteria
        call = self._call_list[0]

        # if there are arguments to check
        if args:
            # verify they match up
            assert call['args'] == args, (
                "Passed arguments do not match the call."
            )
        # if there are keywords to check
        if kwds:
            assert call['kwds'] == kwds, (
                "Passed keywords do not match the call."
            )


    def __call__(self, *args, **kwds):
        """
            This makes instances of the Mock class callable
        """
        # add the arguments to the call number
        self._call_list.append({
            'args': args,
            'kwds': kwds
        })