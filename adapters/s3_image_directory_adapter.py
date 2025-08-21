import boto3
import random
from botocore.client import Config
from ports.driven_port import ImageDirectoryPort

class S3ImageDirectoryAdapter(ImageDirectoryPort):
    """Adapter for retrieving a random image from an S3 directory."""

    def __init__(self, bucket_name: str, aws_access_key_id=None, aws_secret_access_key=None, region_name=None):
        self.bucket_name = bucket_name
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
            # Use the correct endpoint URL for S3, it's necessary for some regions (eu-south-1, etc.)
            endpoint_url=f"https://s3.{region_name}.amazonaws.com",
            config=Config(signature_version="s3v4")
        )

    def get_random_image(self, directory: str) -> str:
        # List all objects under the given prefix (directory)
        paginator = self.s3.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=self.bucket_name, Prefix=directory)
        images = []
        for page in page_iterator:
            for obj in page.get('Contents', []):
                key = obj['Key']
                if key.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    images.append(key)
        if not images:
            return None
        selected_key = random.choice(images)
        # Generate a presigned URL (valid for 1 hour)
        url = self.s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket_name, 'Key': selected_key},
            ExpiresIn=3600
        )
        return url