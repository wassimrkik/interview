
from pydantic import BaseModel
from enum import Enum

class ImageRequest(BaseModel):
    prompt: str
    size: str = "512x512"
    n : int = 1

class TextRequest(BaseModel):
    prompt: str

class Aimodel(str, Enum):
    openai = "openai"
    gemini = "gemini"
    anthropic = "claude"
    groq = "Groq"