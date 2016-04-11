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

@singledispatch
def convert_peewee_field(field):
    """
        This helper converts a peewee field type into the appropriate type
        for a graphql schema.
    """
    raise ValueError(
        "Unable to convert peewee field %s " % field
    )


@convert_peewee_field.register(fields.CharField)
@convert_peewee_field.register(fields.DateField)
@convert_peewee_field.register(fields.DateTimeField)
@convert_peewee_field.register(fields.FixedCharField)
@convert_peewee_field.register(fields.TextField)
@convert_peewee_field.register(fields.TimeField)
@convert_peewee_field.register(fields.UUIDField)
def convert_field_to_string(field):
    return String(description=field.help_text)


@convert_peewee_field.register(fields.PrimaryKeyField)
def convert_field_to_pk(field):
    return ID(description=field.help_text)


@convert_peewee_field.register(fields.IntegerField)
@convert_peewee_field.register(fields.BigIntegerField)
def convert_field_to_int(field):
    return Int(description=field.help_text)


@convert_peewee_field.register(fields.DecimalField)
@convert_peewee_field.register(fields.DoubleField)
@convert_peewee_field.register(fields.FloatField)
def convert_field_to_float(field):
    return Float(description=field.help_text)


@convert_peewee_field.register(fields.BooleanField)
def convert_field_to_bool(field):
    return Boolean(description=field.help_text)
