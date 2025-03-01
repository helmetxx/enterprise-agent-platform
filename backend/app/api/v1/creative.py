from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.creative import (
    CreativeProject,
    CreativeProjectCreate,
    CreativeProjectUpdate,
    DocumentAnalysis,
    MarketAnalysis
)
from app.crud import creative as crud
from app.deps import get_current_user, get_db

router = APIRouter()

@router.post("/projects/", response_model=CreativeProject)
def create_project(
    project: CreativeProjectCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.create_project(db, project, current_user)

@router.get("/projects/{project_id}", response_model=CreativeProject)
def get_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# 其他API接口... 