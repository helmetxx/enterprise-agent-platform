from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.knowledge import KnowledgeBase, Document
from app.schemas.knowledge import KnowledgeBaseCreate, KnowledgeBaseUpdate, DocumentCreate
from app.core.dify import dify_client
import logging

logger = logging.getLogger(__name__)

class CRUDKnowledgeBase(CRUDBase[KnowledgeBase, KnowledgeBaseCreate, KnowledgeBaseUpdate]):
    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[KnowledgeBase]:
        return (
            db.query(self.model)
            .filter(KnowledgeBase.created_by == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_dify_id(self, db: Session, *, dify_kb_id: str) -> Optional[KnowledgeBase]:
        return db.query(self.model).filter(KnowledgeBase.dify_kb_id == dify_kb_id).first()

    async def create_with_owner_and_sync_dify(
        self, db: Session, *, obj_in: KnowledgeBaseCreate, owner_id: int
    ) -> KnowledgeBase:
        # 1. 先创建本地知识库记录
        db_obj = KnowledgeBase(
            name=obj_in.name,
            description=obj_in.description,
            created_by=owner_id,
            dify_sync_status="pending"
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # 2. 尝试同步到 DIFY
        try:
            dify_kb = await dify_client.create_knowledge_base(
                name=obj_in.name,
                description=obj_in.description
            )

            # 同步成功，更新状态和DIFY ID
            db_obj.dify_kb_id = dify_kb.get("id")  # DIFY API 返回的 ID
            db_obj.dify_sync_status = "success"
            db_obj.dify_error_detail = None
            
        except Exception as e:
            # 同步失败，记录错误信息
            error_detail = f"Failed to sync with DIFY: {str(e)}"
            logger.error(error_detail)
            db_obj.dify_sync_status = "failed"
            db_obj.dify_error_detail = error_detail
            
        # 无论同步成功还是失败，都更新本地记录
        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDDocument(CRUDBase[Document, DocumentCreate, DocumentCreate]):
    def get_by_knowledge_base(
        self, db: Session, *, knowledge_base_id: int
    ) -> List[Document]:
        return (
            db.query(self.model)
            .filter(Document.knowledge_base_id == knowledge_base_id)
            .all()
        )

knowledge_base = CRUDKnowledgeBase(KnowledgeBase)
document = CRUDDocument(Document) 