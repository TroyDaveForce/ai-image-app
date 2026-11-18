from .base import ImageProvider
import requests
import os

class CloudflareProvider(ImageProvider):
    def __init__(self):
        self.account_id = os.getenv("CF_ACCOUNT_ID")
        self.api_token = os.getenv("CF_API_TOKEN")
        self.model = "@cf/black-forest-labs/flux-1-schnell"

    def generate(self, prompt: str, width: int = 1024, height: int = 1024) -> str:
        url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/{self.model}"
        headers = {"Authorization": f"Bearer {self.api_token}"}
        data = {"prompt": prompt}
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        image_b64 = result.get("result", {}).get("image")
        
        if not image_b64:
            raise Exception("No image data returned from Cloudflare")
            
        # Convert the base64 string into a data URL that the browser can render
        return f"data:image/jpeg;base64,{image_b64}"