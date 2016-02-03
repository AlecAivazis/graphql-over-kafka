#! /usr/bin/python3

# third party imports
from nautilus import ServiceManager
# local imports
from server import service

# create a manager wrapping the service which provides the command line interface for a particular service
manager = ServiceManager(service)

if __name__ == '__main__':
    manager.run()
