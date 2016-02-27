#! /usr/bin/python3

# third party imports
from nautilus import ServiceManager
# local imports
from .server import service

# create a manager wrapping the service
manager = ServiceManager(service)

if __name__ == '__main__':
    manager.run()
