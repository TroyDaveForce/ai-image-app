from .base import ImageProvider
from openai import OpenAI
import os

class OpenAIProvider(ImageProvider):
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate(self, prompt: str, width: int = 1024, height: int = 1024) -> str:
        response = self.client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="high"
        )
        return "openai_image_url_placeholder"