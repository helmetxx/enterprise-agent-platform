from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import logging
import time

from app.core.config import settings
from app.api.v1.api import api_router
from app.db.session import engine
from app.db.base import Base

app = FastAPI(
    title="Enterprise Agent Platform API",
    description="Backend API for Enterprise Agent Platform",
    version="1.0.0"
)

# 更新 CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 明确指定前端地址
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # 明确指定允许的方法
    allow_headers=["*"],
    expose_headers=["*"]
)

# 注册路由
app.include_router(api_router, prefix=settings.API_V1_STR)

# 创建数据库表
Base.metadata.create_all(bind=engine)

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(
        f"Method: {request.method}, "
        f"Path: {request.url.path}, "
        f"Duration: {duration:.3f}s, "
        f"Status: {response.status_code}"
    )
    return response

@app.get("/")
async def root():
    return {"message": "Welcome to Enterprise Agent Platform API"} 