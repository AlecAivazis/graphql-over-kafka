# external imports
import unittest
# local imports
import nautilus.models as models


class TestUtil(unittest.TestCase):
    """
        This test suite checks the behavior of the various model utilities that
        come with nautilus.
    """

    def test_can_create_connection_model(self):
        from nautilus.models import create_connection_model

        # models to test
        class Model1(models.BaseModel):
            first_name = models.fields.CharField()
        class Model2(models.BaseModel):
            first_name = models.fields.CharField()

        # create the connection model
        connection_model = create_connection_model([Model1, Model2])

        assert issubclass(connection_model, models.BaseModel), (
            "Generated connection model is not an instance of BaseModel"
        )

        # grab the name of the fields
        connect_fields = {field.name for field in connection_model.fields()}

        assert connect_fields == {Model1.model_name.lower(), Model2.model_name.lower(), 'id'}, (
            "Connection model did not have the correct fields."
        )
