from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
from app.crud.base import CRUDBase
from app.models.agent import Agent, AgentUsageRecord
from app.schemas.agent import AgentCreate, AgentUpdate

class CRUDAgent(CRUDBase[Agent, AgentCreate, AgentUpdate]):
    def get_recommended_agents(self, db: Session, *, skip: int = 0, limit: int = 6) -> List[Agent]:
        return db.query(self.model)\
            .filter(self.model.status == 'active')\
            .order_by(self.model.sort_order.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()

    def get_recent_usage(self, db: Session, *, user_id: int, limit: int = 6) -> List[AgentUsageRecord]:
        return db.query(AgentUsageRecord)\
            .filter(AgentUsageRecord.user_id == user_id)\
            .order_by(desc(AgentUsageRecord.created_at))\
            .limit(limit)\
            .all()

    def create_usage_record(self, db: Session, *, user_id: int, agent_id: str) -> AgentUsageRecord:
        usage_record = AgentUsageRecord(
            user_id=user_id,
            agent_id=agent_id
        )
        db.add(usage_record)
        db.commit()
        db.refresh(usage_record)
        return usage_record

    def get_multi(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None
    ):
        """获取智能体列表，支持搜索"""
        query = db.query(self.model)
        if search:
            query = query.filter(
                or_(
                    self.model.name.ilike(f"%{search}%"),
                    self.model.description.ilike(f"%{search}%")
                )
            )
        return query.offset(skip).limit(limit).all()

    def count(self, db: Session, *, search: Optional[str] = None) -> int:
        """获取智能体总数"""
        query = db.query(self.model)
        if search:
            query = query.filter(
                or_(
                    self.model.name.ilike(f"%{search}%"),
                    self.model.description.ilike(f"%{search}%")
                )
            )
        return query.count()

agent = CRUDAgent(Agent) 