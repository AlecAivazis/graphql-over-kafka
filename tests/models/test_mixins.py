# external imports
import unittest
# local imports
import nautilus.models as models
from ..util import Mock


class TestUtil(unittest.TestCase):
    """
        This test suite checks the behavior of the various mixins that come
        with nautilus.
    """

    def test_can_add_fields_with_mixin(self):

        class Mixin(models.BaseModel):
            address = models.fields.CharField(null=True)

        class TestModel(Mixin, models.BaseModel):
            first_name = models.fields.CharField()
            last_name = models.fields.CharField()

        # the name of the fields of test models
        field_names = {field.name for field in TestModel.fields()}

        # make sure the mixin was applied to the table
        assert field_names == {'address', 'id', 'first_name', 'last_name'}, (
            'mixin was not properly applied to model'
        )

    def test_can_add_on_creation_handler_with_mixin(self):

        # a spy to check if the handler was called
        spy = Mock()

        class Mixin:
            @classmethod
            def __mixin__(cls, target):
                # call the spy
                spy(target)

        class TestOnCreationModel(models.BaseModel, Mixin):
            first_name = models.fields.CharField()
            last_name = models.fields.CharField()

        # verify that the mock was called with the correct arguments
        spy.assert_called(TestOnCreationModel)


    def test_multiple_mixins(self):

        # spies to check if the handler was called
        spy1 = Mock()
        spy2 = Mock()

        class MyAwesomeMixin:
            @classmethod
            def __mixin__(cls, target):
                # call the spy
                spy2(target)

        class MyOtherAwesomeMixin:
            @classmethod
            def __mixin__(cls, target):
                # call the spy
                spy1(target)

        class TestOnCreationModel(models.BaseModel, MyAwesomeMixin, MyOtherAwesomeMixin):
            first_name = models.fields.CharField()
            last_name = models.fields.CharField()


        # check that both spies were called
        spy1.assert_called(TestOnCreationModel)
        spy2.assert_called(TestOnCreationModel)