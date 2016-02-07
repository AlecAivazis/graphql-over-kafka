# external imports
from graphene import List
from sqlalchemy.inspection import inspect
# local imports
from nautilus.api import convert_sqlalchemy_type

def args_for_model(Model):
    # the attribute arguments (no filters)
    args = { column.name.lower() : convert_sqlalchemy_type(column.type, column) \
                                        for column in inspect(Model).columns }

    # create a copy of the argument dict we can mutate
    fullArgs = args.copy()

    # todo: add type-specific filters
    # go over the arguments
    for arg, type in args.items():
        # add the list member filter
        fullArgs[arg + '__in'] = List(type)

    # return the complete dictionary of arguments
    return fullArgs

def filter_model(Model, args):
    # start off with the full list of Models
    models = Model.query
    # for each argument
    for arg, value in args.items():
        # if the filter is for a group of values
        if isinstance(value, list):
            # filter the query
            models = models.filter(getattr(Model, arg[:-4]).in_(value))
        else:
            # filter the argument
            models = models.filter(getattr(Model, arg) == value)

    # return the filtered list
    return models.all()
