from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# 使用常量而不是从 settings 获取
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(
    data: dict,
    expires_delta: timedelta = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> str:
    """验证 token 并返回用户ID"""
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id: str = payload.get("sub")  # 我们存储的是用户ID，不是email
        if user_id is None:
            return None
        return user_id
    except jwt.JWTError as e:
        logger.error(f"Token verification failed: {e}")
        return None 