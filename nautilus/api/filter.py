# external imports
from graphene import List
from graphql.type.scalars import GraphQLString
from graphene.core.types.scalars import Int
# local imports
from nautilus.contrib.graphene_peewee import convert_peewee_field

def args_for_model(model):
    # import the model field helper
    from .util import fields_for_model

    # figure use each field as a filter
    args = fields_for_model(model)
    # add the pk argument
    args['pk'] = convert_peewee_field(model.primary_key())
    # create a copy of the argument dict we can mutate
    full_args = args.copy()

    # todo: add type-specific filters
    # go over the arguments
    for arg, field_type in args.items():
        # add the list member filter
        full_args[arg + '_in'] = List(field_type)

    # add integer valued model filters
    for arg in ['first', 'last', 'offset']:
        # add the arg to the dict
        full_args[arg] = Int()

    # add the list of string values model filters
    for arg in ['order_by']:
        # add the arg to the dict
        full_args[arg] = List(GraphQLString)

    # return the complete dictionary of arguments
    return full_args


def filter_model(model, args):

    # convert any args referencing pk to the actual field
    filter_args = {key.replace('pk', model.primary_key().name): value \
                        for key, value in args.items()}

    # pull out the meta filters
    first = filter_args.pop('first', None)
    last = filter_args.pop('last', None)
    order_by = filter_args.pop('order_by', None)
    offset = filter_args.pop('offset', None)

    if len({'first', 'last', 'order_by'}.intersection(set(filter_args.keys()))) > 1:
    # if the user specified both first and last filters
        # yell loudly
        raise ValueError("Please specify one of first, last, and order_by filters")

    # start off with the full list of models
    models = model.select()

    # for each argument
    for arg, value in filter_args.items():
        # if the filter is for a group of values
        if isinstance(value, list):
            # remove the `_in` from the key
            model_attribute = getattr(model, arg[:-3])
            # filter the query
            models = models.where(model_attribute.in_(value))
        else:
            try:
                # filter the argument
                models = models.where(getattr(model, arg) == value)
            # if the model doesn't have the attribute
            except AttributeError:
                # maybe the capitalization is off
                try:
                    # invert the first letter
                    first_letter = arg[0].title() if arg[0].islower() else arg[0].lower()
                    # try filtering with the first letter invetered
                    models = models.where(getattr(model, first_letter + arg[1:]) == value)
                    # print(first_letter + arg[1:])

                # if that still fails
                except AttributeError as err:
                    # yell loudly
                    raise ValueError("Could not handle filter %s: %s" % (arg, err))


    # if the user specified an ordering
    if order_by:
        # apply the ordering to the model
        models = models.order_by(*_parse_order_by(model, order_by))
    # otherwise there is no order by
    else:
        # the filter to use for the primary key
        model_filter = ('-' if last else '+') + model.primary_key().name
        # order the models by their primary key
        models = models.order_by(*_parse_order_by(model, [model_filter]))

    # if there is an offset
    if offset:
        # apply the offset to the selection
        models = models.offset(offset)

    # if there are any limits to apply
    if first or last:
        # apply the limiting segmentations
        models = models.limit(first or last)

    # return the filtered list
    return list(models)


def _parse_order_by(model, order_by):
    """
        This function figures out the list of orderings for the given model and
        argument.

        Args:
            model (nautilus.BaseModel): The model to compute ordering against
            order_by (list of str): the list of fields to order_by. If the field
                starts with a `+` then the order is acending, if `-` descending,
                if no character proceeds the field, the ordering is assumed to be
                ascending.

        Returns:
            (list of filters): the model filters to apply to the query
    """
    # the list of filters for the models
    out = []
    # for each attribute we have to order by
    for key in order_by:
        # remove any whitespace
        key = key.strip()
        # if the key starts with a plus
        if key.startswith("+"):
            # add the ascending filter to the list
            out.append(getattr(model, key[1:]))
        # otherwise if the key starts with a minus
        elif key.startswith("-"):
            # add the descending filter to the list
            out.append(getattr(model, key[1:]).desc())
        # otherwise the key needs the default filter
        else:
            # add the default filter to the list
            out.append(getattr(model, key))

    # returnt the list of filters
    return out
