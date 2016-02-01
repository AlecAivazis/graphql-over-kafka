"""
    This module manages the commands of the manage file.
"""

from flask.ext.script import Manager

class ServiceManager:

    def __init__(self, service):
        # create and attach a command manager for the service
        self.commandManager = Manager(service.app)

        @self.commandManager.command
        def syncdb():
            """ Create the database entries. """
            # import the db module
            from nautilus.ext import db
            # create all of the tables
            db.create_all()
            # notify the user
            print("Successfully created database entries.")

        @self.commandManager.command
        def runserver(port = 8000, debug = False, secretKey = 'supersecret'):
            """ Start the service. """
            service.run(int(port), debug, secretKey)

    def run(self):
        """ run the command manager """
        self.commandManager.run()
