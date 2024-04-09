import asyncio
from functools import partial
import aio_pika
import importlib
from PIL import Image
import io
import json

estimationModule = importlib.import_module("processing.Estimator")

class RabbitmMQService:
    def __init__(self, estimator: any):
        self.__estimator = estimator

    async def consumer(
        self, msg: aio_pika.IncomingMessage,
        channel: aio_pika.RobustChannel
    ):
        async with msg.process():
            image_data = msg.body
            image = Image.open(io.BytesIO(image_data))
            
            result = self.__estimator.estimate(image)
            
            response = json.dumps({"result": result})
            
            if msg.reply_to:
                await channel.default_exchange.publish(
                    message=aio_pika.Message(
                        body=response.encode(),
                        correlation_id=msg.correlation_id,
                    ),
                    routing_key=msg.reply_to,
                )

async def main():
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/"
    )

    queue_name = "estimation"

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name)
        
        service = RabbitmMQService(estimationModule)  
        await queue.consume(partial(service.consumer, channel=channel))  

        try:
            await asyncio.Future()
        except Exception:
            pass

if __name__ == '__main__':
    asyncio.run(main())
