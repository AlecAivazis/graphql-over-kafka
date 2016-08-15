# external imports
import json
import asyncio
# local imports
from nautilus.api.util import parse_string
from nautilus.conventions.actions import query_action_type

class GraphEntity:
    """
        This entity describes an entity path between a source node and
        another entity in the api graph and allows for "equality" checks
        that verify if there is a matching entity.

        Example:

            .. code-block:: python

                source = GraphEntity(model_type='CatPhoto', id=1)

                # check if there is a user with id 5 associated with the photo
                assert 5 in source.owner.foo(arg=2)
    """

    def __init__(self, service, model_type=None, id=None, _api_path=None):
        # save the event broker reference
        self.service = service

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
        return GraphEntity(service=self.service, _api_path=self._api_path)


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
        return GraphEntity(service=self.service, _api_path=self._api_path)


    async def _has_id(self, *args, **kwds):
        """
            Equality checks are overwitten to perform the actual check in a
            semantic way.
        """
        # if there is only one positional argument
        if len(args) == 1:
            # parse the appropriate query
            result = await parse_string(
                self._query,
                self.service.object_resolver,
                self.service.connection_resolver,
                self.service.mutation_resolver,
                obey_auth=False
            )
            # go to the bottom of the result for the list of matching ids
            return self._find_id(result['data'], args[0])
        # otherwise
        else:
            # treat the attribute like a normal filter
            return self._has_id(**kwds)



    def _find_id(self, result, uid):
        """
            This method performs a depth-first search for the given uid in the dictionary of results.
        """
        # if the result is a list
        if isinstance(result, list):
            # if the list has a valid entry
            if any([self._find_id(value, uid) for value in result]):
                # then we're done
                return True

        # otherwise results could be dictionaries
        if isinstance(result, dict):
            # the children of the result that are lists
            list_children = [value for value in result.values() if isinstance(value, list)]

            # go to every value that is a list
            for value in list_children:
                # if the value is a match
                if self._find_id(value, uid):
                    # we're done
                    return True

            # the children of the result that are dicts
            dict_children = [value for value in result.values() if isinstance(value, dict)]

            # perform the check on every child that is a dict
            for value in dict_children:
                # if the child is a match
                if self._find_id(value, uid):
                    # we're done
                    return True

            # if there are no values that are lists and there is an id key
            if not list_children and not dict_children and 'id' in result:
                # the value of the remote id field
                result_id = result['id']
                # we've found a match if the id field matches (cast to match type)
                return result_id == type(result_id)(uid)

        # we didn't find the result
        return False

