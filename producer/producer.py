import pika
import json
from config.settings import RABBITMQ_URL, QUEUE_NAME

def send_to_queue(message):
    """
    Sends a message to a RabbitMQ queue.

    Args:
        message (Any): The message to be sent to the queue.

    Returns:
        None

    Raises:
        pika.exceptions.AMQPConnectionError: If there is an error connecting to the RabbitMQ server.
        pika.exceptions.AMQPChannelError: If there is an error creating a channel or declaring a queue.
        pika.exceptions.AMQPError: If there is an error publishing the message.

    This function establishes a connection to a RabbitMQ server using the provided URL, creates a channel, declares a queue with the specified name, and publishes the message to the queue. The connection is closed afterwards.

    Note:
        - The `RABBITMQ_URL` and `QUEUE_NAME` variables must be defined in the `config.settings` module.
        - The message is serialized to JSON before being sent to the queue.

    Example:
        ```python
        message = {"key": "value"}
        send_to_queue(message)
        ```
    """
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=json.dumps(message))
    connection.close()
