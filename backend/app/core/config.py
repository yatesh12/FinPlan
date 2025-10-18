from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Server
    PORT: int = 8000
    
    # Database
    USE_SQLITE: bool = False
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASS: str = ""
    DB_NAME: str = "mavericks"
    DB_SSL_CA_PATH: Optional[str] = None
    
    # JWT
    JWT_ACCESS_SECRET: str
    JWT_REFRESH_SECRET: str
    ACCESS_TOKEN_EXPIRES_IN: str = "900s"  # 15 minutes
    REFRESH_TOKEN_EXPIRES_IN: str = "7d"   # 7 days
    
    # Bcrypt
    BCRYPT_SALT_ROUNDS: int = 10
    
    # CORS
    FRONTEND_ORIGIN: str = "http://localhost:3000"
    
    # Cookies
    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: str = "Lax"
    
    @property
    def DATABASE_URL(self) -> str:
        # Use SQLite if enabled or for development
        if self.USE_SQLITE:
            return "sqlite+aiosqlite:///./test.db"
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file = ".env"

settings = Settings()