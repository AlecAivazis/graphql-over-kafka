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

    def __init__(
            self,
            schema = None,
            actionHandler = None,
            configObject = None,
            name = 'Nautilus Service',
            auto_register = True,
    ):
        # base the service on a flask app
        self.app = Flask(__name__)

        self.name = name
        self.__name__ = name
        self.auto_register = auto_register

        # apply any necessary flask app config
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

        # if there is a configObject
        if configObject:
            # apply the config object to the flask app
            self.app.config.from_object(configObject)

        # if there is an action consumer, create a wrapper for it
        self.actionConsumer = ActionConsumer(actionHandler = actionHandler) if actionHandler else None

        from nautilus import db
        db.init_app(self.app)

        # setup various functionalities
        self.setupAdmin()
        self.setupAuth()
        self.setupApi(schema)


    def run(self, port = 8000, debug = False, secretKey = 'supersecret'):

        # save command line arguments
        self.app.config['DEBUG'] = debug
        self.app.config['PORT'] = port
        self.app.config['SECRET_KEY'] = secretKey

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
        self.app.run(port = self.app.config['PORT'])


    def stop(self):
        # if there is an action consumer
        if self.actionConsumer:
            # stop the consumer
            self.actionConsumer.stop()

        # if the service is responsible for registering itself
        if self.auto_register:
            # remove the service from the registry
            registry.deregister_service(self)


    def setupAuth(self):
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



