# external imports
import unittest
# local imports
import nautilus.models as models


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
            def __mixin__(cls):
                # call the spy
                spy()

        class TestOnCreationModel(models.BaseModel, Mixin):
            first_name = models.fields.CharField()
            last_name = models.fields.CharField()

        # then number of times the spy was called
        num_called = len(spy.call_args_list)

        assert len(spy.call_args_list) > 0, (
            "Mixin's method wasn't called."
        )

        assert spy.called_once_with(TestOnCreationModel), (
            "Mixin's method was either called too many times or not"+ \
                                                "passed the class record."
        )


    def test_both_on_success_handlers(self):

        # spies to check if the handler was called
        spy1 = unittest.mock.MagicMock()
        spy2 = unittest.mock.MagicMock()

        class MyAwesomeMixin:
            @classmethod
            def __mixin__(cls):
                # call the spy
                spy2()

        class TestOnCreationModel(models.BaseModel, MyAwesomeMixin):
            first_name = models.fields.CharField()
            last_name = models.fields.CharField()

            @classmethod
            def __mixin__(cls):
                # call the spy
                spy1(cls)

        assert spy1.called_once_with(TestOnCreationModel), (
            "Base mixin method wasn't called  when there were both."
        )

        assert spy2.called_once_with(TestOnCreationModel), (
            "Mixin mixin method wasn't called when there were both."
        )
