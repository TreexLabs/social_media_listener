import pika
import json
from config.settings import RABBITMQ_URL, QUEUE_NAME
from utils.file_writer import write_to_excel

def callback(ch, method, properties, body):
    message = json.loads(body)
    write_to_excel(message)

def start_consumer():
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

