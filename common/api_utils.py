import os
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic

load_dotenv()

def get_openai_client() -> OpenAI | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        return None
    return OpenAI(api_key=api_key)

def get_anthropic_client() -> Anthropic | None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key == "your_anthropic_api_key_here":
        return None
    return Anthropic(api_key=api_key)
