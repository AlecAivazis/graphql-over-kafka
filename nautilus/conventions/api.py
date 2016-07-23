"""
    This file is responsible for centralizing the schema conventions used in nautilus.
"""
# external imports
from functools import singledispatch
# local imports
import nautilus
from .models import normalize_string, get_model_string
from nautilus.contrib.graphene_peewee import convert_peewee_field

def root_query(*service):
    ''' This function returns the name of the root query for a model service. '''
    return 'all_models'


def crud_mutation_name(action, model):
    """
        This function returns the name of a mutation that performs the specified
        crud action on the given model service
    """
    return "{}_{}".format(action, get_model_string(model))


def create_mutation_inputs(service):
    """
        Args:
            service : The service being created by the mutation
        Returns:
            (list) : a list of all of the fields availible for the service,
                with the required ones respected.
    """
    # grab the default list of field summaries
    inputs = _service_mutation_summaries(service)
    # make sure the pk isn't in the list
    inputs.remove([field for field in inputs if field['name'] == 'id'][0])

    # return the final list
    return inputs


def create_mutation_outputs(service):
    """
        Args:
            service : The service being created by the mutation
        Returns:
            (list of single dict): A single output representing the object type
                for the service record that was created.
    """
    return [_summarize_object_type(service.model)]



def update_mutation_inputs(service):
    """
        Args:
            service : The service being updated by the mutation
        Returns:
            (list) : a list of all of the fields availible for the service. Pk
                is a required field in order to filter the results
    """
    # grab the default list of field summaries
    inputs = _service_mutation_summaries(service)

    # return the final list
    return inputs



def update_mutation_outputs(service):
    """
        Args:
            service : The service being updated by the mutation
        Returns:
            (list of single dict): A single output representing the object type
                for the service record that was updated.
    """
    return [_summarize_object_type(service.model)]



def delete_mutation_inputs(service):
    """
        Args:
            service : The service being deleted by the mutation
        Returns:
            ([str]):  the only input for delete is the pk of the service.
    """
    from nautilus.api.util import summarize_mutation_io

    # the only input for delete events is the pk of the service record
    return [summarize_mutation_io(name='pk', type='ID', required=True)]


def delete_mutation_outputs(service):
    """
        Args:
            service : The service being deleted by the mutation
        Returns:
            (str): A string providing a status message
    """
    from nautilus.api.util import summarize_mutation_io

    # the only input for delete events is the pk of the service record
    return [summarize_mutation_io(name='status', type='String', required=True)]


def _service_mutation_summaries(service):
    from nautilus.api.util import summarize_mutation_io
    # the dictionary of fields corresponding to the service record
    field_dict = service.model._meta.fields

    def _graphql_type_string(value):
        return type(convert_peewee_field(value)).__name__

    # mutation io summaries
    inputs = [summarize_mutation_io(name=key, type=_graphql_type_string(value), required=(not value.null)) \
                    for key,value in field_dict.items()]

    return inputs


def _summarize_object_type(model):
    # the fields for the service's model
    model_fields = {field.name: field for field in list(model.fields())}
    # summarize the model
    return {
        'name': model._meta.name,
        'fields': [{
            'name': key,
            'type': type(convert_peewee_field(value)).__name__
            } for key, value in model_fields.items()
        ]
    }
