"""
    This module defines the various create scripts availible to the cloud
    manager
"""
# external imports
import click
# local imports
from ..util import render_template


@click.group()
def create():
    """ A set of generators for common files and directory strctures. """
    pass

@click.command()
def model():
    """
        Creates the example directory structure necessary for a model service.
    """
    render_template(template='model')

@click.command()
def connection():
    """
        Creates the example directory structure necessary for a connection
        service.
    """
    render_template(template='connection')

# add the various sub commands
create.add_command(model)
create.add_command(connection)
