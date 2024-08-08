from fetcher.fetch_comments import monitor_channel_comments
from consumer.consumer import start_consumer
import threading
from config.settings import CHANNEL_ID

def fetch_and_send_comments(channel_id):
    monitor_channel_comments(channel_id)

if __name__ == '__main__':
    channel_id = CHANNEL_ID  # Replace with your actual video ID
    threading.Thread(target=fetch_and_send_comments, args=(channel_id,)).start()
    threading.Thread(target=start_consumer).start()

