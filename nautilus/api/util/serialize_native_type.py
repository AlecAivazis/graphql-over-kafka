# local imports
from nautilus.contrib.graphene_peewee import convert_peewee_field

def serialize_native_type(native_type):
    """
        This function serializes the native object type for summaries
    """
    return type(convert_peewee_field(native_type)).__name__