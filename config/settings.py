import os

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', 'YOUR_YOUTUBE_API_KEY')
RABBITMQ_URL = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/')
QUEUE_NAME = 'youtube_comments'
EXCEL_OUTPUT_DIR = 'output1/'
CHANNEL_ID = os.getenv('CHANNEL_ID', 'UCMgbYmq6I5zcQUiCN-k_pFA')
EXCLUDE_VIDEOS=['_mljnxa9IR4','vDViqlhEjyI']
