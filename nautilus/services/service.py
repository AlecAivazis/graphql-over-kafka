# external imports
import os
import requests
import tornado.ioloop
import tornado.web
# local imports
from nautilus.network.amqp.consumers.actions import ActionHandler
from nautilus.network.http import GraphqlRequestHandler

class Service:
    """
        This is the base class for all services that are part of a nautilus
        cloud. This class provides basic functionalities such as registration,
        responding to actions, and predictable api endpoints.

        Args:

            action_handler (optional, function): The callback function fired when
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


                api_schema = create_model_schema(Model)


                action_handler = CRUDHandler(Model)


                service = Service(
                    name = 'My Awesome Service',
                    schema = api_schema,
                    action_handler = action_handler
                )
    """

    def __init__(
            self,
            name,
            schema=None,
            action_handler=None,
            configObject=None,
            auto_register=True,
            auth=True,
    ):
        # base the service on a flask app
        self.app = self.tornado_app(schema)

        self.name = name
        self.__name__ = name
        self.action_consumer = None

        # apply any necessary flask app config
        # self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

        # if there is a configObject
        # if configObject:
        #     # apply the config object to the flask app
        #     self.app.config.from_object(configObject)

        # setup various functionalities
        self.init_action_handler(action_handler)
        # self.setup_db()
        # self.setup_admin()
        # self.setup_auth()


    def tornado_app(self, schema):

        # create a tornado web application
        app = tornado.web.Application([
            (r"/", GraphqlRequestHandler, schema),
        ])

        # attach the ioloop to the application
        app.ioloop = tornado.ioloop.IOLoop.instance()

        return app


    def init_action_handler(self, action_handler):
        # if the service was provided an action handler
        if action_handler:
            # create a wrapper for it
            self.action_consumer = ActionHandler(callback=action_handler)
            # add it to the ioloop
            self.app.ioloop.add_callback(self.action_consumer.run)


    def run(self, port=8000, **kwargs):
        # assign the port to the app instance
        self.app.listen(port)
        # start the ioloop
        self.app.ioloop.start()


    def stop(self):
        # stop the ioloop
        self.app.ioloop.stop()


    # def setup_db(self):
    #     # import the nautilus db configuration
    #     from nautilus.db import db
    #     # initialize the service app
    #     db.init_app(self.app)


    # def setup_auth(self):
    #     # if we are supposed to enable authentication for the service
    #     if self.auth:
    #         from nautilus.auth import init_service
    #         init_service(self)


    # def setup_admin(self):
    #     from nautilus.admin import init_service
    #     init_service(self)

