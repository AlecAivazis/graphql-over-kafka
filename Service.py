# third party imports
import argparse
from flask import Flask
from flask_graphql import GraphQLView, GraphQL
from flask_login import LoginManager
# local imports
from nautilus.network.messaging.consumers import ActionConsumer

class Service:

    def __init__(self, schema, actionHandler = None):
        # instantiate a flask server
        self.app = Flask(__name__)
        self.actionHandler = actionHandler
        self.schema = schema

        # argument definitions
        parser = argparse.ArgumentParser(description='Run the api server.')
        parser.add_argument('--port', type=int, nargs='?', default=8000,
                            help='The port for the application server' )
        parser.add_argument('--debug', action='store_true',
                            help='Wether or not to run in debug mode')

        # parse the args and save it in the app config
        args = parser.parse_args()
        # save command line arguments
        self.app.config['DEBUG'] = args.debug
        self.app.config['PORT'] = args.port

        self.setupAuth()
        self.setupApi()

        # create an action consumer that calls the handler
        self.actionConsumer = ActionConsumer(actionHandler = actionHandler) if actionHandler else None


    def run(self):
        # if we need to spin up an action consumer
        if self.actionConsumer:
            # start the consumer
            self.actionConsumer.run()

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


    def setupApi(self):
        from .api import setupApi
        setupApi(self, schema=self.schema)
