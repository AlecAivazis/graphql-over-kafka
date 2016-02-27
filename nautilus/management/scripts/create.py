"""
    This module defines the various create scripts availible to the cloud
    manager
"""
# external imports
import click

@click.group()
def create():
    """ A set of generators for common files and directory strctures. """
    pass

@click.command()
def model():
    """
        Creates the example directory structure necessary for a model service.
    """
    print('creating model')

@click.command()
def connection():
    """
        Creates the example directory structure necessary for a connection
        service.
    """
    print('creating connection')

# add the various sub commands
create.add_command(model)
create.add_command(connection)
