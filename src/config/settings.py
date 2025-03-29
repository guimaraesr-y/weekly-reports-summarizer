import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG: str = os.environ.get('DEBUG', False)
    GEMINI_API_KEY: str = os.environ.get('GEMINI_API_KEY', None)
    GEMINI_MODEL: str = os.environ.get('GEMINI_MODEL', 'gemini-1.5-flash') 