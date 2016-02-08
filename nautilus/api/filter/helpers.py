# external imports
from graphene import List
from sqlalchemy.inspection import inspect
# local imports
from nautilus.api import convert_sqlalchemy_type

def args_for_model(Model):
    # the attribute arguments (no filters)
    args = { column.name.lower() : convert_sqlalchemy_type(column.type, column) \
                                        for column in inspect(Model).columns }

    # add the primary key filter

    # the primary keys for the Model
    primary_keys = inspect(Model).primary_key
    # make sure there is only one
    assert len(primary_keys) == 1, "Can only support one primary key - how would I know what to reference for joins?"

    primary_key = primary_keys[0]
    # figure out the type of the primary key
    primary_key_type = convert_sqlalchemy_type(primary_key.type, primary_key)
    # add the primary key filter to the arg dictionary
    args['pk'] = primary_key_type

    # create a copy of the argument dict we can mutate
    fullArgs = args.copy()

    # todo: add type-specific filters
    # go over the arguments
    for arg, type in args.items():
        # add the list member filter
        fullArgs[arg + '_in'] = List(type)

    # return the complete dictionary of arguments
    return fullArgs


def filter_model(Model, args):

    # convert any args referencing pk to the actual field
    keys = [key.replace('pk', inspect(Model).primary_key[0].name) for key in args.keys()]

    # start off with the full list of Models
    models = Model.query
    # for each argument
    for arg, value in zip(keys, args.values()):
        # if the filter is for a group of values
        if isinstance(value, list):
            # filter the query
            models = models.filter(getattr(Model, arg[:-3]).in_(value))
        else:
            # filter the argument
            models = models.filter(getattr(Model, arg) == value)

    # return the filtered list
    return models.all()
