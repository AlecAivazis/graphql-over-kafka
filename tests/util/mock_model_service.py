import nautilus
from .mock_model import MockModel

def MockModelService():
    class MockService(nautilus.ModelService):
        model = MockModel()

    return MockService