from functools import lru_cache
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    APP_NAME: str = "FastAPI User Management"

    APP_VERSION: str = "1.0.0"

    DATABASE_URL: str 
    
    SECRET_KEY: str 

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15 

    ALGORITHM: str = "HS256"

    REFRESH_TOKEN_EXPIRE_DAYS: int = 10 


    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Use as a FastAPI dependency for better testability.
    """
    return Settings() 