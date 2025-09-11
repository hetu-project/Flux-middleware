from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from functools import lru_cache
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Hetu Middleware"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Database settings
    DB_SERVER_HOST: str = os.getenv("DB_SERVER_HOST", "localhost")
    DB_SERVER_PORT: int = int(os.getenv("DB_SERVER_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "flux_middle")
    DB_USER: str = os.getenv("DB_USER", "litterpigger")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    
    # Twitter 采集服务配置
    TWITTER_SERVER_IP: str = os.getenv("TWITTER_SERVER_IP", "")
    TWITTER_SERVER_PORT: int = int(os.getenv("TWITTER_SERVER_PORT", "5005"))
    
    @property
    def DATABASE_URL(self) -> str:
        """获取数据库 URL"""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_SERVER_HOST}:{self.DB_SERVER_PORT}/{self.DB_NAME}"
    
    @property
    def twitter_service_url(self) -> str:
        """获取 Twitter 服务完整 URL"""
        return f"http://{self.TWITTER_SERVER_IP}:{self.TWITTER_SERVER_PORT}"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        env_file_encoding='utf-8'
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()
