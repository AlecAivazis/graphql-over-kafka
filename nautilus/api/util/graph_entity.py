# external imports
import json
import asyncio
# from collections.abc import Iterable
# local imports
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
                assert source.owner.foo(arg=2) == 5
    """

    def __init__(self, event_broker, model_type=None, id=None, _api_path=None):
        # save the event broker reference
        self.event_broker = event_broker

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
        return GraphEntity(event_broker=self.event_broker, _api_path=self._api_path)


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
        return GraphEntity(event_broker=self.event_broker, _api_path=self._api_path)


    def __eq__(self, other):
        """
            Equality checks are overwitten to perform the actual check in a
            semantic way.
        """
        # the current event loop
        event_loop = asyncio.get_event_loop()
        # first perform the query associated with the entity
        result = event_loop.run_until_complete(self.event_broker.ask(
            action_type=query_action_type(),
            payload=self._query,
        ))
        # go to the bottom of the result for the list of matching ids
        return self._find_id(result, other)


    def _find_id(self, result, uid):
        """
            This method performs a depth-first search for the given uid in the dictionary of results.
        """
        # if we've found the result
        if result == uid:
            # we're done
            return True

        # otherwise if there is a list to traverse
        elif isinstance(result, list):
            # go over the entries in the list and return true if there is a match
            return any([self._find_id(item, uid) for item in result])

        # otherwise the entry could be a dictionary
        elif isinstance(result, dict):
            # go over every item
            for key, value in result.items():
                # if the value is a match
                if self._find_id(value, uid):
                    # we're done
                    return True

        # we didn't find the result
        return False

