import unittest
from unittest.mock import patch, MagicMock
import json
import pika

from producer.producer import send_to_queue

class TestSendToQueue(unittest.TestCase):
    @patch('producer.producer.pika.BlockingConnection')
    def test_send_to_queue_success(self, mock_connection):
        message = {"key": "value"}
        connection_mock = MagicMock()
        channel_mock = MagicMock()
        connection_mock.channel.return_value = channel_mock
        mock_connection.return_value = connection_mock

        send_to_queue(message)

        connection_mock.channel.assert_called_once()
        channel_mock.queue_declare.assert_called_once_with(queue=QUEUE_NAME)
        # channel_mock.basic_publish.assert_called_once_with(exchange='', routing_key=QUEUE_NAME, body=json.