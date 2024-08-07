import pandas as pd
from config.settings import EXCEL_OUTPUT_DIR
import os

def write_to_excel(comment):
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
        df = pd.DataFrame(columns=['video_id', 'author', 'text', 'published_at', 'like_count', 'favorite_count'])

    df = df.append(comment, ignore_index=True)
    df.to_excel(file_path, index=False)

