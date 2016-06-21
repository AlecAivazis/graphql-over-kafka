"""
    This file is responsible for centralizing the model conventions used in nautilus.
"""

def normalize_string(string):
    return string[0].lower() + string[1:]

def get_model_string(model):
    """
        This function returns the conventional action designator for a given model.
    """
    return model if isinstance(model, str) else normalize_string(model.__name__)
