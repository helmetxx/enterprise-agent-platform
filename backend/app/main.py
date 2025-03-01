from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router
from app.db.init_db import init_db
from app.db.session import SessionLocal
import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # 输出到控制台
        logging.FileHandler('app.log')  # 输出到文件
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Enterprise Agent Platform API")

# 记录应用启动日志
logger.info("Starting FastAPI application")

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 记录路由注册日志
logger.info("Registering API routes")
app.include_router(api_router, prefix=settings.API_V1_STR)
logger.info("API routes registered successfully")

# Initialize database with first superuser
@app.on_event("startup")
async def init_data():
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close() 