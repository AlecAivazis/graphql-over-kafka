# external imports
import consul
import threading
import time
from consul import Check
# local imports
from ..util import get_ip_address

# create a consul session
consulSession = consul.Consul()

def register_service(service):
    # the consul service entry
    consulSession.agent.service.register(
        name = service.name,
        service_id = service.name,
        port = service.app.config['PORT'],
        address = get_ip_address(),
    )

def deregister_service(service):
    consulSession.agent.service.deregister(service.name)


def keep_alive(service):

    ttl = service.ttl if hasattr(service, 'ttl') else 10

    consulSession.agent.check.register(
        name = service.name,
        check = Check.ttl(str(ttl) + 's'),
    )

    def run_check():
        register_service(service)
        while True:
            time.sleep(2)
            consulSession.agent.check.ttl_pass(service.name, 'Agent alive and reachable.')


    # create a thread that will run the consumer
    thread = threading.Thread(target=run_check)
    # register the
    # start the thread
    thread.start()
