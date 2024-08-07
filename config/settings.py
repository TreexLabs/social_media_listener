import os

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', 'YOUR_YOUTUBE_API_KEY')
RABBITMQ_URL = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/')
QUEUE_NAME = 'youtube_comments'
EXCEL_OUTPUT_DIR = 'output/'

