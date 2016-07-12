# external imports
import unittest
import json
# local imports
from nautilus.conventions.actions import (
    get_crud_action,
    change_action_status,
    intialize_service_action,
    success_status,
    error_status,
    pending_status,
)
from ..util import MockModel


class TestUtil(unittest.TestCase):
    """
        This test suite looks at the various utilities for manipulating
        action types.
    """

    def setUp(self):
        # save the model to the test suite
        self.model = MockModel()


    def test_can_generate_crud_action_types(self):
        #  try to creat a crud action for a model
        action_type = get_crud_action(
            method='create',
            model=self.model
        )

        assert action_type == 'create.testModel.pending', (
            "New action type did not have the correct form."
        )


    def test_can_change_action_types(self):

        #  try to creat a crud action for a model
        action_type = get_crud_action(method='create', model=self.model)
        # try to change the action
        success_action = change_action_status(action_type, 'success')
        # make sure the new action type is in the result
        assert success_action == 'create.testModel.success', (
            "New action type did not have the correct form."
        )


    def test_can_generate_init_action_for_service(self):
        # verify we get a string back
        assert isinstance(intialize_service_action(), str)


    def test_can_generate_init_action_catchall(self):
        # create the action
        action = intialize_service_action(all_services=True)
        # verify we got a string back
        assert isinstance(action, str) and '*' in action


    def test_can_serialize_and_deserialize_action(self):
        from nautilus.conventions.actions import serialize_action, hydrate_action
        # the target
        target = dict(
            action_type='hello',
            payload='world'
        )
        # the hydrated form of the object
        serialized = serialize_action(**target)

        # make sure we can hydrate the hydrated form into the target
        assert hydrate_action(serialized) == target, (
            "Could not serialize/deserialize action."
        )


    def test_can_serialize_and_deserialize_action_with_extra_fields(self):
        from nautilus.conventions.actions import serialize_action, hydrate_action
        # the target
        target = dict(
            foo='bar',
            action_type='hello',
            payload='world'
        )
        # the hydrated form of the object
        serialized = serialize_action(**target)
        # make sure we can hydrate the hydrated form into the target
        assert hydrate_action(serialized) == target, (
            "Could not serialize action with extra fields."
        )


    def test_can_hydrate_extra_fields(self):
        from nautilus.conventions.actions import serialize_action, hydrate_action
        # the target
        target = dict(action_type='foo', payload='bar', foo='bar')
        # the serialized form of the object
        serialized = serialize_action(**target)
        # make sure we can hydrate the serialized form into the target
        assert hydrate_action(serialized) == target, (
            "Could not hydrate action with extra fields."
        )


    def test_has_success_status(self):
        # create the success status
        status = success_status()
        # make sure its a string
        assert isinstance(status, str)


    def test_has_error_status(self):
        # create the error status
        status = error_status()
        # make sure its a string
        assert isinstance(status, str)


    def test_has_pending_status(self):
        # create the pending status
        status = pending_status()
        # make sure its a string
        assert isinstance(status, str)
