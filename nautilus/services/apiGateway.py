# external imports
import aiohttp_cors
from collections.abc import Callable
from collections import defaultdict
import json
import functools
# local imports
from nautilus.auth.models import UserPassword
import nautilus.database
import nautilus.api.endpoints.requestHandlers.apiQuery as api_query
import nautilus.network.events.consumers.api as api_handler
from nautilus.conventions.services import api_gateway_name
from nautilus.conventions.actions import roll_call_type
from nautilus.conventions.actions import get_crud_action
from nautilus.conventions.api import root_query
from nautilus.auth.util import generate_session_token, read_session_token
from nautilus.api.endpoints import static_dir as api_endpoint_static
from nautilus.api.util import query_for_model, arg_string_from_dict
from .service import Service
from nautilus.api.util import GraphEntity
from nautilus.api.util import parse_string
from nautilus.api.endpoints import (
    GraphiQLRequestHandler,
    GraphQLRequestHandler
)


class APIGateway(Service):
    """
        This provides a single endpoint that other services and clients can
        use to query the cloud without worrying about the distributed nature
        of the system.

        Example:

            .. code-block:: python

                # external imports
                import nautilus

                # local imports
                from .schema import schema

                class MyAPIGateway(nautilus.APIGateway):
                    schema = schema
    """
    name = api_gateway_name()
    model = UserPassword
    api_request_handler_class = api_query.APIQueryHandler
    action_handler = api_handler.APIActionHandler
    _external_service_data = defaultdict(list)
    secret_key = None

    def __init__(self, *args, **kwds):
        # bubble up
        super().__init__(*args, **kwds)
        # attach this service to the action handler
        self.action_handler.service = self
        # do any sort of database setup
        self.init_db()
        # make sure there is a valid secret key


    def init_db(self):
        """
            This function configures the database used for models to make
            the configuration parameters.
        """
        # get the database url from the configuration
        db_url = self.config.get('database_url', 'sqlite:///passwords.db')
        # configure the nautilus database to the url
        nautilus.database.init_db(db_url)


    # when its time for the service to announce itself
    async def announce(self):
        # bubble up
        await super().announce()
        # ask for rollcall aswell
        await self.event_broker.send(
            action_type=roll_call_type(),
            payload='please report yourself'
        )


    @property
    def auth_criteria(self):
        """
            This attribute provides the mapping of services to their auth requirement

            Returns:
                (dict) : the mapping from services to their auth requirements.
        """
        # the dictionary we will return
        auth = {}

        # go over each attribute of the service
        for attr in dir(self):
            # make sure we could hit an infinite loop
            if attr != 'auth_criteria':
                # get the actual attribute
                attribute = getattr(self, attr)
                # if the service represents an auth criteria
                if isinstance(attribute, Callable) and hasattr(attribute, '_service_auth'):
                    # add the criteria to the final results
                    auth[getattr(self, attr)._service_auth] = attribute

        # return the auth mapping
        return auth


    def init_routes(self):
        # add the cors handler
        self.cors = aiohttp_cors.setup(self.app)

        # for each route that was registered
        for route in self._routes:
            # add the corresponding http endpoint
            self.add_http_endpoint(**route)

        # add the schema reference to graphql handler
        self.api_request_handler_class.service = self

        # add a cors resource
        api_resource = self.cors.add(self.app.router.add_resource("/"))
        # add the root api handler
        self.cors.add(
            api_resource.add_route("GET", self.api_request_handler_class),
            {
                "": aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers=("X-Custom-Server-Header",),
                    allow_headers=("X-Requested-With", "Content-Type"),
                    max_age=3600,
                )
            }
        )
        # add the static file urls
        self.app.router.add_static('/graphiql/static/', api_endpoint_static)
        # add the graphiql endpoint
        self.add_http_endpoint('/graphiql', GraphiQLRequestHandler)


    async def login_user(self, password, **kwds):
        """
            This function handles the registration of the given user credentials in the database
        """
        # find the matching user with the given email
        user_data = (await self._get_matching_user(fields=list(kwds.keys()), **kwds))['data']
        try:
            # look for a matching entry in the local database
            passwordEntry = self.model.select().where(
                self.model.user == user_data[root_query()][0]['pk']
            )[0]
        # if we couldn't acess the id of the result
        except (KeyError, IndexError) as e:
            # yell loudly
            raise RuntimeError('Could not find matching registered user')


        # if the given password matches the stored hash
        if passwordEntry and passwordEntry.password == password:
            # the remote entry for the user
            user = user_data[root_query()][0]
            # then return a dictionary with the user and sessionToken
            return {
                'user': user,
                'sessionToken': self._user_session_token(user)
            }

        # otherwise the passwords don't match
        raise RuntimeError("Incorrect credentials")


    async def register_user(self, password, **kwds):
        """
            This function is used to provide a sessionToken for later requests.

            Args:
                uid (str): The
        """
        # so make one
        user = await self._create_remote_user(password=password, **kwds)
        # if there is no pk field
        if not 'pk' in user:
            # make sure the user has a pk field
            user['pk'] = user['id']

        # the query to find a matching query
        match_query = self.model.user == user['id']

        # if the user has already been registered
        if self.model.select().where(match_query).count() > 0:
            # yell loudly
            raise RuntimeError('The user is already registered.')

        # create an entry in the user password table
        password = self.model(user=user['id'], password=password)

        # save it to the database
        password.save()

        # return a dictionary with the user we created and a session token for later use
        return {
            'user': user,
            'sessionToken': self._user_session_token(user)
        }


    async def object_resolver(self, object_name, fields, obey_auth=False, current_user=None, **filters):
        """
            This function resolves a given object in the remote backend services
        """

        try:
            # check if an object with that name has been registered
            registered = [model for model in self._external_service_data['models'] \
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
        query = query_for_model(fields, **filters)

        # the action type for the question
        action_type = get_crud_action('read', object_name)

        # query the appropriate stream for the information
        response = await self.event_broker.ask(
            action_type=action_type,
            payload=query
        )

        # treat the reply like a json object
        response_data = json.loads(response)

        # if something went wrong
        if 'errors' in response_data and response_data['errors']:
            # return an empty response
            raise ValueError(','.join(response_data['errors']))

        # grab the valid list of matches
        result = response_data['data'][root_query()]

        # grab the auth handler for the object
        auth_criteria = self.auth_criteria.get(object_name)

        # if we care about auth requirements and there is one for this object
        if obey_auth and auth_criteria:

            # build a second list of authorized entries
            authorized_results = []

            # for each query result
            for query_result in result:
                # create a graph entity for the model
                graph_entity = GraphEntity(self, model_type=object_name, id=query_result['pk'])
                # if the auth handler passes
                if await auth_criteria(model=graph_entity, user_id=current_user):
                    # add the result to the final list
                    authorized_results.append(query_result)

            # overwrite the query result
            result = authorized_results

        # apply the auth handler to the result
        return result


    def user_session(self, user):
        """
            This method handles what information the api gateway stores about
            a particular user in their session.
        """
        return {
            'id': user['pk']
        }


    async def connection_resolver(self, connection_name, object):

        try:
            # grab the recorded data for this connection
            expected = [ conn for conn in self._external_service_data['connections']\
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
        query = query_for_model(fields, **filters).replace("'", '"')

        # the action type for the question
        action_type = get_crud_action('read', connection_name)

        # get the service name for the connection
        response = json.loads(await self.event_broker.ask(
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


    async def mutation_resolver(self, mutation_name, args, fields):
        """
            the default behavior for mutations is to look up the event,
            publish the correct event type with the args as the body,
            and return the fields contained in the result
        """

        try:
            # make sure we can identify the mutation
            mutation_summary = [mutation for mutation in \
                                            self._external_service_data['mutations'] \
                                            if mutation['name'] == mutation_name][0]
        # if we couldn't get the first entry in the list
        except KeyError as e:
            # make sure the error is reported
            raise ValueError("Could not execute mutation named: " + mutation_name)


        # the function to use for running the mutation depends on its schronicity
        # event_function = self.event_broker.ask \
        #                     if mutation_summary['isAsync'] else self.event_broker.send
        event_function = self.event_broker.ask

        # send the event and wait for a response
        value =  await event_function(
            action_type=mutation_summary['event'],
            payload=args
        )
        try:
            # return a dictionary with the values we asked for
            return json.loads(value)

        # if the result was not valid json
        except json.decoder.JSONDecodeError:
            # just throw the value
            raise RuntimeError(value)


    def get_models(self):
        """
            Returns the models managed by this service.

            Returns:
                (list): the models managed by the service
        """
        return [self.model]

    ## internal utilities

    def _user_session_token(self, user):
        # grab the session for this particular user
        user_session = self.user_session(user)
        # return the token signed by the services secret key
        return generate_session_token(self.secret_key, **user_session)


    def _read_session_token(self, token):
        # make sure the token is valid while we're at it
        return read_session_token(self.secret_key, token)


    async def _get_matching_user(self, fields=[], **filters):
        # the action type for a remote query
        read_action = get_crud_action(method='read', model='user')
        # the fields of the user to ask for
        user_fields = ['pk'] + fields

        # the query for matching entries
        payload = """
            query {
                %s(%s) {
                    %s
                }
            }
        """ % (root_query(), arg_string_from_dict(filters), '\n'.join(user_fields))

        # perform the query and return the result
        return json.loads(await self.event_broker.ask(
            action_type=read_action,
            payload=payload
        ))



    async def _check_for_matching_user(self, **user_filters):
        """
            This function checks if there is a user with the same uid in the
            remote user service
            Args:
                **kwds : the filters of the user to check for
            Returns:
                (bool): wether or not there is a matching user
        """
        # there is a matching user if there are no errors and no results from
        user_data = self._get_matching_user(user_filters)

        # return true if there were no errors and at lease one  result
        return not user_data['errors'] and len(user_data['data'][root_query()])


    async def _create_remote_user(self, **payload):
        """
            This method creates a service record in the remote user service
            with the given email.
            Args:
                uid (str): the user identifier to create
            Returns:
                (dict): a summary of the user that was created
        """
        # the action for reading user entries
        read_action = get_crud_action(method='create', model='user')

        # see if there is a matching user
        user_data = await self.event_broker.ask(
            action_type=read_action,
            payload=payload
        )
        # treat the reply like a json object
        return json.loads(user_data)
