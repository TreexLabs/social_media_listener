import os
import time
import logging
from googleapiclient.discovery import build
from config.settings import YOUTUBE_API_KEY

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_channel_videos(channel_id):
    """
    Fetches a list of video IDs from a specified YouTube channel.

    Args:
        channel_id (str): The ID of the YouTube channel.

    Returns:
        list: A list of video IDs.

    Raises:
        HttpError: If an error occurs while executing the request.
    """
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
    """
    Retrieves comments from a YouTube video.

    Args:
        video_id (str): The ID of the YouTube video.

    Returns:
        list: A list of comments from the video.
    """
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

# def fetch_comments(video_id):
#     """
#     Fetches comments from a YouTube video.

#     Args:
#         video_id (str): The ID of the YouTube video.

#     Returns:
#         list: A list of dictionaries containing information about each comment. Each dictionary has the following keys:
#             - 'video_id' (str): The ID of the video.
#             - 'author' (str): The display name of the comment author.
#             - 'text' (str): The original text of the comment.
#             - 'published_at' (str): The date and time when the comment was published.
#             - 'like_count' (int): The number of likes the comment has received.
#             - 'favorite_count' (int): The number of favorites the comment has received.

#     Raises:
#         None

#     Notes:
#         - This function uses the YouTube Data API v3 to fetch comments from a video.
#         - The maximum number of comments fetched per request is 100.
#         - The 'favoriteCount' key may not be present in the comment dictionary, so it is fetched using the get() method with a default value of 0.
#     """
#     youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
#     request = youtube.commentThreads().list(
#         part='snippet',
#         videoId=video_id,
#         maxResults=100
#     )
#     response = request.execute()
#     comments = []
#     for item in response['items']:
#         comment = item['snippet']['topLevelComment']['snippet']
#         comments.append({
#             'video_id': video_id,
#             'author': comment['authorDisplayName'],
#             'text': comment['textOriginal'],
#             'published_at': comment['publishedAt'],
#             'like_count': comment['likeCount'],
#             'favorite_count': comment.get('favoriteCount', 0)
#         })
#     return comments
