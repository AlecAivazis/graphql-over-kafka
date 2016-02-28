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
@click.argument('model_names', nargs=-1)
def model(model_names):
    """
        Creates the example directory structure necessary for a model service.
    """
    # for each model name we need to create
    for model_name in model_names:
        # the template context
        context = {
            'name': model_name,
        }

        # render the model template
        render_template(template='common', context=context)
        render_template(template='model', context=context)

@click.command()
def api():
    """
        Create the folder/directories for an ApiGateway service.
    """
    # the template context
    context = {
        'name': 'api',
    }

    render_template(template='common', context=context)
    render_template(template='api', context=context)

@click.command()
@click.argument('model_connections', nargs=-1)
def connection(model_connections):
    """
        Creates the example directory structure necessary for a connection
        service.
    """

    # for each connection group
    for connection_str in model_connections:

        # the services to connect
        services = connection_str.split(':')
        services.sort()

        service_name = ''.join([service.title() for service in services])

        # the template context
        context = {
            # make sure the first letter is lowercase
            'name': service_name[0].lower() + service_name[1:],
            'services': services,
        }

        render_template(template='common', context=context)
        render_template(template='connection', context=context)

# add the various sub commands
create.add_command(api)
create.add_command(connection)
create.add_command(model)
