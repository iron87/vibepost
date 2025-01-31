import os
from dotenv import load_dotenv

load_dotenv()  
class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./database.db")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY","")
    LLM_API_URL: str = os.getenv("LLM_API_URL","http://localhost:11434")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER","ollama")
    LLM_MODEL: str = os.getenv("LLM_MODEL","llama3.1:8b")
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN","");
settings = Settings()
