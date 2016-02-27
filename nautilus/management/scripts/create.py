"""
    This module defines the various create scripts availible to the cloud
    manager
"""
# external imports
import click
import sys
# local imports
from ..util import render_template


@click.group()
def create():
    """ A set of generators for common files and directory strctures. """
    pass

@click.command()
@click.argument('model_names', nargs=-1)
def model(model_names):
    """
        Creates the example directory structure necessary for a model service.
    """
    # for each model name we need to create
    for model_name in model_names:
        # render the model template
        render_template(template='model', context={
            'name': model_name
        })

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
