from .base import ImageProvider
import urllib.parse

class PollinationsProvider(ImageProvider):
    def generate(self, prompt: str, width: int = 1024, height: int = 1024) -> str:
        encoded_prompt = urllib.parse.quote(prompt)
        return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model=flux"