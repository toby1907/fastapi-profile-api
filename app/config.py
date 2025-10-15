import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Dynamic Profile API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Cat Facts API configuration
    CAT_FACTS_API_URL: str = "https://catfact.ninja/fact"
    CAT_FACTS_TIMEOUT: int = 10
    
    # User profile information
    USER_EMAIL: str = os.getenv("USER_EMAIL", "olaleyetobi3@gmail.com")
    USER_NAME: str = os.getenv("USER_NAME", "Olaleye Paul Tobi")
    USER_STACK: str = os.getenv("USER_STACK", "Python/FastAPI")
    
    # CORS settings
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "*"  # For testing, restrict in production
    ]

settings = Settings()