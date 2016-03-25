"""
    This module defines various patches for peewee to easily interact with
    graphene.
"""

# external imports
from functools import singledispatch
from graphene.core.types.scalars import (
    Boolean,
    Float,
    ID,
    Int,
    String,
)
# local imports
import nautilus.models.fields as fields

def convert_peewee_field(field):
    """
        This utility converts the given peewee field into the corresponding
        graphql scalar
    """
    return convert_peewee_type(field, field)

@singledispatch
def convert_peewee_type(field_type, field):
    """
        This helper converts a peewee field type into the appropriate type
        for a graphql schema.
    """
    raise ValueError(
        "Unable to convert peewee field %s (%s)" % (field, field_type)
    )


@convert_peewee_type.register(fields.CharField)
@convert_peewee_type.register(fields.DateField)
@convert_peewee_type.register(fields.DateTimeField)
@convert_peewee_type.register(fields.FixedCharField)
@convert_peewee_type.register(fields.TextField)
@convert_peewee_type.register(fields.TimeField)
@convert_peewee_type.register(fields.UUIDField)
def convert_field_to_string(field_type, field):
    return String(description=field.help_text)


@convert_peewee_type.register(fields.PrimaryKeyField)
def convert_field_to_pk(field_type, field):
    return ID(description=field.help_text)


@convert_peewee_type.register(fields.IntegerField)
@convert_peewee_type.register(fields.BigIntegerField)
def convert_field_to_int(field_type, field):
    return Int(description=field.help_text)


@convert_peewee_type.register(fields.DecimalField)
@convert_peewee_type.register(fields.DoubleField)
@convert_peewee_type.register(fields.FloatField)
def convert_field_to_float(field_type, field):
    return Float(description=field.help_text)


@convert_peewee_type.register(fields.BooleanField)
def convert_field_to_bool(field_type, field):
    return Boolean(description=field.help_text)
