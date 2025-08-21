import os
import unittest
from adapters.s3_image_directory_adapter import S3ImageDirectoryAdapter

class TestS3ImageDirectoryAdapterIntegration(unittest.TestCase):
    def setUp(self):
        self.bucket_name = "vibepost-images"
        self.aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        self.region_name =  "eu-south-1"
        self.directory = "client1"  # e.g. "businesses/123/"
        if not all([self.bucket_name, self.aws_access_key_id, self.aws_secret_access_key, self.directory]):
            self.skipTest("Set AWS_S3_BUCKET, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_S3_TEST_DIRECTORY in environment variables to run this test.")
        self.adapter = S3ImageDirectoryAdapter(
            bucket_name=self.bucket_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name
        )

    def test_get_random_image(self):
        url = self.adapter.get_random_image(self.directory)
        print("Random image URL:", url)
        self.assertIsInstance(url, str)
        self.assertTrue(url.startswith("http"))

if __name__ == "__main__":
    unittest.main()