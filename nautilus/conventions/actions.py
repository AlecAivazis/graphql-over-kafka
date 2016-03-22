"""
    This file is responsible for centralizing the action conventions used in nautilus.
"""
from .models import get_model_string

def get_crud_action(method, model, status='pending'):
    return "%s.%s.%s" % (method, get_model_string(model), status)
