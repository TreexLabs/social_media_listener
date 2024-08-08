from googleapiclient.discovery import build
import os

# Set your YouTube Data API key here
API_KEY = os.getenv('YOUTUBE_API_KEY', 'YOUR_YOUTUBE_API_KEY')

def get_channel_id(api_key, for_username=None, for_url=None):
    youtube = build('youtube', 'v3', developerKey=api_key)

    if for_username:
        # Fetch channel details by username
        request = youtube.channels().list(
            part='id',
            forUsername=for_username
        )
    elif for_url:
        # Extract channel identifier from URL (if provided)
        if 'youtube.com/channel/' in for_url:
            return for_url.split('youtube.com/channel/')[1]
        elif 'youtube.com/@' in for_url:
            # Fetch channel details by custom URL (using @username format)
            username = for_url.split('youtube.com/@')[1]
            request = youtube.search().list(
                part='snippet',
                type='channel',
                q=username
            )
        else:
            raise ValueError("Invalid URL format.")
    else:
        raise ValueError("Provide either for_username or for_url.")

    response = request.execute()
    if 'items' in response and len(response['items']) > 0:
        return response['items'][0]['snippet']['channelId']
    else:
        raise ValueError("No channel found.")

# Example usage
if __name__ == "__main__":
    # Replace with your actual URL or API key
    try:
        channel_id = get_channel_id(API_KEY, for_url='https://www.youtube.com/@JohnWeslyMinistries')
        print(f'Channel ID: {channel_id}')
    except ValueError as e:
        print(e)
