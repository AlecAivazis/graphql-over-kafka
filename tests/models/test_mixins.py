# external imports
import unittest
# local imports
import nautilus.models as models


class TestUtil(unittest.TestCase):
    """
        This test suite checks the behavior of the various mixins that come
        with nautilus.
    """

    def test_can_extend_models_with_mixins(self):

        class Mixin(models.Model):
            address = models.fields.CharField(null=True)

        class TestModel(Mixin, models.BaseModel):
            first_name = models.fields.CharField()
            last_name = models.fields.CharField()

        # the name of the fields of test models
        field_names = set([field.name for field in TestModel.fields()])

        # make sure the mixin was applied to the table
        assert (
            field_names == set(['address', 'id', 'first_name', 'last_name'])
        ), (
            'mixin was not properly applied to model' \
        )
