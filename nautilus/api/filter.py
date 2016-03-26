# external imports
from graphene import List
# local imports
from nautilus.contrib.graphene_peewee import convert_peewee_field

def args_for_model(Model):
    # the attribute arguments (no filters)
    args = { field.name.lower() : convert_peewee_field(field) \
                                        for field in Model.fields() }

    # add the primary key filter

    # the primary keys for the Model
    primary_key = Model.primary_key()
    # add the primary key filter to the arg dictionary
    args['pk'] = convert_peewee_field(primary_key)

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
    return models.all()
