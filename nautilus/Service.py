# third party imports
import threading
from flask import Flask
from flask_graphql import GraphQLView, GraphQL
from flask_login import LoginManager
# local imports
from .network.messaging.consumers import ActionConsumer

class Service:

    name = 'Nautilus Service'

    def __init__(self, schema = None, actionHandler = None, configObject = None):
        # base the service on a flask app
        self.app = Flask(__name__)

        # apply any necessary flask app config
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        # if there is a configObject
        if configObject:
            # apply the config object to the flask app
            self.app.config.from_object(configObject)

        # if there is an action consumer, create a wrapper for it
        self.actionConsumer = ActionConsumer(actionHandler = actionHandler) if actionHandler else None

        from .ext import db
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

        # if we need to spin up an action consumer
        if self.actionConsumer:
            # create a thread that will run the consumer
            actionThread = threading.Thread(target=self.actionConsumer.run)
            # start the thread
            actionThread.start()

        #run the service at the designated port
        self.app.run(port = self.app.config['PORT'])


    def stop(self):
        # if there is an action consumer
        if self.actionConsumer:
            # stop the consumer
            self.actionConsumer.stop()


    def setupAuth(self):
        from .auth import init_service
        init_service(self)


    def setupAdmin(self):
        from .ext.admin import init_service
        init_service(self)


    def setupApi(self, schema = None):
        # if there is a schema for the service
        if schema:
            # configure the service api with the schema
            from .ext.api import init_service
            init_service(self, schema=schema)


    def addModelToAdmin(self, model):
        from nautilus.ext.admin import add_model
        add_model(model)

