# external imports
import consul
import threading
from consul import Check

# create a consul session
consulSession = consul.Consul()

def register_service(service):
    # the consul service entry
    consulSession.agent.service.register(
        name = service.name,
        service_id = service.name,
        port = service.app.config['PORT'],
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
            consulSession.agent.check.ttl_pass(service.name)


    # create a thread that will run the consumer
    thread = threading.Thread(target=run_check)
    # register the
    # start the thread
    thread.start()
