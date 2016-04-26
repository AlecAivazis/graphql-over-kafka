#! /usr/bin/env python3

# external imports
import click
# local imports
from .scripts.create import create

@click.group()
def cli():
    """
        A collection of functions for managing nautilus clouds.
    """
    pass

# add the various sub commands to the manager
cli.add_command(create)
