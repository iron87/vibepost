import os
import unittest
from adapters.apitemplate_adapter import APITemplateImageGeneratorAdapter

class TestAPITemplateImageGeneratorIntegration(unittest.TestCase):
    """Integration tests for APITemplateImageGeneratorAdapter using the real API."""

    def setUp(self):
        self.api_key = os.environ.get("APITEMPLATE_API_KEY")
        self.template_id = "34e77b23d8c3e972"
        self.img_url = "https://images.unsplash.com/photo-1482049016688-2d3e1b311543?q=80&w=820&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        if not self.api_key or not self.template_id:
            self.skipTest("Set APITEMPLATE_API_KEY and APITEMPLATE_TEMPLATE_ID in environment variables to run this test.")
        self.adapter = APITemplateImageGeneratorAdapter(self.api_key)

    def test_generate_image_real_api(self):
        overrides = [
            {"name": "text_big", "text": "Integration Test"}] 
        image_url = self.adapter.generate_image(self.template_id, self.img_url, overrides)
        print("Generated image URL:", image_url)
        self.assertIsInstance(image_url, str)
        self.assertTrue(image_url.startswith("http"))

if __name__ == "__main__":
    unittest.main()