from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100), index=True)
    hashed_password = Column(String(200), nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    # 关联关系
    projects = relationship("CreativeProject", back_populates="owner", cascade="all, delete-orphan")
    created_agents = relationship("Agent", back_populates="creator")
    agent_usage_records = relationship("AgentUsageRecord", back_populates="user")
    knowledge_bases = relationship("KnowledgeBase", back_populates="creator") 