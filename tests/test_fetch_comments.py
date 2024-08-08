import unittest
from unittest.mock import patch, MagicMock
from fetcher.fetch_comments import get_comments

class TestGetComments(unittest.TestCase):

    @patch('fetcher.fetch_comments.youtube')
    def test_get_comments_with_valid_video_id(self, mock_youtube):
        # Arrange
        video_id = 'valid_video_id'
        mock_response = {
            'items': [
                {
                    'snippet': {
                        'topLevelComment': {
                            'snippet': {
                                'textDisplay': 'comment1'
                            }
                        }
                    }
                },
                {
                    'snippet': {
                        'topLevelComment': {
                            'snippet': {
                                'textDisplay': 'comment2'
                            }
                        }
                    }
                }
            ]
        }
        mock_youtube.commentThreads().list.return_value.execute.return_value = mock_response

        # Act
        comments = get_comments(video_id)

        # Assert
        self.assertEqual(comments, ['comment1', 'comment2'])

    @patch('fetcher.fetch_comments.youtube')
    def test_get_comments_with_invalid_video_id(self, mock_youtube):
        # Arrange
        video_id = 'invalid_video_id'
        mock_response = {}
        mock_youtube.commentThreads().list.return_value.execute.return_value = mock_response

        # Act
        comments = get_comments(video_id)

        # Assert
        self.assertEqual(comments, [])

    @patch('fetcher.fetch_comments.youtube')
    def test_get_comments_with_http_error(self, mock_youtube):
        # Arrange
        video_id = 'valid_video_id'
        mock_youtube.commentThreads().list.side_effect = HttpError(
            {'status': '404'},
            b'{"error": {"errors": [{"domain": "youtube.commentThread", "reason": "videoNotFound", "message": "Video not found."}]}}'
        )

        # Act
        with self.assertLogs(level='ERROR') as cm:
            comments = get_comments(video_id)

        # Assert
        self.assertEqual(comments, [])
        self.assertEqual(len(cm.output), 1)
        self.assertIn('An error occurred: HttpError: <HttpError 404', cm.output[0])

if __name__ == '__main__':
    unittest.main()
