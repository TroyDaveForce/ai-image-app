from .base import ImageProvider
import requests
import os

class IdeogramProvider(ImageProvider):
    def __init__(self):
        self.api_key = os.getenv("IDEOGRAM_API_KEY")
        self.base_url = "https://api.ideogram.ai"

    def generate(self, prompt: str, width: int = 1024, height: int = 1024) -> str:
        headers = {"Api-Key": self.api_key}
        payload = {"prompt": prompt}
        
        response = requests.post(f"{self.base_url}/v2/image/generate/ideogram-4-5", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["data"][0]["url"]