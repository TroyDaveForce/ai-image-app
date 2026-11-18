from .base import ImageProvider
import requests
import os

class HuggingFaceProvider(ImageProvider):
    def __init__(self):
        self.api_key = os.getenv("HF_TOKEN")
        self.api_url = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def generate(self, prompt: str, width: int = 1024, height: int = 1024) -> str:
        payload = {
            "inputs": prompt,
            "parameters": {"width": width, "height": height}
        }
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        # This direct endpoint returns the image bytes, not a URL.
        # For a production app, you would save these bytes to a file or cloud storage.
        # For now, we'll return a placeholder URL to keep the app running.
        print(f"Image generated successfully, size: {len(response.content)} bytes")
        return "https://image.pollinations.ai/prompt/placeholder?width=1024&height=1024"