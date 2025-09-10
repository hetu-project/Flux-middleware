from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "Hetu Middleware"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Twitter 采集服务配置
    TWITTER_SERVER_IP: str = "54.179.155.13"
    TWITTER_SERVER_PORT: int = 5005
    
    @property
    def twitter_service_url(self) -> str:
        """获取 Twitter 服务完整 URL"""
        return f"http://{self.TWITTER_SERVER_IP}:{self.TWITTER_SERVER_PORT}"
    
    # 数据库配置
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "hetu"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @property
    def get_database_url(self) -> str:
        """获取数据库URL"""
        if self.SQLALCHEMY_DATABASE_URI:
            return self.SQLALCHEMY_DATABASE_URI
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    class Config:
        case_sensitive = True
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
