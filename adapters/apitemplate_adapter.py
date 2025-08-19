import requests
from ports.driven_port import ImageGeneratorPort

class APITemplateImageGeneratorAdapter(ImageGeneratorPort):
    """Adapter for generating images using apitemplate.io API v2."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://rest.apitemplate.io/v2/create-image"

    def generate_image(self, template_id: str, overrides: list) -> str:
        """
        Calls apitemplate.io API v2 to generate an image and returns the image URL.
        :param template_id: The apitemplate.io template ID.
        :param overrides: List of override dicts as required by apitemplate.io.
        :return: URL of the generated image.
        """
        url = f"{self.base_url}?template_id={template_id}"
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "overrides": overrides
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        # The image URL is usually in 'download_url'
        return result.get("download_url")