from faststream import FastStream
from faststream.rabbit import RabbitMessage, RabbitBroker


class RabbitmMQService:
    def __init__(self):
        self.__estimator = None

    async def run(self):
        print("Starting RabbitMQ service", flush=True)
        try:
            broker = RabbitBroker("amqp://user:password@rabbitmq:5672/")

            @broker.subscriber("estimation")
            async def consumer(msg: RabbitMessage):
                print(msg.body, flush=True)

                if msg.reply_to:
                    await broker.publish(
                        "10",
                        queue=msg.reply_to,
                        correlation_id=msg.correlation_id,
                    )

            app = FastStream(broker)
            await app.run()
        except:
            print(f"Failed to connect to RabbitMQ server", flush=True)
