import json
import requests

from nautilus.conventions.services import api_gateway_name
from nautilus.network.registry import service_location_by_name

def query_graphql_service(url, name, fields, filters=None, query_type='query'):
    """ A graphql query wrapper factory """

    # by default there are no args to add to the query
    args = ''
    # if there are filters defined for the query
    if filters:
        # construct the argument string out of the given dictionary
        arg_string = ', '.join(['{}: {}'.format(key, json.dumps(value)) \
                                            for key, value in filters.items()])
        args = "(%s)" % arg_string if len(arg_string) > 0  else ''

    # construct the field string
    field_list = ', '.join(fields)

    # build the query out of the given paramters
    query = "%s { %s %s { %s } }" % (query_type, name, args, field_list)

    # query the service to retrieve the data
    data_request = requests.get(url + '?query='   + query).json()
    # if there is an error
    if 'errors' in data_request and data_request['errors']:
        raise RuntimeError(data_request['errors'])
    # otherwise there is no error
    else:
        # return the data
        return data_request['data'][name]


def query_service(service, fields, name=None, filters=None):
    '''
        Apply the given filters to a query of a model service given its name
        and the desired fields.
    '''
    # necessary imports
    from nautilus.conventions import root_query
    # query the target using model service conventions
    return query_graphql_service(
        url='http://{}'.format(service_location_by_name(service)),
        name=name or root_query(service),
        fields=fields,
        filters=filters or {}
    )


def query_api(model, fields, filters=None):
    '''
        Perform the given query on the api gateway and turn the results.
        Use this function to avoid hard coding the name of the api gateway.
    '''
    # query the api
    return query_service(api_gateway_name(), fields, filters, name=model)


def wait_for_response(): pass


def combine_action_handlers(*args):
    """
        This function combines the given action handlers into a single function
        which will call all of them.
    """
    # the combined action handler
    def combined_action_handler(action_type, payload):
        # goes over every given handler
        for handler in args:
            # call the handler
            handler(action_type, payload)

    # return the combined action handler
    return combined_action_handler
