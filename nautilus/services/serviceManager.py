"""
    This module defines a small singleton that runs various scripts in the
    context of the service.
"""

# external imports
import click

class ServiceManager:

    def __init__(self, service):
        self.service = service
        self._running_service = False

        @click.group()
        def group():
            pass

        @group.command()
        def syncdb():
            print('sync db')

        @group.command(help="Run the service.")
        @click.option('--port', default=8000, help="The port for the service http server.")
        @click.option('--host', default='127.0.0.1', help="The host for the http server.")
        def runserver(port, host):
            # make sure we clean up the service later on
            self._running_service = True
            # run the service
            service.run(
                host = host,
                port = int(port),
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
            # if the service is running
            if self._running_service:
                # stop the service and clean up
                self.service.stop()
            # bubble up the exception for someone else
            raise err
