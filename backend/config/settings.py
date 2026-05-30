"""
Configuration settings for Foodie application
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings"""
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./foodie.db")
    
    # JWT
    SECRET_KEY = os.getenv("SECRET_KEY", "sb_publishable_Dij3VqTJEpqUJuvh86P1OA_aD7oAi-2")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    # CORS
    CORS_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000", "http://localhost:5500", "http://127.0.0.1:5500"]
    
    # Application
    APP_NAME = "Foodie"
    APP_VERSION = "1.0.0"
    
    # Pagination
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100


settings = Settings()
