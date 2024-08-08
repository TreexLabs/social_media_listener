from fetcher.fetch_comments import fetch_comments
from producer.producer import send_to_queue
from consumer.consumer import start_consumer
import threading

def fetch_and_send_comments(video_id):
    comments = fetch_comments(video_id)
    for comment in comments:
        send_to_queue(comment)

if __name__ == '__main__':
    video_id = 'YOUR_VIDEO_ID'  # Replace with your actual video ID
    threading.Thread(target=fetch_and_send_comments, args=(video_id,)).start()
    threading.Thread(target=start_consumer).start()

