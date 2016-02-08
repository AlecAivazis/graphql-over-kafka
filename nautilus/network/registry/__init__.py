# external imports
import consul
import threading
import time
import random
from consul import Check
# local imports
from nautilus.auth import random_string

# create a consul session
consulSession = consul.Consul()

def register_service(service):
    ''' Add a service to the registry service. '''
    # the consul service entry
    consulSession.agent.service.register(
        name = service.name,
        service_id = "{}-{}".format(service.name, random_string(6)),
        port = service.app.config['PORT'],
    )


def deregister_service(service):
    ''' Remove a service from the registery. '''
    consulSession.agent.service.deregister(service.name)


def get_services():
    ''' Return a list of the active services. '''
    return consulSession.agent.services()


def service_location_by_name(key):
    ''' Return the service entry matching the given key '''
    # grab the registry of services
    # todo: go through nginx reverse proxy (service proxy service)
    services = ["localhost:{}".format(service['Port']) for service in get_services().values() \
                                                    if service['Service'] == key ]
    # return a random entry from the possibilities
    return random.choice(services)


def keep_alive(service):
    ''' Ping the registry on an interval to show good health. '''

    # the default tt is 10 sec
    ttl = service.ttl if hasattr(service, 'ttl') else 10

    # register the service with consul
    register_service(service)
    # add a ttl check for the service in case we die
    consulSession.agent.check.register(
        name = service.name,
        check = Check.ttl(str(ttl) + 's'),
    )

    # the keep alive check
    def run_check():
        # continuously run
        while True:
            # sleep every 2 seconds
            time.sleep(2)
            # tell the agent that we are passing the ttl check
            consulSession.agent.check.ttl_pass(service.name, 'Agent alive and reachable.')

    # create a thread that will run the consumer
    thread = threading.Thread(target=run_check)
    # start the thread
    thread.start()
