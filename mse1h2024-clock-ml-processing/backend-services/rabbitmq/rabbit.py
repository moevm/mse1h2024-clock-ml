import pika


class RabbitmMQService:
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
            response = 10

            ch.basic_publish(exchange='',
                             routing_key=props.reply_to,
                             properties=pika.BasicProperties(correlation_id=props.correlation_id),
                             body=str(response))
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='estimation', on_message_callback=on_request)

        channel.start_consuming()