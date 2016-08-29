# external imports
import json
import graphql
import functools
# local imports
import nautilus
from nautilus.config import Config
from nautilus.network.http import Response
from nautilus.api.util import parse_string
from .graphql import GraphQLRequestHandler


class APIQueryHandler(GraphQLRequestHandler):
    """
        The api query handler parses and executes the query by hand,
        requesting the appropriate data over the action system. Queries
        are validated using the internally tracked schema maintained by
        the service.
    """

    async def _handle_query(self, query):


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

        # by default there is no current user
        current_user = None

        # if there is an authorization header
        if 'Authorization' in self.request.headers:
            # the authorization header value
            auth_header = self.request.headers['Authorization']
            # the name of the token method
            method = 'Bearer'
            # only accept bearer tokens
            if method in auth_header:
                # pull the session token out from the header value
                session_token = auth_header.replace(method, '').strip()
                # create a config object from the current user session
                current_user = Config(self.service._read_session_token(session_token))

        # otherwise its a normal query/mutation so walk it like normal
        response = await parse_string(
            query,
            self.service.object_resolver,
            self.service.connection_resolver,
            self.service.mutation_resolver,
            extra_mutations={
                'loginUser': self.service.login_user,
                'registerUser': self.service.register_user
            },
            current_user=current_user
        )

        # pass the result to the request
        return Response(body=json.dumps(response).encode())
