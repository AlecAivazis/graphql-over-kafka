# external imports
import unittest
from unittest.mock import call
# local imports
import nautilus.models as models
from ..util import assert_called_once_with


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
        spy = unittest.mock.MagicMock()

        class Mixin:
            @classmethod
            def __mixin__(cls, target):
                # call the spy
                spy(target)

        class TestOnCreationModel(models.BaseModel, Mixin):
            first_name = models.fields.CharField()
            last_name = models.fields.CharField()

        # then number of times the spy was called
        num_called = len(spy.call_args_list)

        assert num_called > 0, (
            "Mixin's method wasn't called."
        )
        assert len(spy.call_args_list) == 1, (
            "Mixin's method was called too many times."
        )
        assert spy.call_args_list == [call(TestOnCreationModel)], (
            "Mixin method was not passed the correct class record."
        )


    def test_multiple_mixins(self):

        # spies to check if the handler was called
        spy1 = unittest.mock.MagicMock()
        spy2 = unittest.mock.MagicMock()

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
        assert_called_once_with(spy1, TestOnCreationModel, spy_name='Base spy')
        assert_called_once_with(spy2, TestOnCreationModel, spy_name='Mixin spy')
