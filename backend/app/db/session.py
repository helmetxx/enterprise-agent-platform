from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

logger.info(f"Creating database engine with URI: {settings.SQLALCHEMY_DATABASE_URI}")

# 确保使用 pymysql 作为驱动
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=True  # 添加这行来查看 SQL 日志
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 