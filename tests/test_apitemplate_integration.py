import os
import unittest
from adapters.apitemplate_adapter import APITemplateImageGeneratorAdapter

class TestAPITemplateImageGeneratorIntegration(unittest.TestCase):
    def setUp(self):
        self.api_key = os.environ.get("APITEMPLATE_API_KEY")
        self.template_id = "90e77b238b565ee4"
        if not self.api_key or not self.template_id:
            self.skipTest("Set APITEMPLATE_API_KEY and APITEMPLATE_TEMPLATE_ID in environment variables to run this test.")
        self.adapter = APITemplateImageGeneratorAdapter(self.api_key)

    def test_generate_image_real_api(self):
        overrides = [
            {"name": "text_big", "text": "Integration Test"}] 
        image_url = self.adapter.generate_image(self.template_id, overrides)
        print("Generated image URL:", image_url)
        self.assertIsInstance(image_url, str)
        self.assertTrue(image_url.startswith("http"))

if __name__ == "__main__":
    unittest.main()