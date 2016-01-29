# third party imports
import argparse
from flask import Flask
from flask_graphql import GraphQLView, GraphQL
from flask_login import LoginManager
# local imports

class Service:

    def __init__(self, schema, actionHandler):
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


    def run(self):
        self.app.run(port = self.app.config['PORT'])


    def setupAuth(self):
        from .auth import setupAuth
        setupAuth(self)


    def setupApi(self):
        from .api import setupApi
        setupApi(self, schema=self.schema)
