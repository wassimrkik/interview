
from pydantic import BaseModel

class ImageRequest(BaseModel):
    prompt: str
    size: str = "512x512"
    n : int = 1

class TextRequest(BaseModel):
    prompt: str
