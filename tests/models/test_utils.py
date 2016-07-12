# external imports
import unittest
# local imports
import nautilus.models as models
from nautilus.conventions.services import model_service_name

class TestUtil(unittest.TestCase):
    """
        This test suite checks the behavior of the various model utilities that
        come with nautilus.
    """

    def test_can_create_connection_model(self):
        import nautilus

        # models to test
        Model1 = model_service_name('Model1')
        Model2 = model_service_name('Model2')

        class TestConnectionService(nautilus.ConnectionService):
            to_service = (Model1,)
            from_service = (Model2,)

        # create the connection model
        connection_model = nautilus.models.create_connection_model(TestConnectionService())

        assert issubclass(connection_model, models.BaseModel), (
            "Generated connection model is not an instance of BaseModel"
        )

        # grab the name of the fields
        connect_fields = {field.name for field in connection_model.fields()}

        assert connect_fields == {Model1, Model2, 'id'}, (
            "Connection model did not have the correct fields."
        )
