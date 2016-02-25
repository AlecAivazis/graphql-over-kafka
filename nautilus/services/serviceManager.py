"""
    This module defines a small singleton that runs various scripts in the
    context of the service.
"""

# external imports
from flask.ext.script import Manager
import threading

class ServiceManager:

    def __init__(self, service):
        # create and attach a command manager for the service
        self.commandManager = Manager(service.app)
        self.service = service

        @self.commandManager.command
        def syncdb():
            """ Create the database entries. """
            # import the db module
            from nautilus.db import db
            # create all of the tables
            db.create_all()
            # notify the user
            print("Successfully created database entries.")

        @self.commandManager.command
        def runserver(host = '127.0.0.1', port = 8000, debug = False, secretKey = 'supersecret'):
            """ Start the service. """
            service.run(host = host, port = int(port), debug = debug, secretKey = secretKey)


    def run(self):
        """ run the command manager """
        try:
            self.commandManager.run()
        except Exception as err:
            print(err)
            self.service.stop()
