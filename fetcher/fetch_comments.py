from googleapiclient.discovery import build
from config.settings import YOUTUBE_API_KEY

def fetch_comments(video_id):
    """
    Fetches comments from a YouTube video.

    Args:
        video_id (str): The ID of the YouTube video.

    Returns:
        list: A list of dictionaries containing information about each comment. Each dictionary has the following keys:
            - 'video_id' (str): The ID of the video.
            - 'author' (str): The display name of the comment author.
            - 'text' (str): The original text of the comment.
            - 'published_at' (str): The date and time when the comment was published.
            - 'like_count' (int): The number of likes the comment has received.
            - 'favorite_count' (int): The number of favorites the comment has received.

    Raises:
        None

    Notes:
        - This function uses the YouTube Data API v3 to fetch comments from a video.
        - The maximum number of comments fetched per request is 100.
        - The 'favoriteCount' key may not be present in the comment dictionary, so it is fetched using the get() method with a default value of 0.
    """
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=100
    )
    response = request.execute()
    comments = []
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        comments.append({
            'video_id': video_id,
            'author': comment['authorDisplayName'],
            'text': comment['textOriginal'],
            'published_at': comment['publishedAt'],
            'like_count': comment['likeCount'],
            'favorite_count': comment.get('favoriteCount', 0)
        })
    return comments
