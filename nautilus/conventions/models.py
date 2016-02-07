"""
    This file is responsible for centralizing the model conventions used in nautilus.
"""

def get_model_string(model):
    """
        This function returns the conventional action designator for a given model.
    """
    return model.__name__.lower()
