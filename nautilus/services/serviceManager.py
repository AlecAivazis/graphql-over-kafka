"""
    This module defines a small singleton that runs various scripts in the
    context of the service.
"""

# external imports
import click
# local imports
from ..config import Config

class ServiceManager:

    def __init__(self, service, config=None):
        self.service = service
        self.service_config = Config(config)

        @click.group()
        def group():
            pass

        @group.command(help="Run the service.")
        @click.option('--port', default=8000, help="The port for the service http server.")
        @click.option('--host', default='127.0.0.1', help="The host for the http server.")
        @click.option('--debug', default=False, is_flag=True, help="Run the service in debug mode.")
        def runserver(port, host, debug):
            # the service configuration based on cli args
            self.service_config.update(dict(
                debug=debug
            ))

            # initialize the service with the config
            self.service_instance = self.service(config=self.service_config)

            # run the service
            self.service_instance.run(
                host=host,
                port=int(port),
            )


        @group.command(help="Make sure the models have been written to the db.")
        def syncdb():
            """ Create the database entries. """
            # instantiate the service before we do anything
            service = self.service()
            # get the models managed by the service
            models = getattr(service, 'get_models', lambda: [])()

            # if there are models to create
            if models:
                # for each model that we are managing
                for model in models:
                    # create the table in the database
                    model.create_table(True)

                # notify the user
                print("Successfully created necessary database tables.")

            # otherwise there are no tables to create
            else:
                print("There are no models to add.")


        @group.command(help="Drop the database tables associated with this service.")
        def cleardb():
            """ Drop the tables associated with this service. """
            # instantiate the service before we do anything
            service = self.service()
            # get the models managed by the service
            models = getattr(service, 'get_models', lambda: [])()

            # if there are models to create
            if models:
                # for each model that we are managing
                for model in models:
                    # create the table in the database
                    model.drop_table(True)

                # notify the user
                print("Successfully dropped necessary database tables.")

            # otherwise there are no tables to create
            else:
                print("There are no models to drop.")


        # save the command group to the manager
        self.group = group

    def run(self):
        """ run the command manager """
        try:
            # run the command group
            self.group()
        # if there is a normal exception
        except Exception as err:
            print("Closing due to error: %s" % err)
            # bubble up the exception for someone else
            raise err
