from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps
from app.models.user import User
from app.crud import crud_agent
from app.schemas.agent import Agent, AgentList

router = APIRouter()

@router.get("/agents", response_model=List[schemas.Agent])
def get_agents(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
):
    """获取所有智能体"""
    agents = crud.agent.get_multi(db, skip=skip, limit=limit)
    return agents

@router.get("/recommended", response_model=List[schemas.Agent])
def get_recommended_agents(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """获取推荐智能体"""
    agents = crud.agent.get_recommended_agents(db)
    return agents

@router.get("/recent-usage", response_model=List[schemas.AgentUsageRecord])
def get_recent_usage(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """获取最近使用记录"""
    records = crud.agent.get_recent_usage(db, user_id=current_user.id)
    return records

@router.get("/{agent_id}", response_model=schemas.Agent)
def get_agent(
    agent_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """获取特定智能体"""
    agent = crud.agent.get(db, id=agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.get("/", response_model=AgentList)
def get_agents_list(
    db: Session = Depends(deps.get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    current_user: User = Depends(deps.get_current_user)
):
    """获取智能体列表，支持分页和搜索"""
    skip = (page - 1) * page_size
    agents = crud.agent.get_multi(db, skip=skip, limit=page_size, search=search)
    total = crud.agent.count(db, search=search)
    
    return {
        "items": agents,
        "total": total,
        "page": page,
        "page_size": page_size
    } 