"""
Configuration module for Travel Booking API.

Loads environment variables and provides application settings using pydantic-settings.
All secrets and configuration must be managed through environment variables.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Attributes:
        APP_NAME: Application name for logging and documentation
        DEBUG: Enable debug mode (detailed error messages)
        SECRET_KEY: Secret key for JWT token signing (must be kept secure)
        ALGORITHM: JWT hashing algorithm (default: HS256)
        ACCESS_TOKEN_EXPIRE_MINUTES: JWT token expiration time in minutes
        DATABASE_URL: PostgreSQL database connection string
    """
    
    APP_NAME: str = "TravelAPI"
    DEBUG: bool = False
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
