from fetcher.fetch_comments import monitor_channel_comments
from consumer.consumer import start_consumer
import threading
import time
from config.settings import CHANNEL_ID

def fetch_and_send_comments(channel_id, stop_event):
    while not stop_event.is_set():
        monitor_channel_comments(channel_id)
        time.sleep(10)

def consumer_thread(stop_event):
    while not stop_event.is_set():
        start_consumer()
        time.sleep(10) 

if __name__ == '__main__':
    channel_id = CHANNEL_ID  # Replace with your actual video ID
    stop_event = threading.Event()

    # Start threads
    fetch_thread = threading.Thread(target=fetch_and_send_comments, args=(channel_id, stop_event))
    consumer_thread = threading.Thread(target=consumer_thread, args=(stop_event,))
    
    fetch_thread.start()
    consumer_thread.start()

    # Wait for 3 hours then stop
    time.sleep(3 * 3600)  # 3 hours in seconds
    stop_event.set()  # Signal all threads to stop

    # Optionally join threads
    fetch_thread.join()
    consumer_thread.join()

    print("All processes have been stopped.")

