from .pollinations import PollinationsProvider
from .huggingface import HuggingFaceProvider
from .cloudflare import CloudflareProvider
from .fal import FalProvider
from .ideogram import IdeogramProvider
from .openai_provider import OpenAIProvider

PROVIDER_MAP = {
    "pollinations-flux": PollinationsProvider,
    "huggingface-flux": HuggingFaceProvider,
    "cloudflare-flux": CloudflareProvider,
    "fal-flux-2-flash": FalProvider,
    "fal-flux-2-pro": FalProvider,
    "ideogram-4-5": IdeogramProvider,
    "openai-gpt-image-1": OpenAIProvider,
}