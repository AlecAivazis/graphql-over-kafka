# external imports
import threading
import time
import random
import consul
import tornado

# create a consul session
consul_session = consul.Consul()

def register_service(service):
    ''' Add a service to the registry service. '''

    # local imports
    from nautilus.auth import random_string

    # compute and save the consul identifier for the service
    service.consul_name = "{}-{}".format(service.name, random_string(6))\
                                 .replace('_', '-')

    # the consul service entry
    consul_session.agent.service.register(
        name=service.name,
        service_id=service.consul_name,
        # port=service.app.config['PORT'],
        port=service.config.port
    )


def deregister_service(service):
    ''' Remove a service from the registery. '''
    # if the service has been registered
    if hasattr(service, 'consul_name'):
        # deregister it
        consul_session.agent.service.deregister(service.consul_name)
        consul_session.agent.check.deregister(service.consul_name)


def get_services():
    ''' Return a list of the active services. '''
    return consul_session.agent.services()


def service_location_by_name(key):
    ''' Return the service entry matching the given key '''
    # grab the registry of services
    # todo: go through service proxy service for more efficient loadbalancing
    services = ["localhost:{}".format(service['Port']) \
                                for service in get_services().values() \
                                                if service['Service'] == key]
    # return a random entry from the possibilities
    return random.choice(services)


def keep_alive(service):
    ''' Ping the registry on an interval to show good health. '''

    # the default ttl is 10 sec
    ttl = service.ttl if hasattr(service, 'ttl') else 10

    # register the service with consul
    register_service(service)
    # add a ttl check for the service in case we die
    consul_session.agent.check.register(
        name=service.consul_name,
        check=consul.Check.ttl(str(ttl) + 's'),
    )

    def pass_ttl():
        # tell the agent that we are passing the ttl check
        consul_session.agent.check.ttl_pass(service.consul_name, 'Agent alive and reachable.')

    # the interval to perform the check (in millisecons)
    interval = 2000

    # create a period callback that will perform the check every {t} seconds
    periodic_callback = tornado.ioloop.PeriodicCallback(pass_ttl, callback_time=interval)

    return periodic_callback
