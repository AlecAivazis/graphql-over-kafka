# external imports
import threading
import consul
from nautilus.network import registry
from consul import Check
from flask import Flask
from flask_graphql import GraphQLView, GraphQL
from flask_login import LoginManager
# local imports
from nautilus.network.consumers import ActionConsumer

class Service:
    """
        This is the base class for all services that are part of a nautilus
        cloud. This class provides basic functionalities such as registration,
        responding to actions, and predictable api endpoints.

        Args:

            actionHandler (optional, function): The callback function fired when
                an action is recieved. If None, the service does not connect to the
                action queue.

            auth (optional, bool, default = True): Whether or not the service should add
                authentication requirements.

            auto_register (optional, bool): Whether or not the service should
                register itself when ran

            configObject (optional, class): A python class to use for configuring the
                service.

            name (string): The name of the service. This will be used to
                register the service with the registry as act as the designator
                for a ServiceObjectType.

            schema (optional, graphql.core.type.GraphQLSchema): The GraphQL schema
                which acts as a basis for the external API. If None, no endpoints are
                added to the service.

        Example:

            .. code-block:: python

                from nautilus import Service
                from nautilus.api import create_model_schema
                from nautilus.network import CRUDHandler
                from nautilus.models import BaseModel


                class Model(BaseModel):
                    name = Column(Text)


                # you could also make your own
                api_schema = create_model_schema(Model)
                action_handler = CRUDHandler(Model)


                service = Service(
                    name = 'My Awesome Service',
                    schema = api_schema,
                    actionHandler = action_handler
                )
    """

    def __init__(
            self,
            name,
            schema = None,
            actionHandler = None,
            configObject = None,
            auto_register = True,
            auth = True,
    ):
        # base the service on a flask app
        self.app = Flask(__name__)

        self.name = name
        self.__name__ = name
        self.auto_register = auto_register
        self.auth = auth

        # apply any necessary flask app config
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

        # if there is a configObject
        if configObject:
            # apply the config object to the flask app
            self.app.config.from_object(configObject)

        # if there is an action consumer, create a wrapper for it
        self.actionConsumer = ActionConsumer(actionHandler = actionHandler) if actionHandler else None

        from nautilus.db import db
        db.init_app(self.app)

        # setup various functionalities
        self.setupAdmin()
        self.setupAuth()
        self.setupApi(schema)


    def run(self, host='127.0.0.1', port = 8000, debug = False, secretKey = 'supersecret', **kwargs):

        # save command line arguments
        self.app.config['DEBUG'] = kwargs['debug'] if 'debug' in kwargs \
                                                    else debug
        self.app.config['HOST'] = kwargs['host'] if 'host' in kwargs \
                                                    else host
        self.app.config['PORT'] = kwargs['port'] if 'port' in kwargs \
                                                    else port
        self.app.config['SECRET_KEY'] = kwargs['secretKey'] if 'secretKey' in kwargs \
                                                            else secretKey

        # if the service needs to register itself
        if self.auto_register:
            # register with the service registry
            registry.keep_alive(self)

        # if we need to spin up an action consumer
        if self.actionConsumer:
            # create a thread that will run the consumer
            actionThread = threading.Thread(target = self.actionConsumer.run)
            # start the thread
            actionThread.start()

        # run the service at the designated port
        self.app.run(host=self.app.config['HOST'], port = self.app.config['PORT'])


    def stop(self):
        # if there is an action consumer
        if self.actionConsumer:
            # stop the consumer
            self.actionConsumer.stop()

        # if the service is responsible for registering itself
        if self.auto_register:
            # remove the service from the registry
            registry.deregister_service(self)

    def use_blueprint(self, blueprint):
        """ Apply a flask blueprint to the internal application """
        self.app.register_blueprint(blueprint)

    def setupAuth(self):
        # if we are supposed to enable authentication for the service
        if self.auth:
            from nautilus.auth import init_service
            init_service(self)


    def setupAdmin(self):
        from nautilus.admin import init_service
        init_service(self)


    def setupApi(self, schema = None):
        # if there is a schema for the service
        if schema:
            # configure the service api with the schema
            from nautilus.api import init_service
            init_service(self, schema=schema)


    def route(self, **options):
        """
            A wrapper over Flask's @app.route(**options).
        """

        return self.app.route(**options)

