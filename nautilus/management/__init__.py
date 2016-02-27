#! /usr/bin/env python3

# external imports
import click
# local imports
from .scripts.create import create

@click.group()
def cloud_manager():
    """
        A collection of functions for managing nautilus clouds.
    """
    pass

# add the various sub commands to the manager
cloud_manager.add_command(create)
