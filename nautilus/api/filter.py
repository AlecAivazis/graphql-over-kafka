# external imports
from graphene import List
# local imports
from nautilus.contrib.graphene_peewee import convert_peewee_field

def args_for_model(Model):
    # import the model field helper
    from .helpers import fields_for_model

    # figure use each field as a filter
    args = fields_for_model(Model)
    # create a copy of the argument dict we can mutate
    fullArgs = args.copy()

    # todo: add type-specific filters
    # go over the arguments
    for arg, field_type in args.items():
        # add the list member filter
        fullArgs[arg + '_in'] = List(field_type)

    # return the complete dictionary of arguments
    return fullArgs


def filter_model(Model, args):

    # convert any args referencing pk to the actual field
    keys = [key.replace('pk', Model.primary_key().name) for key in args.keys()]

    # start off with the full list of Models
    models = Model.select()
    # for each argument
    for arg, value in zip(keys, args.values()):
        # if the filter is for a group of values
        if isinstance(value, list):
            model_attribute = getattr(Model, arg[:-3])
            # filter the query
            models = models.where(model_attribute.in_(value))
        else:
            # filter the argument
            models = models.where(getattr(Model, arg) == value)

    # return the filtered list
    return list(models)
