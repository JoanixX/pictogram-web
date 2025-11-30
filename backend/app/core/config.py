import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Pictogram AI Backend"
    # DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    DATABASE_URL: str = "sqlite:///./test.db"


settings = Settings()