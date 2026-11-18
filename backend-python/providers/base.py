from abc import ABC, abstractmethod

class ImageProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, width: int = 1024, height: int = 1024) -> str:
        """Returns the URL of the generated image."""
        pass