from sqlalchemy import Column, String, Text, JSON, DateTime, Integer, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Agent(Base):
    __tablename__ = "agents"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    icon = Column(String(255))
    category = Column(String(50), nullable=False)
    capabilities = Column(JSON)
    status = Column(String(20), nullable=False, default='inactive')
    version = Column(String(20))
    sort_order = Column(Integer, default=0)
    
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关联
    creator = relationship("User", back_populates="created_agents")
    usage_records = relationship("AgentUsageRecord", back_populates="agent")

class AgentUsageRecord(Base):
    __tablename__ = "agent_usage_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    agent_id = Column(String(36), ForeignKey('agents.id'), nullable=False)
    status = Column(String(20), nullable=False, default='completed')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关联
    user = relationship("User", back_populates="agent_usage_records")
    agent = relationship("Agent", back_populates="usage_records") 