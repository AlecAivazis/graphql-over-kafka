def MockModel():

    """
        This function returns a nautilus model to use throughout the test suite.
    """
    # local imports
    from nautilus import models

    class TestModel(models.BaseModel):
        name = models.fields.CharField(null=True)
        date = models.fields.CharField(null=True)

    # return the mocked model
    return TestModel