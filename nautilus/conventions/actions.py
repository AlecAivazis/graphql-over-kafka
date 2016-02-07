"""
    This file is responsible for centralizing the action conventions used in nautilus.
"""
from .models import get_model_string

def getCRUDAction(method, model):
    return "{}_{}".format(method, get_model_string(model))
