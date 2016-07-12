def MockModel(name='TestModel'):

    """
        This function returns a nautilus model to use throughout the test suite.
    """
    # local imports
    from nautilus import models

    # return the mocked model
    return type(name, (models.BaseModel,), {
        'name': models.fields.CharField(null=True),
        'date': models.fields.CharField(null=True)
    })