from googleapiclient.discovery import build
from config.settings import YOUTUBE_API_KEY
import itertools

class YouTubeAPIKeyManager:
    def __init__(self, api_keys):
        self.api_key = itertools.cycle(api_keys)
        self.current_key = next(self.api_keys)
        self.youtube = self.build_youtube_client(self.current_key)

    def build_youtube_client(self, api_key):
        return build('youtube', 'v3', developerKey=api_key)

    def get_youtube_client(self):
        return self.youtube

    def rotate_key(self):
        self.current_key = next(self.api_keys)
        self.youtube = self.build_youtube_client(self.current_key)
    
api_keys = [
    YOUTUBE_API_KEY,
    '',
    ''
    
]