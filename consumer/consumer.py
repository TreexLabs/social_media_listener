import pika
import json
from config.settings import RABBITMQ_URL, QUEUE_NAME
from utils.file_writer import write_to_excel
import time

def callback(ch, method, properties, body):
    """
    Parses the JSON message from the body, and writes the parsed message to an Excel file.

    Parameters:
    ch (parameter type): Description of the parameter.
    method (parameter type): Description of the parameter.
    properties (parameter type): Description of the parameter.
    body (parameter type): Description of the parameter.

    Returns:
    None
    """
    message = json.loads(body)
    write_to_excel(message)

def start_consumer():
    """
    Establishes a connection to a RabbitMQ server and starts consuming messages from a specified queue.

    This function creates a connection to a RabbitMQ server using the provided URL. It then declares a queue
    with the specified name and starts consuming messages from that queue. The `on_message_callback` parameter
    specifies the function to be called when a message is received. The `auto_ack` parameter determines
    whether the message is automatically acknowledged by the consumer.

    Parameters:
        None

    Returns:
        None
    """
    while True:
        try:
            connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
            channel = connection.channel()
            channel.queue_declare(queue=QUEUE_NAME)
            channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
            print('Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(30)

