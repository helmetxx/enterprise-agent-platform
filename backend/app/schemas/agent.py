from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class AgentBase(BaseModel):
    name: str
    description: str
    category: str
    capabilities: Optional[List[str]] = None
    icon: Optional[str] = None
    status: str = 'inactive'
    version: Optional[str] = None
    sort_order: Optional[int] = 0

class AgentCreate(AgentBase):
    pass

class AgentUpdate(AgentBase):
    pass

class Agent(AgentBase):
    id: str
    created_by: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class AgentUsageRecord(BaseModel):
    id: str
    agent: Agent
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

class AgentList(BaseModel):
    items: List[Agent]
    total: int
    page: int
    page_size: int 