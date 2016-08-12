import json

class GraphEntity:
    """
        This entity describes an entity path between a source node and
        another entity in the api graph and allows for "equality" checks
        that verify if there is a matching entity.

        Example:

            .. code-block:: python

                source = GraphEntity(model_type='CatPhoto', id=1)

                # check if there is a user with id 5 associated with the photo
                assert source.owner.foo(arg=2) == 5
    """

    def __init__(self, model_type=None, id=None, _api_path=None):
        # if there is a source specification
        if model_type and id:
            # the internal api needs to start at the appropriate node
            self._api_path = [{"name": model_type, "args": {"id": id}}]
        # they could also specify the api path to start from
        elif _api_path:
            # set the path to the given value
            self._api_path = _api_path
        # otherwise we weren't given a valid starting point
        else:
            # yell loudly
            raise ValueError("GraphEntity need to start at a given path or model_type/id")


    def __getattr__(self, attr):
        """
            Attribute retrieval is overwritten to build the path we care about
        """
        # add a node with no arguments to the api path
        self._api_path.append({
            "name": attr,
            "args": {},
        })
        # return the entity so we can continue building the path
        return GraphEntity(_api_path=self._api_path)


    @property
    def _query(self):
        """
            This attribute provides the graphql query corresponding to the api path
        """
        return "query { %s }" % self._summarize_node(self._api_path)


    def _summarize_node(self, node_list):
        # if there are not entries in the node list (the base case)
        if not node_list:
            # return the id field
            return 'id'

        # grab the top of the node list
        node = node_list.pop(0)

        # if there are arguments for the node
        if node['args']:
            # add the starting parenthesis
            arg_string = '('
            # construct the argument string
            for key, value in node['args'].items():
                # add the key to the arg string
                arg_string += "%s : %s" % (key, json.dumps(value))

            # close the parenthesis
            arg_string += ')'

        # otherwise there are no arguments for the node
        else:
            # just use an empty string
            arg_string = ''

        return "%s %s { %s }" % (node['name'], arg_string, self._summarize_node(node_list))


    def __call__(self, **kwds):
        """
            Calling the entity adds the arguments to the head of its path.
        """
        # set the args of the tail of the path to the given keywords
        self._api_path[-1]['args'] = kwds
        # return the entity so we can continue building the path
        return GraphEntity(_api_path=self._api_path)


    def __eq__(self, other):
        """
            Equality checks are overwitten to perform the actual check in a
            semantic way.
        """
