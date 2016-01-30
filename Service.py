# third party imports
import argparse, threading
from flask import Flask
from flask_graphql import GraphQLView, GraphQL
from flask_login import LoginManager
# local imports
from .network.messaging.consumers import ActionConsumer

class Service:

    def __init__(self, schema = None, actionHandler = None):

        # argument definitions
        parser = argparse.ArgumentParser(description='Run the api server.')
        parser.add_argument('--port', type=int, nargs='?', default=8000, const=8000,
                            help='The port for the application server' )
        parser.add_argument('--debug', action='store_true',
                            help='Wether or not to run in debug mode')
        parser.add_argument('--secret', nargs='?', default='supersecret', const='supersecret',
                            help='The secret key to use for various crypto bits.')

        # parse the args and save it in the app config
        args = parser.parse_args()

        # instantiate a flask server
        self.app = Flask(__name__)
        self.actionConsumer = ActionConsumer(actionHandler = actionHandler) if actionHandler else None

        # save command line arguments
        self.app.config['DEBUG'] = args.debug
        self.app.config['PORT'] = args.port
        self.app.config['SECRET_KEY'] = args.secret

        self.setupAuth()
        self.setupApi(schema)


    def run(self):

        # if we need to spin up an action consumer
        if self.actionConsumer:
            # create a thread that will run the consumer
            actionThread = threading.Thread(target=self.actionConsumer.run)
            # start the thread
            actionThread.start()

        # run the service at the designated port
        self.app.run(port = self.app.config['PORT'])


    def stop(self):
        # if there is an action consumer
        if self.actionConsumer:
            # stop the consumer
            self.actionConsumer.stop()


    def setupAuth(self):
        from .auth import setupAuth
        setupAuth(self)


    def setupApi(self, schema = None):
        # if there is a schema for the service
        if schema:
            # configure the service api with the schema
            from .api import setupApi
            setupApi(self, schema=schema)
