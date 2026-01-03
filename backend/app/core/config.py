"""
Application configuration settings
"""
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    PROJECT_NAME: str = "FESE - Financial Engineering & Smart Economy"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # Blockchain settings
    BLOCKCHAIN_NETWORK: str = "localhost"
    BLOCKCHAIN_RPC_URL: str = "http://127.0.0.1:8545"
    CONTRACT_ADDRESS: str = ""
    
    # Database (if needed)
    DATABASE_URL: str = "sqlite:///./fese.db"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
