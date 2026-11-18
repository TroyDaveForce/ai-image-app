from .base import ImageProvider
import fal_client
import os

class FalProvider(ImageProvider):
    def __init__(self):
        if not os.getenv("FAL_KEY"):
            raise ValueError("FAL_KEY environment variable is not set")

    def generate(self, prompt: str, width: int = 1024, height: int = 1024) -> str:
        result = fal_client.subscribe(
            "fal-ai/flux-2/flash",
            arguments={"prompt": prompt, "image_size": "square_hd", "num_images": 1}
        )
        return result["images"][0]["url"]