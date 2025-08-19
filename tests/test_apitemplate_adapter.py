import unittest
from unittest.mock import patch, MagicMock
from adapters.apitemplate_adapter import APITemplateImageGeneratorAdapter

class TestAPITemplateImageGeneratorAdapter(unittest.TestCase):
    @patch("adapters.apitemplate_adapter.requests.post")
    def test_generate_image_success(self, mock_post):
        # Arrange
        adapter = APITemplateImageGeneratorAdapter(api_key="fake-key")
        template_id = "template123"
        overrides = [
            {"name": "text_1", "text": "hello world"},
            {"name": "image_1", "src": "https://via.placeholder.com/150"}
        ]
        expected_url = "https://apitemplate.io/download/abc123.png"

        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"download_url": expected_url}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        # Act
        result = adapter.generate_image(template_id, overrides)

        # Assert
        self.assertEqual(result, expected_url)
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertIn("X-API-KEY", kwargs["headers"])
        self.assertEqual(kwargs["json"]["overrides"], overrides)
        self.assertTrue(kwargs["url"].endswith(f"?template_id={template_id}"))

if __name__ == "__main__":
    unittest.main()