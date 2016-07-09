"""
    This file is responsible for centralizing the model conventions used in nautilus.
"""

def normalize_string(string):
    return string[0].lower() + string[1:]

def get_model_string(model):
    """
        This function returns the conventional action designator for a given model.
    """
    name = model if isinstance(model, str) else model.__name__
    return normalize_string(name)
