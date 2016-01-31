"""
    This module manages the commands made availible when the command file is ran.
"""


from flask.ext.script import Manager

class ServiceManager:

    def __init__(self, service):
        # create and attach a command manager for the service
        self.commandManager = Manager(service.app)

        @self.commandManager.command
        def createdb():
            """ Create the database entries. """
            # import the db module
            from nautilus.ext import db
            # create all of the tables
            db.create_all()
            # notify the user
            print("Successfully created database entries.")


    def run(self):
        """ run the command manager """
        self.commandManager.run()
