from json import JSONEncoder

class ModelSerializer(JSONEncoder):
    """
        This encoder serializes nautilus models to JSON
    """

    def default(self, obj):
        try:
            # use the custom json handler
            return obj._json()

        # if the custom json handler doesn't exist
        except AttributeError:
            # perform the normal behavior
            return JSONEncoder.default(self, obj)

    def serialize(self, obj):
        """
            This function performs the serialization on the given object.
        """
        return self.encode(obj)
