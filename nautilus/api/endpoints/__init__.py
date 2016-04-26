# external imports
import os

# local imports
from .requestHandlers.graphiql import GraphiQLRequestHandler
from .requestHandlers.graphql import GraphQLRequestHandler
from .requestHandlers.apiQuery import APIQueryHandler

root_dir = os.path.dirname(__file__)
template_dir = os.path.join(root_dir, 'templates')
static_dir = os.path.join(root_dir, 'static', 'build')
