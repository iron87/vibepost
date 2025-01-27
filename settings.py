import os
from dotenv import load_dotenv

load_dotenv()  # Carica le variabili d'ambiente da .env

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./database.db")

settings = Settings()
