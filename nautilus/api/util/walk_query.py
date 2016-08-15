async def walk_query(obj, object_resolver, connection_resolver, errors, current_user=None, __naut_name=None, obey_auth=True, **filters):
    """
        This function traverses a query and collects the corresponding
        information in a dictionary.
    """
    # if the object has no selection set
    if not hasattr(obj, 'selection_set'):
        # yell loudly
        raise ValueError("Can only resolve objects, not primitive types")

    # the name of the node
    node_name = __naut_name or obj.name.value if obj.name else obj.operation

    # the selected fields
    selection_set = obj.selection_set.selections

    def _build_arg_tree(arg):
        """
            This function recursively builds the arguments for lists and single values
        """
        # TODO: what about object arguments??

        # if there is a single value
        if hasattr(arg, 'value'):
            # assign the value to the filter
            return arg.value
        # otherwise if there are multiple values for the argument
        elif hasattr(arg, 'values'):
            return [_build_arg_tree(node) for node in arg.values]

    # for each argument on this node
    for arg in obj.arguments:
        # add it to the query filters
        filters[arg.name.value] = _build_arg_tree(arg.value)

    # the fields we have to ask for
    fields = [field for field in selection_set if not field.selection_set]
    # the links between objects
    connections = [field for field in selection_set if field.selection_set]

    try:
        # resolve the model with the given fields
        models = await object_resolver(node_name, [field.name.value for field in fields], current_user=current_user, obey_auth=obey_auth, **filters)
    # if something went wrong resolving the object
    except Exception as e:
        # add the error as a string
        errors.append(e.__str__())
        # stop here
        return None

    # add connections to each matching model
    for model in models:
        # if is an id for the model
        if 'pk' in model:
            # for each connection
            for connection in connections:
                # the name of the connection
                connection_name = connection.name.value
                # the target of the connection
                node = {
                    'name': node_name,
                    'pk': model['pk']
                }

                try:
                    # go through the connection
                    connected_ids, next_target = await connection_resolver(
                        connection_name,
                        node,
                    )

                    # if there are connections
                    if connected_ids:
                        # add the id filter to the list
                        filters['pk_in'] = connected_ids

                        # add the connection field
                        value = await walk_query(
                            connection,
                            object_resolver,
                            connection_resolver,
                            errors,
                            current_user=current_user,
                            obey_auth=obey_auth,
                            __naut_name=next_target,
                            **filters
                        )
                    # there were no connections
                    else:
                        value = []
                # if something went wrong
                except Exception as e:
                    # add the error as a string
                    errors.append(e.__str__())
                    # stop here
                    value = None

                # set the connection to the appropriate value
                model[connection_name] = value

    # return the list of matching models
    return models

