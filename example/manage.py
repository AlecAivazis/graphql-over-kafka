#! /usr/bin/python3

# third party imports
from nautilus import ServiceManager
# local imports
from server import service

# create a manager which provides the command line interface to manage the service
# for example: ./manage.py runserver --port 8000 --debug
manager = ServiceManager(service)

if __name__ == '__main__':
    manager.run()
