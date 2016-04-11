# external imports
import unittest
# local imports
from nautilus.models import BaseModel, fields
from nautilus.conventions.actions import (
    get_crud_action,
    change_action_status
)


class TestUtil(unittest.TestCase):
    """
        This test suite looks at the various utilities for manipulating
        action types.
    """

    def setUp(self):

        class TestModel(BaseModel):
            first_name = fields.CharField()

        # save the model to the test suite
        self.model = TestModel


    def test_can_generate_crud_action_types(self):
        #  try to creat a crud action for a model
        action_type = get_crud_action(
            method='create',
            model=self.model
        )

        assert action_type == 'create.testmodel.pending', (
            "New action type did not have the correct form."
        )


    def test_can_change_action_types(self):

        #  try to creat a crud action for a model
        action_type = get_crud_action(method='create', model=self.model)
        # try to change the action
        success_action = change_action_status(action_type, 'success')
        # make sure the new action type is in the result
        assert success_action == 'create.testmodel.success', (
            "New action type did not have the correct form."
        )
