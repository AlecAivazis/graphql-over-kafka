# external imports
import json
import graphql
# local imports
import nautilus
from nautilus.network.http import Response
from nautilus.conventions.actions import get_crud_action
from nautilus.api.util import parse_string
from .graphql import GraphQLRequestHandler


class APIQueryHandler(nautilus.api.endpoints.GraphQLRequestHandler):
    """
        The api query handler parses and executes the query by hand,
        requesting the appropriate data over the action system. Queries
        are validated using the internally tracked schema maintained by
        the service.
    """

    async def _handle_query(self, query):

        async def object_resolver(object_name, fields, **filters):
            """
                This function performs the actual query for the given
                object and fields. Returns the
            """

            try:
                # check if an object with that name has been registered
                registered = [model for model in self.service._connection_data['models'] \
                                    if model['name']==object_name][0]
            # if there is no connection data yet
            except AttributeError:
                raise ValueError("No objects are registered with this schema yet.")
            # if we dont recognize the model that was requested
            except IndexError:
                raise ValueError("Cannot query for object {} on this service.".format(object_name))

            # the valid fields for this object
            valid_fields = [field['name'] for field in registered['fields']]

            # figure out if any invalid fields were requested
            invalid_fields = [field for field in fields if field not in valid_fields]
            try:
                # make sure we never treat pk as invalid
                invalid_fields.remove('pk')
            # if they weren't asking for pk as a field
            except ValueError:
                pass

            # if there were
            if invalid_fields:
                # yell loudly
                raise ValueError("Cannot query for fields {!r} on {}".format(
                    invalid_fields, registered['name']
                ))

            # make sure we include the id in the request
            fields.append('pk')

            # the query for model records
            query = self._query_for_model(fields, **filters)

            # the action type for the question
            action_type = get_crud_action('read', object_name)

            # query the appropriate stream for the information
            response = await self.service.event_broker.ask(
                action_type=action_type,
                payload=query
            )
            # treat the reply like a json object
            response_data = json.loads(response)

            # if something went wrong
            if 'errors' in response_data and response_data['errors']:
                # return an empty response
                raise ValueError(','.join(response_data['errors']))

            # otherwise it was a successful query so return the result
            return response_data['data']['all_models']


        async def connection_resolver(connection_name, object):

            try:
                # grab the recorded data for this connection
                expected = [ conn for conn in self.service._connection_data['connections']\
                                  if conn['name'] == connection_name][0]
                                              # if there is no connection data yet
            except AttributeError:
                raise ValueError("No objects are registered with this schema yet.")
            # if we dont recognize the model that was requested
            except IndexError:
                raise ValueError("Cannot query for {} on {}.".format(connection_name, object['name']))

            # the target of the connection
            to_service = expected['connection']['to']['service']

            # ask for only the entries connected to the object
            filters = {object['name']: object['pk']}
            # the field of the connection is the model name
            fields = [to_service]

            # the query for model records
            query = self._query_for_model(fields, **filters).replace("'", '"')

            # the action type for the question
            action_type = get_crud_action('read', connection_name)

            # get the service name for the connection
            response = json.loads(await self.service.event_broker.ask(
                action_type=action_type,
                payload=query
            ))

            if 'errors' in response and response['errors']:
                # return an empty response
                raise ValueError(','.join(response['errors']))

            # grab the ids from the response
            ids = [int(entry[to_service]) for entry in response['data']['all_models']]

            # the question for connected nodes
            return ids, to_service

        # if there hasn't been a schema generated yet
        if not self.schema:
            # yell loudly
            result = json.dumps({
                'data': {},
                'errors': ['No schema for this service.']
            })
            # send the result of the introspection to the user
            return Response(body=result.encode())

        try:
            # figure out if the query is an introspection
            is_introspection = graphql.parse(query).definitions[0].name.value == 'IntrospectionQuery'
        # if something went wrong
        except AttributeError:
            # its not
            is_introspection = False

        # if the query is an introspection
        if is_introspection:
            # handle it using the schema
            introspection = self.service.schema.execute(query)
            result = json.dumps({
                'data': {key: value for key,value in introspection.data.items()},
                'errors': introspection.errors
            })
            # send the result of the introspection to the user
            return Response(body=result.encode())


        # otherwise its a normal query/mutation

        # walk the query
        response = await parse_string(query, object_resolver, connection_resolver)

        # pass the result to the request
        return Response(body=json.dumps(response).encode())


    def _query_for_model(self, fields, **filters):
        # if there are filters
        if filters:
            # the string for the filters
            filter_string = "(%s)" % ",".join("{}: {!r}".format(key, value) for key,value in filters.items())
        else:
            filter_string = ''

        # the query for the requested data
        return """
            query {
                all_models%s {
                    %s
                }
            }
        """ % (filter_string, ', '.join(fields))
