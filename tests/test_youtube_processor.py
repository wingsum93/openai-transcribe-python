import unittest
from unittest.mock import patch, MagicMock
from subtitle_generator import YoutubeProcessor
import requests
from pytube.exceptions import PytubeError

class TestYoutubeProcessor(unittest.TestCase):
    @patch('subtitle_generator.YoutubeProcessor.download_video')
    def test_download_video(self, mock_download):
        # Setup
        processor = YoutubeProcessor()
        test_url = "https://www.youtube.com/watch?v=example"
        expected_file_path = "/path/to/downloaded/video.mp4"

        # Mock the return value of the download_video method
        mock_download.return_value = expected_file_path

        # Test
        result = processor.download_video(test_url)

        # Assert
        mock_download.assert_called_with(test_url)
        self.assertEqual(result, expected_file_path)

    # More tests can be added here to cover different scenarios,
    # such as handling invalid URLs, errors during download, etc.
    @patch('subtitle_generator.YoutubeProcessor.download_video')
    def test_download_video_with_invalid_url(self, mock_download):
        processor = YoutubeProcessor()
        invalid_url = "this-is-not-a-valid-url"
        mock_download.side_effect = ValueError("Invalid YouTube URL")

        with self.assertRaises(ValueError):
            processor.download_video(invalid_url)

    @patch('subtitle_generator.YoutubeProcessor.download_video')
    @patch('pytube.YouTube')
    def test_download_video_network_issue(self,  mock_download,mock_youtube):
        processor = YoutubeProcessor()
        test_url = "https://www.youtube.com/watch?v=example"
        mock_youtube.side_effect = PytubeError("Network error occurred")

        result = processor.download_video(test_url)
        print(result)
        self.assertIsNone(result)
        mock_download.assert_called_with(test_url)

    @patch('subtitle_generator.YoutubeProcessor.download_video')
    def test_download_video_not_found(self, mock_download):
        processor = YoutubeProcessor()
        test_url = "https://www.youtube.com/watch?v=non_existent_video"
        mock_download.side_effect = FileNotFoundError("Video not found")

        with self.assertRaises(FileNotFoundError):
            processor.download_video(test_url)

    @patch('subtitle_generator.YoutubeProcessor.download_video')
    def test_download_video_empty_url(self, mock_download):
        processor = YoutubeProcessor()
        empty_url = ""
        mock_download.side_effect = ValueError("URL cannot be empty")

        with self.assertRaises(ValueError):
            processor.download_video(empty_url)

if __name__ == '__main__':
    unittest.main()
