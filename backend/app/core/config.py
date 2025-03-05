from typing import Any, Dict, List, Optional, Union
# 修改导入语句，兼容 pydantic v1 和 v2
try:
    # 尝试从 pydantic_settings 导入 (pydantic v2)
    from pydantic_settings import BaseSettings
except ImportError:
    # 如果失败，从 pydantic 导入 (pydantic v1)
    from pydantic import BaseSettings
from pydantic import validator, AnyHttpUrl, EmailStr, HttpUrl, PostgresDsn
import secrets
import logging
import os
import tempfile

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
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    # JWT
    JWT_SECRET: str = "your-secret-key"
    
    # 文件上传配置
    UPLOAD_DIR: str = "uploads"  # 相对于项目根目录的路径
    MAX_UPLOAD_SIZE: int = 15 * 1024 * 1024  # 15MB

    # DIFY配置
    DIFY_API_BASE_URL: str = "https://api.dify.ai/v1"
    DIFY_API_KEY: str = "dataset-EDHGw4D7Yug1r3H1FBwOQnuS"

    # 外部报表系统配置
    REPORT_API_BASE_URL: str = "https://test.ihotel.cn"
    REPORT_API_PATH: str = "/inn-report/report/export"
    REPORT_API_AUTH_TOKEN: str = "eyJhbGciOiJIUzUxMiJ9.eyJkZXZpY2VUeXBlIjoiQ09NUFVURVIiLCJtYWluQXBwQ29kZSI6IlNTTyIsIm9yZ0NvZGUiOiJHQ0lOTjAwMSIsInVjU2VydmVyVXJsIjoiaHR0cHM6Ly90ZXN0Lmlob3RlbC5jbi91Yy13ZWIvIiwiYXBwQ29kZSI6IklOTiIsInVzZXJUeXBlIjoiU1VQRVIiLCJsb2dpbkF0IjoxNzQxMDY1MDI0MDAwLCJwcmluY2lwYWxVc2VyQ29kZSI6IkdDSU5OMDAxX0FETUlOIiwiZXhwIjozMjUwMzY1MTIwMCwidXNlckNvZGUiOiJVQ0FETUlOIn0.Iof-gwRa-M1BUebO9NJ92fHwz114cZh5JSqK6CET35q4Mu1ZUiMFTBlwYPJO6hlQAMmHzsSHrvLqb0QyoLAmXA"
    REPORT_API_LANGUAGE: str = "zh-CN"
    REPORT_TEMP_DIR: str = os.path.join(tempfile.gettempdir(), "reports")

    # 修改报表文件存储相关配置
    REPORT_STORAGE_DIR: str = "reports"  # 报表文件存储目录（物理路径，相对于项目根目录）
    REPORT_URL_BASE: str = "/reports"  # 报表文件访问的URL基础路径
    SERVER_HOST: str = "http://localhost:8000"  # 服务器主机名和端口

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
logger.info(f"Initialized settings with DB_USER: {settings.DB_USER}")
logger.info(f"Database URI: {settings.SQLALCHEMY_DATABASE_URI}")
logger.info(f"Report temp directory: {settings.REPORT_TEMP_DIR}") 