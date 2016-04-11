from .amqp import AMQPConsumer


class ActionHandler(AMQPConsumer):
    EXCHANGE = 'my_events'
    EXCHANGE_TYPE = 'topic'
    ROUTING_KEY = '*.*.pending'
    DURABLE = True

    def __init__(self, callback, routing_key=None, **kwds):
        # save a reference to the callback we were provided
        self.handle_event = callback
        self.ROUTING_KEY = routing_key or self.ROUTING_KEY
        super().__init__(**kwds)
