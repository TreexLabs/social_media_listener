import os
from urllib.error import HTTPError
import time
import logging
from utils.key_manager import youtube_api_manager
from producer.producer import send_to_queue
import json
from config.settings import EXCLUDE_VIDEOS, PUBLISHED_AFTER, PUBLISHED_BEFORE
from googleapiclient.errors import HttpError
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_channel_videos(channel_id, published_after=PUBLISHED_AFTER, published_before=PUBLISHED_BEFORE):
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
    youtube = youtube_api_manager.get_youtube_client()
    try:
        response = youtube.search().list(
            part='snippet',
            publishedAfter=published_after,
            publishedBefore=published_before,
            channelId=channel_id,
            maxResults=50,
            order='date'
        ).execute()
        
        while response:
            try:
                for item in response['items']:
                    if item['id']['kind'] == 'youtube#video':
                        published_at = item['snippet']['publishedAt']
                        if published_at >= published_after and published_at <= published_before and item['id']['videoId'] not in EXCLUDE_VIDEOS:
                            videos.append(item['id']['videoId'])
                if 'nextPageToken' in response:
                    response = youtube.search().list(
                    channelId=channel_id,
                    publishedAfter=published_after,
                    publishedBefore=published_before,
                    part='snippet',
                    maxResults=50,
                    order='date',
                    pageToken=response['nextPageToken']).execute()
                else:
                    break
            except Exception as e:
                logging.error(f"An error occurred: {e}")
                break
    except HttpError as e:
        logging.error(f"An error occurred: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
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
    youtube = youtube_api_manager.get_youtube_client()
    response = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText',
        maxResults=100
    ).execute()
    
    while response:
        try:
            for item in response['items']:
                comments.append({
                    'video_id': item['snippet']['topLevelComment']['snippet']['videoId'],
                    'author': item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                    'text': item['snippet']['topLevelComment']['snippet']['textOriginal'],
                    'published_at': item['snippet']['topLevelComment']['snippet']['publishedAt'],
                    'like_count': item['snippet']['topLevelComment']['snippet']['likeCount'],
                    'reply_count': item['snippet']['totalReplyCount']
                })
            if 'nextPageToken' in response:
                response = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    textFormat='plainText',
                    pageToken=response['nextPageToken'],
                    maxResults=100 
                ).execute()
            else:
                break
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            break
    
    return comments

def monitor_channel_comments(channel_id, interval=60):
    seen_comments = set()
    seen_videos = set()
    while True:
        try:
            logging.info("Checking for new videos and comments...")
            videos = get_channel_videos(channel_id)
            
            new_videos = [video for video in videos if video not in seen_videos]
            for video_id in new_videos:
                logging.info(f"New video detected: {video_id}")
                seen_videos.add(video_id)
            
            for video_id in videos:
                if video_id in EXCLUDE_VIDEOS:
                    continue
                try:
                    comments = get_comments(video_id)
                except HttpError as e:
                    if e.resp.status == 403:
                        error_reason = e.error_details[0]['reason']
                        if 'quotaExceeded' in error_reason:
                            logging.error(f"Quota exceeded")
                            youtube_api_manager.rotate_key()
                        else:
                            logging.error(f"HTTP 403 error for video ID: {video_id}. Adding to EXCLUDE_VIDEOS.")
                            EXCLUDE_VIDEOS.append(video_id)
                            time.sleep(interval)
                    else:
                        logging.error(f"An error occurred: {e}")
                        time.sleep(interval)
                        youtube_api_manager.rotate_key()
                except Exception as e:
                    logging.error(f"An error occurred: {e}")
                    time.sleep(interval)
                    youtube_api_manager.rotate_key()
                
                new_comments = [c for c in comments if c['text'] not in seen_comments]
                if new_comments:
                    for comment in new_comments:
                        logging.info("New comment: %s", comment)
                        send_to_queue(comment)
                        seen_comments.update(comment['text'])
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            time.sleep(interval)
            youtube_api_manager.rotate_key()

