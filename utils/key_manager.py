from googleapiclient.discovery import build
import os, sys
import itertools
import time
config_dir = os.path.abspath(os.getcwd()+"/config")
sys.path.append(config_dir)
from settings import YOUTUBE_API_KEY

class YouTubeAPIKeyManager:
    def __init__(self, api_keys):
        self.api_key = itertools.cycle(api_keys)
        self.current_key = next(self.api_key)
        self.youtube = self.build_youtube_client(self.current_key)

    def build_youtube_client(self, api_key):
        return build('youtube', 'v3', developerKey=api_key)

    def get_youtube_client(self):
        return self.youtube

    def rotate_key(self):
        self.current_key = next(self.api_key)
        self.youtube = self.build_youtube_client(self.current_key)

    def check_quota(self):
        if QUOTA_USAGE[self.current_key] >= QUOTA_LIMIT:
            print(f"Quota limit reached for API key index {self.current_key}. Switching to the next key.")
            self.rotate_key()
            CURRENT_KEY_INDEX = (CURRENT_KEY_INDEX + 1) % len(api_keys)
            if CURRENT_KEY_INDEX == 0:
                print("All API keys have reached their quota limit. Pausing requests until next day.")
                time.sleep(24 * 60 * 60)  # Sleep for 24 hours
                for i in range(len(QUOTA_USAGE)):
                    QUOTA_USAGE[i] = 0 
        
    
api_keys = [
    'AIzaSyCIW2AFalSwm3pPYfRDUAgltBx-AgAwBEM',
    'AIzaSyB2qB9lqcPyxvunJE2ZptowwrlSzuvCHX8',
    YOUTUBE_API_KEY,
    'AIzaSyAM3osaFTBDKzid9Gyv5w6sYdB1WpS9qyc'
]
QUOTA_LIMIT = 10000  # Daily quota limit per key
QUOTA_USAGE = [0] * len(api_keys)  # Track quota usage for each key
REQUEST_COST = 1  # Cost per commentThreads.list request
CURRENT_KEY_INDEX = 0

youtube_api_manager = YouTubeAPIKeyManager(api_keys)