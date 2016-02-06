"""
    This file is responsible for centralizing the action conventions used in nautilus.
    Most actions types take the form <method>_<target>
"""


methods = {
    'createMethod' 'create',
    'editMethod' 'edit',
    'deleteMethod' 'delete',
    'updateMethod' 'update',
}

def actionTargetForModel(model):
    """
        This function returns the conventional action designator for a given model.
    """
    return model.__name__.lower()


def getCRUDAction(method, model):
    return "{}_{}".format(methods[method], actionTargetForModel(model))
