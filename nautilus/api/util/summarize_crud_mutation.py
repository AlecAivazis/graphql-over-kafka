# local imports
from nautilus.conventions.actions import get_crud_action
from nautilus.conventions.models import get_model_string
from .summarize_mutation import summarize_mutation
from nautilus.conventions.api import (
    create_mutation_inputs,
    update_mutation_inputs,
    delete_mutation_inputs,
    create_mutation_outputs,
    update_mutation_outputs,
    delete_mutation_outputs,
    crud_mutation_name,
)

def summarize_crud_mutation(method, model, isAsync=False):
    """
        This function provides the standard form for crud mutations.
    """

    # create the approrpriate action type
    action_type = get_crud_action(method=method, model=model)
    # the name of the mutation
    name = crud_mutation_name(model=model, action=method)
    # a mapping of methods to input factories
    input_map = {
        'create': create_mutation_inputs,
        'update': update_mutation_inputs,
        'delete': delete_mutation_inputs,
    }
    # a mappting of methods to output factories
    output_map = {
        'create': create_mutation_outputs,
        'update': update_mutation_outputs,
        'delete': delete_mutation_outputs,
    }
    # the inputs for the mutation
    inputs = input_map[method](model)
    # the mutation outputs
    outputs = output_map[method](model)

    # return the appropriate summary
    return summarize_mutation(
        mutation_name=name,
        event=action_type,
        isAsync=isAsync,
        inputs=inputs,
        outputs=outputs
    )
