import os

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', 'YOUR_YOUTUBE_API_KEY')
RABBITMQ_URL = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/')
QUEUE_NAME = 'youtube_comments'
EXCEL_OUTPUT_DIR = 'output/'
CHANNEL_ID = os.getenv('CHANNEL_ID', 'UCMgbYmq6I5zcQUiCN-k_pFA')
EXCLUDE_VIDEOS=['_mljnxa9IR4','vDViqlhEjyI']
PUBLISHED_AFTER='2021-01-01T00:00:00Z'
PUBLISHED_BEFORE='2021-12-01T23:59:59Z'
