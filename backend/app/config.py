import os

try:
    from dotenv import load_dotenv
    load_dotenv()
    load_dotenv("backend/.env")
except ImportError:
    pass

class Settings:
    PROJECT_NAME: str = "Celonis Marketing Asset Translation Engine"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    DEFAULT_TRANSLATION_MODEL: str = "gemini-1.5-flash"
    DEFAULT_JUDGE_MODEL: str = "gemini-1.5-pro"

settings = Settings()
