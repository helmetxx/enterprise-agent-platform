from .crud_user import CRUDUser, user
from .crud_creative import creative
from .crud_agent import agent
from .crud_knowledge import knowledge_base, document
from app.models.user import User

# 导出所有 CRUD 实例
__all__ = [
    "user",
    "creative",
    "agent",
    "knowledge_base",
    "document"
] 