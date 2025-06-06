from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator, EmailStr, PostgresDsn, SecretStr
import secrets

class Settings(BaseSettings):
    PROJECT_NAME: str = "MirrorScan"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = "development"
    
    # BACKEND_CORS_ORIGINS is a comma-separated list of origins
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database configuration
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "mirrorscan"
    SQLALCHEMY_DATABASE_URI: Union[PostgresDsn, str] = "sqlite:///./mirrorscan.db"

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Union[str, None], values: dict) -> str:
        if v and isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Scanning settings
    SCAN_TIMEOUT_SECONDS: int = 300
    MAX_CONCURRENT_SCANS: int = 5
    
    # Redis settings (for rate limiting and task queue)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""

    # Initial superuser
    FIRST_SUPERUSER_EMAIL: EmailStr = "admin@mirrorscan.ai"
    FIRST_SUPERUSER_PASSWORD: str = "admin123"  # Change in production!

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 