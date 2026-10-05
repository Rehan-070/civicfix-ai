import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "CivicFix AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment & Demo Mode
    DEMO_MODE: bool = True
    ENVIRONMENT: str = "development"
    
    # Database
    DATABASE_URL: str = "sqlite:///./civicfix.db"
    
    # Security
    JWT_SECRET: str = "super-secret-civicfix-key-for-hackathon-demo-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Storage
    UPLOAD_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_MIME_TYPES: list[str] = ["image/jpeg", "image/png", "image/webp"]
    
    # Optional External AI API Keys
    LLM_API_KEY: str = ""
    VISION_API_KEY: str = ""
    MAPS_API_KEY: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

# Ensure uploads directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
