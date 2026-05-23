"""
Application configuration management using Pydantic Settings
Supports environment-specific configurations with ADA compliance
"""
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr


class Settings(BaseSettings):
    """Application settings with ADA protocol compliance"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    
    # FastAPI Configuration
    API_TITLE: str = "Enterprise RAG System"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Agentic RAG System for Document Analysis with Enterprise Features"
    ENVIRONMENT: str = Field(default="development", description="Environment: development, testing, production")
    DEBUG: bool = Field(default=False, description="Enable debug mode")
    
    # Server Configuration
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    WORKERS: int = Field(default=4, description="Number of workers")
    
    # Security
    SECRET_KEY: SecretStr = Field(default="change-me-in-production", description="Secret key for JWT")
    ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="Access token expiration")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, description="Refresh token expiration")
    
    # Database
    DATABASE_URL: Optional[str] = Field(default=None, description="PostgreSQL connection string")
    DB_ECHO: bool = Field(default=False, description="SQL echo mode")
    
    # Redis
    REDIS_URL: Optional[str] = Field(default="redis://localhost:6379/0", description="Redis connection")
    REDIS_CACHE_EXPIRE: int = Field(default=3600, description="Cache expiration in seconds")
    
    # Chroma DB
    CHROMA_DB_PATH: str = Field(default="./chroma_db", description="Chroma DB path")
    CHROMA_HOST: Optional[str] = Field(default="localhost", description="Chroma host")
    CHROMA_PORT: Optional[int] = Field(default=8001, description="Chroma port")
    
    # LLM Configuration
    OPENAI_API_KEY: Optional[SecretStr] = Field(default=None, description="OpenAI API key")
    OPENAI_MODEL: str = Field(default="gpt-4", description="OpenAI model")
    ANTHROPIC_API_KEY: Optional[SecretStr] = Field(default=None, description="Anthropic API key")
    
    # Embeddings
    EMBEDDING_MODEL: str = Field(default="text-embedding-3-small", description="Embedding model")
    EMBEDDING_DIMENSION: int = Field(default=1536, description="Embedding dimension")
    
    # Document Processing
    MAX_UPLOAD_SIZE: int = Field(default=52428800, description="Max upload size (bytes)")
    ALLOWED_EXTENSIONS: List[str] = Field(
        default=["pdf", "docx", "xlsx", "csv", "txt", "json"],
        description="Allowed file extensions"
    )
    
    # Agentic RAG
    RAG_CHUNK_SIZE: int = Field(default=1000, description="Chunk size for RAG")
    RAG_CHUNK_OVERLAP: int = Field(default=200, description="Chunk overlap")
    RAG_TOP_K: int = Field(default=5, description="Top K results")
    MAX_TOKENS: int = Field(default=2000, description="Max tokens for generation")
    
    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:4200", "http://localhost:3000"],
        description="Allowed origins"
    )
    CORS_CREDENTIALS: bool = Field(default=True, description="Allow credentials")
    CORS_METHODS: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        description="Allowed HTTP methods"
    )
    CORS_HEADERS: List[str] = Field(
        default=["Content-Type", "Authorization"],
        description="Allowed headers"
    )
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FORMAT: str = Field(default="json", description="Log format: json or standard")
    
    # Monitoring
    PROMETHEUS_ENABLED: bool = Field(default=True, description="Enable Prometheus")
    SENTRY_DSN: Optional[str] = Field(default=None, description="Sentry DSN")
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = Field(default=100, description="Rate limit requests")
    RATE_LIMIT_PERIOD: int = Field(default=3600, description="Rate limit period (seconds)")
    
    # ADA Protocol Compliance
    ENABLE_ADA_COMPLIANCE: bool = Field(default=True, description="Enable ADA compliance")
    AUDIT_LOG_ENABLED: bool = Field(default=True, description="Enable audit logging")
    ENCRYPTION_ENABLED: bool = Field(default=True, description="Enable encryption")
    

# Create settings instance
settings = Settings()
