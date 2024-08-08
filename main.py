from fetcher.fetch_comments import monitor_channel_comments
from producer.producer import send_to_queue
from consumer.consumer import start_consumer
import threading
from config.settings import CHANNEL_ID

def fetch_and_send_comments(channel_id):
    comments = monitor_channel_comments(channel_id)
    for comment in comments:
        send_to_queue(comment)

if __name__ == '__main__':
    channel_id = CHANNEL_ID  # Replace with your actual video ID
    threading.Thread(target=fetch_and_send_comments, args=(channel_id,)).start()
    threading.Thread(target=start_consumer).start()

