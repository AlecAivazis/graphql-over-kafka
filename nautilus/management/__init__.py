#! /usr/bin/env python3

# external imports
import click
# local imports
from .scripts import create, publish

@click.group()
def cli():
    """
        A collection of functions for managing nautilus clouds.
    """
    pass

# add the various sub commands to the manager
cli.add_command(create)
cli.add_command(publish)
