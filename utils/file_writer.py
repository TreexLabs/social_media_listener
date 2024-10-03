import pandas as pd
from config.settings import EXCEL_OUTPUT_DIR
import os

def write_to_excel(item):
    comment = {
                    'video_id': item['snippet']['topLevelComment']['snippet']['videoId'],
                    'author': item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                    'text': item['snippet']['topLevelComment']['snippet']['textOriginal'],
                    'published_at': item['snippet']['topLevelComment']['snippet']['publishedAt'],
                    'like_count': item['snippet']['topLevelComment']['snippet']['likeCount'],
                    'reply_count': item['snippet']['totalReplyCount']
                }
    date = comment['published_at'].split('T')[0]
    year, month, _ = date.split('-')
    directory = os.path.join(EXCEL_OUTPUT_DIR, year, month)

    # Create directories if they do not exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, f'{date}.xlsx')

    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
    else:
        df = pd.DataFrame(columns=['video_id', 'author', 'text', 'published_at', 'like_count', 'reply_count'])

    new_df = pd.DataFrame([comment], columns=['video_id', 'author', 'text', 'published_at', 'like_count', 'reply_count'])
    
    # Concatenate the existing DataFrame with the new comment DataFrame
    df = pd.concat([df, new_df], ignore_index=True)

    df.to_excel(file_path, index=False, engine='openpyxl')

