# local imports
from nautilus.conventions.actions import get_crud_action
from nautilus.conventions.api import crud_mutation_name
from nautilus.conventions.models import get_model_string
from .summarize_mutation import summarize_mutation

def summarize_crud_mutation(method, model, isAsync=False):
    """
        This function provides the standard form for crud mutations.
    """
    # create the approrpriate action type
    action_type = get_crud_action(method=method, model=model)
    # the name of the mutation
    name = crud_mutation_name(model=model, action=method)
    # return the appropriate summary
    return summarize_mutation(mutation_name=name, event=action_type, isAsync=isAsync)
