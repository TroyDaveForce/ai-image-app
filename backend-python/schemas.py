from pydantic import BaseModel

class GenerationRequest(BaseModel):
    prompt: str
    model_id: str
    width: int = 1024
    height: int = 1024
    negative_prompt: str | None = None # <-- NEW

class GenerationResponse(BaseModel):
    id: int
    prompt: str
    model_id: str
    image_url: str | None
    status: str