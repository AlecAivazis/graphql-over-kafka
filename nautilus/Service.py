# third party imports
import threading
from flask import Flask
from flask_graphql import GraphQLView, GraphQL
from flask_login import LoginManager
# local imports
from .network.messaging.consumers import ActionConsumer
from .ext import db

class Service:

    name = 'Nautilus Service'

    def __init__(self, schema = None, actionHandler = None):
        # base the service on a flask app
        self.app = Flask(__name__)
        # if there is an action consumer, create a wrapper for it
        self.actionConsumer = ActionConsumer(actionHandler = actionHandler) if actionHandler else None
        # setup various functionalities
        db.init_app(self.app)
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

