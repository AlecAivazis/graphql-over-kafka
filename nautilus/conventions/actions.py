"""
    This file is responsible for centralizing the action conventions used in nautilus.
"""
from .models import get_model_string


methods = {
    'createMethod' 'create',
    'editMethod' 'edit',
    'deleteMethod' 'delete',
    'updateMethod' 'update',
}


def getCRUDAction(method, model):
    return "{}_{}".format(methods[method], get_model_string(model))
