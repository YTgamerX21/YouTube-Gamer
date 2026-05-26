"""
Configuration settings for the AI Assistant
"""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings and configuration"""
    
    # API Configuration
    API_TITLE: str = "YouTube Gamer AI Assistant"
    API_VERSION: str = "1.0.0"
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Model Configuration
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt2")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "150"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    TOP_P: float = float(os.getenv("TOP_P", "0.9"))
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    HUGGINGFACE_API_KEY: Optional[str] = os.getenv("HUGGINGFACE_API_KEY")
    
    # Server Configuration
    WORKERS: int = int(os.getenv("WORKERS", "4"))
    TIMEOUT: int = int(os.getenv("TIMEOUT", "30"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/app.log")
    
    # Feature Flags
    ENABLE_CODE_COMPLETION: bool = True
    ENABLE_CHAT: bool = True
    ENABLE_DEBUGGING: bool = True
    ENABLE_DOCUMENTATION: bool = True
    
    # Cache Configuration
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 3600  # 1 hour in seconds


settings = Settings()
