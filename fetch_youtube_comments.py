import os
import googleapiclient.discovery

def get_youtube_comments(video_id, api_key):
    # Disable OAuthlib's HTTPS verification when running locally.
    # DO NOT leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Build the YouTube service object.
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    # Get the comments
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText"
    )
    response = request.execute()

    comments = []
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)

    return comments

if __name__ == "__main__":
    # Replace 'YOUR_API_KEY' with your actual YouTube Data API key
    api_key = 'AIzaSyCCelfOhh7zVUoyGxI1czv0FCUwmYkMb5U'
    # Replace 'VIDEO_ID' with the actual video ID you want to fetch comments from
    video_id = 'nWzbmbHa8fw'

    comments = get_youtube_comments(video_id, api_key)
    for comment in comments:
        print(comment)


def get_all_comments(video_id, api_key):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    comments = []
    next_page_token = None

    while True:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return comments

# Usage remains the same


