#! /usr/bin/env python3

# third party imports
from nautilus import ServiceManager
# local imports
from server import {{name.title()}}Service

# create a manager wrapping the service
manager = ServiceManager({{name.title()}}Service)

if __name__ == '__main__':
    manager.run()
