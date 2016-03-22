# external imports
import consul
import threading
import time
import random
from consul import Check

# create a consul session
consulSession = consul.Consul()

def register_service(service):
    ''' Add a service to the registry service. '''

    # local imports
    from nautilus.auth import random_string

    # compute and save the consul identifier for the service
    service.consul_name = "{}-{}".format(service.name, random_string(6))\
                                 .replace('_', '-')

    # the consul service entry
    consulSession.agent.service.register(
        name=service.name,
        service_id=service.consul_name,
        port=service.app.config['PORT'],
    )


def deregister_service(service):
    ''' Remove a service from the registery. '''
    # if the service has been registered
    if hasattr(service, 'consul_name'):
        # deregister it
        consulSession.agent.service.deregister(service.consul_name)
        consulSession.agent.check.deregister(service.consul_name)


def get_services():
    ''' Return a list of the active services. '''
    return consulSession.agent.services()


def service_location_by_name(key):
    ''' Return the service entry matching the given key '''
    # grab the registry of services
    # todo: go through service proxy service for more efficient loadbalancing
    services = ["localhost:{}".format(service['Port']) for service in get_services().values() \
                                                    if service['Service'] == key ]
    # return a random entry from the possibilities
    return random.choice(services)


def keep_alive(service):
    ''' Ping the registry on an interval to show good health. '''

    # the default ttl is 10 sec
    ttl = service.ttl if hasattr(service, 'ttl') else 10

    # register the service with consul
    register_service(service)
    # add a ttl check for the service in case we die
    consulSession.agent.check.register(
        name = service.consul_name,
        check = Check.ttl(str(ttl) + 's'),
    )

    # the keep alive check
    def run_check():
        # continuously run
        while True:
            # sleep every 2 seconds
            time.sleep(2)
            # tell the agent that we are passing the ttl check
            consulSession.agent.check.ttl_pass(service.consul_name, 'Agent alive and reachable.')

    # create a thread that will run the consumer
    thread = threading.Thread(target=run_check)
    # start the thread
    thread.start()
