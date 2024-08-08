from googleapiclient.discovery import build
import os, sys
import itertools
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
    
api_keys = [
    YOUTUBE_API_KEY,
    'AIzaSyAM3osaFTBDKzid9Gyv5w6sYdB1WpS9qyc',
    'AIzaSyChdh26NjCpkvy_x-WZrlltXptr91VMGRU',
    'AIzaSyCMgL-aXmdgDcxCeeAmcFIgJ79DIZ_Sp5k',
    'AIzaSyCAl8LcoBDlZ80rDEd2EwK6AWhsEsOs08Y'
]

youtube_api_manager = YouTubeAPIKeyManager(api_keys)