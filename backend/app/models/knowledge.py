from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class KnowledgeBase(Base):
    __tablename__ = "knowledge_bases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    dify_kb_id = Column(String(100), unique=True)  # DIFY平台上的知识库ID
    dify_sync_status = Column(String(20), default="pending")  # pending, success, failed
    dify_error_detail = Column(Text)  # 记录DIFY同步失败的错误信息
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    documents = relationship("Document", back_populates="knowledge_base", cascade="all, delete-orphan")
    creator = relationship("User", back_populates="knowledge_bases")

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(100))
    file_path = Column(String(255))
    status = Column(String(50), default="pending")
    knowledge_base_id = Column(Integer, ForeignKey("knowledge_bases.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 新增字段
    dify_document_id = Column(String(100), nullable=True)
    sync_status = Column(String(20), nullable=False, default="pending")
    sync_error = Column(String(500), nullable=True)
    last_sync_time = Column(DateTime, nullable=True)

    knowledge_base = relationship("KnowledgeBase", back_populates="documents") 