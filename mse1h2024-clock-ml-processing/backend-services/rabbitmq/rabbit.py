import asyncio
from functools import partial
import aio_pika

class RabbitmMQService:
    def __init__(self):
        self.__estimator = None

    async def consumer(
            self, msg: aio_pika.IncomingMessage,
            channel: aio_pika.RobustChannel
    ):
        async with msg.process():
            print(msg.body)

            if msg.reply_to:
                await channel.default_exchange.publish(
                    message=aio_pika.Message(
                        body="10",
                        correlation_id=msg.correlation_id,
                    ),
                    routing_key=msg.reply_to,
                )

    async def run(self):
        print("Starting RabbitMQ service")
        try:
            connection = await aio_pika.connect_robust(
                "amqp://user:password@rabbitmq:5672/"
            )

            queue_name = "estimation"

            async with connection:
                channel = await connection.channel()
                queue = await channel.declare_queue(queue_name)

                await queue.consume(partial(self.consumer, channel=channel))

                # Run indefinitely
                await asyncio.Future()
        except aio_pika.exceptions.AMQPConnectionError as e:
            print(f"Failed to connect to RabbitMQ server: {e}")
