import io
import numpy as np
import pika
import werkzeug
from PIL import Image


class RabbitMQService:
    def __init__(self, estimator):
        self.__estimator = estimator

    def run(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='rabbitmq', port='5672', virtual_host='/',
                credentials=pika.PlainCredentials(username='user', password='password')
            )
        )

        channel = connection.channel()

        channel.queue_declare(queue='estimation')

        def on_request(ch, method, props, body):
            _, form, files = werkzeug.formparser.parse_form_data({
                'wsgi.input': io.BufferedReader(io.BytesIO(body)),
                'CONTENT_LENGTH': str(len(body)),
                'CONTENT_TYPE': props.content_type,
                'REQUEST_METHOD': 'POST'
            }, silent=False)


            hours = int(form.get('hours'))
            minutes = int(form.get('minutes'))
            try:
                response = self.__estimator.estimate(
                    image=np.array(Image.open(io.BytesIO(files.get('file').read()))),
                    time=(hours, minutes)
                )
            except Exception as e:
                response = "Failed to process image"
                print(e, flush=True)

            ch.basic_publish(exchange='',
                             routing_key=props.reply_to,
                             properties=pika.BasicProperties(correlation_id=props.correlation_id),
                             body=str(response))
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='estimation', on_message_callback=on_request)

        channel.start_consuming()
