"""
    This file is responsible for centralizing the action conventions used in nautilus.
    Most actions types take the form <method>_<target>
"""
from .models import getModelString


methods = {
    'createMethod' 'create',
    'editMethod' 'edit',
    'deleteMethod' 'delete',
    'updateMethod' 'update',
}


def getCRUDAction(method, model):
    return "{}_{}".format(methods[method], getModelString(model))
