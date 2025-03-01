from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class KnowledgeBaseBase(BaseModel):
    name: str
    description: Optional[str] = None

class KnowledgeBaseCreate(KnowledgeBaseBase):
    pass

class KnowledgeBaseUpdate(KnowledgeBaseBase):
    pass

class KnowledgeBase(KnowledgeBaseBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    document_count: Optional[int] = 0

    class Config:
        orm_mode = True

class DocumentBase(BaseModel):
    filename: str
    file_type: str
    status: str = "pending"

class DocumentCreate(DocumentBase):
    knowledge_base_id: int
    file_path: Optional[str] = None

class Document(DocumentBase):
    id: int
    knowledge_base_id: int
    file_path: Optional[str]
    dify_document_id: Optional[str] = None
    sync_status: str = "pending"
    sync_error: Optional[str] = None
    last_sync_time: Optional[datetime] = None

    class Config:
        orm_mode = True 