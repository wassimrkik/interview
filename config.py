from google import genai
from google.generativeai import types
from openai import OpenAI
import anthropic
from groq import Groq

from dotenv import load_dotenv
import httpx
import os

load_dotenv()


client_google = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
    )
    
############################

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.getenv("OPEN_API_KEY")
)

############################

client_anth = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)

client_groq = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
    http_client=httpx.Client(verify=False)
)