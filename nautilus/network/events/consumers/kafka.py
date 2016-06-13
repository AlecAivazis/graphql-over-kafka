# external imports
import asyncio
import uuid
import json
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from kafka.common import KafkaError
# local imports


class KafkaBroker:
    """
        This class handles two way communication with the kafka
        server. Also allows for a question/answer interface served
        over the kafka stream.
    """
    loop = None
    server = None
    consumer_channel = None
    producer_channel = None


    def __init__(self):
        # a dictionary to keep the question/answer correlation ids
        self._request_handlers = {}

        # a placeholder for the event consumer task
        self._consumer_task = None
        # create a consumer instance
        self._consumer = AIOKafkaConsumer(self.consumer_channel, loop=self.loop, bootstrap_servers=self.server)
        self._producer = AIOKafkaProducer(loop=self.loop, bootstrap_servers=self.server)


    def start(self):
        """
            This function starts the brokers interaction with the kafka stream
        """
        self.loop.run_until_complete(self._consumer.start())
        self.loop.run_until_complete(self._producer.start())
        self._consumer_task = self.loop.create_task(self._consume_event_callback())


    def stop(self):
        """
            This method stops the brokers interaction with the kafka stream
        """
        self.loop.run_until_complete(self._consumer.stop())
        self.loop.run_until_complete(self._producer.stop())
        self._consumer_task.cancel()


    async def send(self, message, channel=None, *args, **kwds):
        """
            This method sends a message over the kafka stream.
        """
        # use a custom channel if one was provided
        channel = channel or self.producer_channel

        # send the message
        return await self._producer.send(channel, message, *args, **kwds)


    async def getone(self, *args, **kwds):
        """
            This method waits for a single method over the
        """
        return await self._consumer.getone(*args, **kwds)


    async def ask(self, message, **kwds):
        # create a correlation id for the question
        correlation_id = uuid.uuid4()
        # make sure its unique
        while correlation_id in self._request_handlers:
            # create a new correlation id
            correlation_id = uuid.uuid4()
        # use the integer form of the uuid
        correlation_id = correlation_id.int

        # create a future to wait on before we ask the question
        question_future = asyncio.Future()
        # register the future's callback with the request handler
        self._request_handlers[correlation_id] = question_future.set_result

        # the question dictionary
        question = {
            'correlation_id': correlation_id,
            'body': message
        }

        # publish the question
        await self.send(json.dumps(question).encode(), **kwds)

        print('asking %s' % correlation_id)

        # return the response
        return await question_future


    ## internal implementations


    async def handle_message(self, msg, props):
        raise NotImplementedError()


    async def _consume_event_callback(self):
        # continuously loop
        while True:
            try:

                # grab the next message
                msg = await self.getone()

                # parse the message as json
                message = json.loads(msg.value.decode())
                # the correlation_id associated with this message
                correlation_id = message.get('correlation_id')
                # the body of the message
                body = message['body']

                # if we know how to respond to this message
                if correlation_id and correlation_id in self._request_handlers:
                    # pass the body to the handler
                    self._request_handlers[correlation_id](body)
                    print('handled %s' % correlation_id)

                # otherwise there was no correlation id, pass it along to the general handlers
                else:
                    # build the dictionary of message properties
                    message_props = {
                        'correlation_id': correlation_id
                    }
                    # pass it to the handler
                    await self.handle_message(body, message_props)

            # if something goes wrong
            except KafkaError as err:
                print("error while consuming message: ", err)


