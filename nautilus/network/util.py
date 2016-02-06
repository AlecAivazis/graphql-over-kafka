import json, requests

def queryGraphQLService(url, name, filedList, filterDict = {}):
    """ A graphql query wrapper factory"""

    # construct the argument string out of the given dictionary
    argString = ', '.join(['{}: {}'.format(key, json.dumps(value)) for key,value in filterDict.items()])
    args = "(%s)" % argString if len(argString) > 0  else ''

    # construct the field string
    fields = ', '.join(filedList)

    # build the query out of the given paramters
    query = """
        query {
            %s %s {
                %s
            }
        }
    """ % (name, args, fields)

    # query the service to retrieve the data
    dataRequest = requests.get(url + '?query='   + query).json()
    # if there is an error
    if 'errors' in dataRequest:
        raise RuntimeError(dataRequest['errors'])
    # otherwise there is no error
    else:
        # return the data
        return dataRequest['data'][name]


def combineActionHandlers(*args):
    """
        This function combines the given action handlers into a single function
        which will call all of them.
    """
    # the combined action handler
    def combinedActionHandler(type, payload):
        # goes over every given handler
        for handler in args:
            # call the handler
            handler(type, payload)

    # return the combined action handler
    return combinedActionHandler
