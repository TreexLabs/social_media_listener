import pika
import json
from config.settings import RABBITMQ_URL, QUEUE_NAME
from utils.file_writer import write_to_excel
from utils.mongo_writer import write_to_mongo
import time
import threading
import backoff

def callback(ch, method, properties, body, is_write_excel=False):
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
    try:
        message = json.loads(body)
        if is_write_excel:
            write_to_excel(message)
        write_to_mongo(message)
    except Exception as e:
        print(f"Error processing message: {e}")

@backoff.on_exception(backoff.expo, pika.exceptions.AMQPConnectionError, max_time=300)
def connect_to_rabbitmq():
    """Establish a connection to RabbitMQ with retries on failure using exponential backoff."""
    return pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))

def start_consumer(stop_event):
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
    while not stop_event.is_set():
        try:
            connection = connect_to_rabbitmq()
            channel = connection.channel()
            channel.queue_declare(queue=QUEUE_NAME)
            def check_stop_event(ch, method, properties, body):
                if not stop_event.is_set():
                    callback(ch, method, properties, body, True)
                else:
                    channel.stop_consuming()
            channel.basic_consume(queue=QUEUE_NAME, on_message_callback=check_stop_event, auto_ack=True)
            print('Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Connection error occurred: {e}")
            time.sleep(3)
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(3)
        finally:
            if connection.is_open:
                try:
                    connection.close()
                except Exception as e:
                    print(f"Error closing connection: {e}")

# Usage
if __name__ == '__main__':
    stop_event = threading.Event()
    consumer_thread = threading.Thread(target=start_consumer, args=(stop_event,))
    consumer_thread.start()

    # Run the consumer for 3 hours then stop
    time.sleep(3600)
    stop_event.set()
    consumer_thread.join()
    print("Consumer has been stopped.")