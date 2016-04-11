import collections

class Config(dict):
    """
        This class creates a general api for configuration.
    """

    def __init__(self, *args, **kwds):

        # start off with the given values
        values = kwds
        # for each argument passed
        for arg in args:
            # if the argument is a dictionary
            if isinstance(arg, dict):
                values.update(arg)
            # otherwise if the argument is a class record
            if isinstance(arg, type):
                values.update(self._from_type(arg))

        # use the kwds as keys
        self.update(kwds)


    def __getattr__(self, attr):
        """
            This method allows the retrieval of internal keys like attributes
        """
        # access the dictionary for attributes
        return self[attr]


    def __setattr__(self, attr, value):
        """
            This method allows the setting of internal keys like attributes
        """
        # update the internal structure
        self[attr] = value


    def _from_type(self, config):
        """
            This method converts a type into a dict.
        """
        def is_user_attribute(attr):
            return (
                not attr.startswith('__') and
                not isinstance(getattr(config, attr), collections.abc.Callable)
            )

        return {attr: getattr(config, attr) for attr in dir(config) \
                                                    if is_user_attribute(attr)}
