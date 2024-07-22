import os
import time
import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Your API key (use environment variable for security)
API_KEY = ('AIzaSyDI6bi_YezEblZqrXzHLc2muXBR53C7P_Q')  # Ensure this environment variable is set
if not API_KEY:
    logging.error("API_KEY not found. Please set the environment variable 'YOUTUBE_API_KEY'.")
    exit(1)

# The ID of the YouTube channel
CHANNEL_ID = 'UClCFVPNhvTLFxHWzdYXMFAg'  # Replace with your actual channel ID

# Create a YouTube resource object
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_channel_videos(channel_id):
    videos = []
    request = youtube.search().list(
        part='id',
        channelId=channel_id,
        maxResults=50,
        order='date'
    )
    
    while request:
        try:
            response = request.execute()
            for item in response['items']:
                if item['id']['kind'] == 'youtube#video':
                    videos.append(item['id']['videoId'])
            request = youtube.search().list_next(request, response)
        except HttpError as e:
            logging.error(f"An error occurred: {e}")
            break
    
    return videos

def get_comments(video_id):
    comments = []
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText'
    )
    
    while request:
        try:
            response = request.execute()
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)
            request = youtube.commentThreads().list_next(request, response)
        except HttpError as e:
            logging.error(f"An error occurred: {e}")
            break
    
    return comments

def monitor_channel_comments(channel_id, interval=60):
    seen_comments = set()
    seen_videos = set()
    
    while True:
        logging.info("Checking for new videos and comments...")
        videos = get_channel_videos(channel_id)
        
        new_videos = [video for video in videos if video not in seen_videos]
        for video_id in new_videos:
            logging.info(f"New video detected: {video_id}")
            seen_videos.add(video_id)
        
        for video_id in videos:
            comments = get_comments(video_id)
            new_comments = [c for c in comments if c not in seen_comments]
            
            if new_comments:
                for comment in new_comments:
                    logging.info("New comment: %s", comment)
                seen_comments.update(new_comments)
        
        time.sleep(interval)

if __name__ == '__main__':
    monitor_channel_comments(CHANNEL_ID, interval=60)
