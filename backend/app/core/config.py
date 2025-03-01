from typing import Any, Dict, List, Optional, Union
from pydantic import BaseSettings, validator, AnyHttpUrl
import secrets
import logging
import os

logger = logging.getLogger(__name__)

# 确保日志目录存在
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "app.log")),
        logging.StreamHandler()
    ]
)

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    DB_HOST: str = "mysql"  # 使用 Docker 服务名
    DB_PORT: int = 3306    # Docker 内部端口
    DB_USER: str = "root"
    DB_PASSWORD: str = "123456"
    DB_NAME: str = "agent_platform"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return f"mysql+pymysql://{values.get('DB_USER')}:{values.get('DB_PASSWORD')}@{values.get('DB_HOST')}:{values.get('DB_PORT')}/{values.get('DB_NAME')}"
    
    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    # JWT
    JWT_SECRET: str
    
    # 文件上传配置
    UPLOAD_DIR: str = "uploads"  # 相对于项目根目录的路径
    MAX_UPLOAD_SIZE: int = 15 * 1024 * 1024  # 15MB

    # DIFY配置
    DIFY_API_BASE_URL: str = "https://api.dify.ai/v1"
    DIFY_API_KEY: str = "dataset-EDHGw4D7Yug1r3H1FBwOQnuS"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
logger.info(f"Initialized settings with DB_USER: {settings.DB_USER}")
logger.info(f"Database URI: {settings.SQLALCHEMY_DATABASE_URI}") 