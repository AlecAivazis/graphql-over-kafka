# external imports
import unittest
# local imports
import nautilus
from ..util import MockModelService
from nautilus.contrib.graphene_peewee import convert_peewee_field
from nautilus.conventions.api import (
    root_query,
    create_mutation_inputs,
    create_mutation_outputs,
    update_mutation_inputs,
    update_mutation_outputs,
    delete_mutation_inputs,
    delete_mutation_outputs,
    _summarize_object_type,
    _summarize_o_mutation_type
)



class TestUtil(unittest.TestCase):
    """
        This test suite looks at the various utilities for manipulating
        models.
    """

    def setUp(self):
        # create a mock model service
        self.model_service = MockModelService()


    def test_root_query(self):
        # import the utility
        from nautilus.conventions.api import root_query

        # save the model to the test suite
        assert isinstance(root_query(), str), (
            "Could not a root query string for schema"
        )


    def test_crud_mutation_name(self):
        # import the utility
        from nautilus.conventions.api import crud_mutation_name

        # make sure we can generate a mutation name, and that it's a string
        assert isinstance(crud_mutation_name(self.model_service, 'create'), str), (
            "Could not generate string name for model service mutation"
        )


    def test_create_mutation_inputs(self):
        # create the list of inputs
        inputs = create_mutation_inputs(self.model_service)
        # make sure the inputs match the model
        from nautilus.api.util import summarize_mutation_io
        # the dictionary of fields corresponding to the service record
        field_dict = self.model_service.model._meta.fields

        # the expected values
        expected = [summarize_mutation_io(name=key, type=_graphql_type_string(value), required=(not value.null)) \
                        for key,value in field_dict.items()]

        # make sure the pk isn't required
        expected.remove([field for field in expected if field['name'] == 'id'][0])

        assert inputs == expected, (
            "Create mutation inputs did not match expecttations"
        )


    def test_create_mutation_outputs(self):
        # create the list of inputs
        outputs = create_mutation_outputs(self.model_service)

        # the output of a create mutation should be the object corresponding
        # to the model created

        assert outputs == [_summarize_o_mutation_type(self.model_service.model)], (
            "Create mutation output was not correct."
        )


    def test_update_mutation_inputs(self):
        # create the list of inputs
        inputs = update_mutation_inputs(self.model_service)

        # the inputs of an update mutation should be the fieldsof the object
        # no required args except pk to identify the target
        # make sure the inputs match the model

        from nautilus.api.util import summarize_mutation_io
        # the dictionary of fields corresponding to the service record
        field_dict = self.model_service.model._meta.fields

        # the expected values
        expected = [summarize_mutation_io(name=key, type=_graphql_type_string(value), required=(not value.null)) \
                        for key,value in field_dict.items()]
        # make sure only the pk is required
        for field in expected:
            if field['name'] == 'id':
                field['required'] = True
            else:
                field['required'] = False

        assert inputs == expected, (
            "Update mutation inputs did not match expecttations"
        )


    def test_update_mutation_outputs(self):
        # create the list of inputs
        inputs = update_mutation_outputs(self.model_service)

        # the output of an update mutation should be a graphql object corresponding
        # to the newly updated object
        assert inputs == [_summarize_o_mutation_type(self.model_service.model)], (
            "Update mutation output was not correct."
        )


    def test_delete_mutation_inputs(self):
        # the input of a delete mutation is just the pk of the model
        from nautilus.api.util import summarize_mutation_io

        # create the list of inputs
        inputs = delete_mutation_inputs(self.model_service)
        # the only input for delete events is the pk of the service record
        expected = [summarize_mutation_io(name='pk', type='ID', required=True)]

        # make sure the result matches what we expected
        assert inputs == expected, (
            "Delete mutation inputs were incorrect"
        )


    def test_delete_mutation_outputs(self):
        # delete the list of inputs
        inputs = delete_mutation_outputs(self.model_service)

        # the output of a delete mutation is a status message indicating wether or
        # not the mutation was successful

        from nautilus.api.util import summarize_mutation_io

        # the only input for delete events is the pk of the service record
        expected = [summarize_mutation_io(name='status', type='String', required=True)]

        # make sure the result matches what we expected
        assert inputs == expected, (
            "Delete mutation outputs were incorrect"
        )


    def test__summarize_object_type(self):
        from nautilus.api.util import summarize_mutation_io

        # summarize the model of the test service
        summarized = _summarize_object_type(self.model_service.model)

        target = {
            'fields': [
                {'type': 'String', 'name': 'date'},
                {'type': 'String', 'name': 'name'},
                {'type': 'ID', 'name': 'id'}
            ]
        }

        assert _stringify_dicts(target['fields']) == _stringify_dicts(summarized['fields']), (
            "Internal summary utility did not return the right object"
        )



def _graphql_type_string(value):
    return type(convert_peewee_field(value)).__name__


def _stringify_dicts(list_of_dicts):
    import json
    return {json.dumps(obj) for obj in list_of_dicts}
