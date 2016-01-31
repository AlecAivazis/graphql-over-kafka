# third party imports
from flask_graphql import GraphQLView, GraphQL

def init_service(service, schema):
    """ Add GraphQL support to the given Flask app """
    # add default graphql endpoints
    GraphQL(service.app, schema=schema)
    # add the index query per service agreement
    service.app.add_url_rule('/', view_func=GraphQLView.as_view('index', schema=schema))
