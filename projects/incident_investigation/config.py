"""
Configuration management for Incident Investigation System.
Loads settings from environment variables (.env file).
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Configuration class for the Incident Investigation System."""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL: str = os.getenv('OPENAI_MODEL', 'gpt-4o')
    OPENAI_VISION_MODEL: str = os.getenv('OPENAI_VISION_MODEL', 'gpt-4o')
    OPENAI_TEMPERATURE: float = float(os.getenv('OPENAI_TEMPERATURE', '0.2'))
    
    # Vector Database Configuration
    PINECONE_API_KEY: Optional[str] = os.getenv('PINECONE_API_KEY')
    PINECONE_ENVIRONMENT: Optional[str] = os.getenv('PINECONE_ENVIRONMENT')
    PINECONE_INDEX_NAME: str = os.getenv('PINECONE_INDEX_NAME', 'incident-investigations')
    
    # Database Configuration
    DATABASE_URL: Optional[str] = os.getenv('DATABASE_URL')
    REDIS_URL: Optional[str] = os.getenv('REDIS_URL')
    
    # File Storage Configuration
    S3_BUCKET_NAME: Optional[str] = os.getenv('S3_BUCKET_NAME')
    S3_REGION: str = os.getenv('S3_REGION', 'us-east-1')
    AWS_ACCESS_KEY_ID: Optional[str] = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    # Application Settings
    ENVIRONMENT: str = os.getenv('ENVIRONMENT', 'development')
    DEBUG: bool = os.getenv('DEBUG', 'True').lower() == 'true'
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    # Security Settings
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    ALLOWED_ORIGINS: list = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
    
    # Email Configuration
    SMTP_HOST: str = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    SMTP_PORT: int = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USERNAME: Optional[str] = os.getenv('SMTP_USERNAME')
    SMTP_PASSWORD: Optional[str] = os.getenv('SMTP_PASSWORD')
    EMAIL_FROM: str = os.getenv('EMAIL_FROM', 'noreply@incident-investigation.com')
    
    # Company/Organization Settings
    COMPANY_NAME: str = os.getenv('COMPANY_NAME', 'Your Company')
    ORGANIZATION_ID: str = os.getenv('ORGANIZATION_ID', 'default-org')
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent
    OUTPUTS_DIR: Path = BASE_DIR / 'outputs'
    REPORTS_DIR: Path = OUTPUTS_DIR / 'reports'
    DIAGRAMS_DIR: Path = OUTPUTS_DIR / 'diagrams'
    EVIDENCE_DIR: Path = BASE_DIR / 'evidence'
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate that required configuration is present.
        
        Returns:
            bool: True if configuration is valid
            
        Raises:
            ValueError: If required configuration is missing
        """
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is required. Please set it in your .env file.\n"
                "Copy .env.example to .env and add your API key."
            )
        
        # Create necessary directories
        cls.OUTPUTS_DIR.mkdir(exist_ok=True)
        cls.REPORTS_DIR.mkdir(exist_ok=True)
        cls.DIAGRAMS_DIR.mkdir(exist_ok=True)
        cls.EVIDENCE_DIR.mkdir(exist_ok=True)
        
        return True
    
    @classmethod
    def get_openai_client_config(cls) -> dict:
        """
        Get configuration for OpenAI client.
        
        Returns:
            dict: Configuration dictionary for OpenAI client
        """
        return {
            'api_key': cls.OPENAI_API_KEY,
            'model': cls.OPENAI_MODEL,
            'vision_model': cls.OPENAI_VISION_MODEL,
            'temperature': cls.OPENAI_TEMPERATURE
        }
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment."""
        return cls.ENVIRONMENT.lower() == 'production'
    
    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development environment."""
        return cls.ENVIRONMENT.lower() == 'development'


# Singleton instance
config = Config()

# Validate configuration on import (only in production)
if config.is_production():
    config.validate()
