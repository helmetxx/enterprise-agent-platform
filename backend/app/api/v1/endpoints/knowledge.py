from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
import os
from app.core.config import settings
from pathlib import Path
import logging
from datetime import datetime
from app.core.dify import dify_client
import uuid

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/", response_model=List[schemas.KnowledgeBase])
def get_knowledge_bases(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """获取知识库列表"""
    knowledge_bases = crud.knowledge_base.get_by_user(
        db, user_id=current_user.id, skip=skip, limit=limit
    )
    return knowledge_bases

@router.delete("/{id}", status_code=204)
def delete_knowledge_base(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user)
):
    """删除知识库"""
    knowledge_base = crud.knowledge_base.get(db=db, id=id)
    if not knowledge_base:
        raise HTTPException(status_code=404, detail="Knowledge base not found")
    if knowledge_base.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    crud.knowledge_base.remove(db=db, id=id)
    return None

@router.post("/", response_model=schemas.KnowledgeBase)
async def create_knowledge_base(
    *,
    db: Session = Depends(deps.get_db),
    knowledge_base_in: schemas.KnowledgeBaseCreate,
    current_user: models.User = Depends(deps.get_current_user)
):
    """创建知识库"""
    knowledge_base = await crud.knowledge_base.create_with_owner_and_sync_dify(
        db=db,
        obj_in=knowledge_base_in,
        owner_id=current_user.id
    )
    return knowledge_base

@router.post("/{id}/documents", response_model=schemas.Document)
async def upload_document(
    id: int,
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    try:
        # 1. 验证文件大小
        content = await file.read()
        if len(content) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=400, detail="File too large")
        
        # 2. 验证知识库存在且属于当前用户
        kb = crud.knowledge_base.get(db, id=id)
        if not kb:
            raise HTTPException(status_code=404, detail="Knowledge base not found")
        if kb.created_by != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        
        # 3. 保存文件到本地存储
        upload_dir = Path(settings.UPLOAD_DIR) / str(id)
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / file.filename
        
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        logger.info(f"File saved to: {file_path}")
        
        # 4. 创建文档记录
        doc_in = schemas.DocumentCreate(
            filename=file.filename,
            file_type=file.content_type,
            knowledge_base_id=id,
            file_path=str(file_path),
            status="pending",
            sync_status="pending"
        )
        
        document = crud.document.create(db, obj_in=doc_in)
        
        # 5. 如果知识库已同步到DIFY，则同步文档
        if kb.dify_kb_id:
            try:
                dify_response = await dify_client.create_document_by_file(
                    dataset_id=kb.dify_kb_id,
                    file_path=str(file_path),
                    file_name=file.filename
                )
                
                # 更新文档的DIFY同步状态
                document = crud.document.update(
                    db,
                    db_obj=document,
                    obj_in={
                        "sync_status": "success",
                        "dify_document_id": dify_response["document"]["id"],
                        "last_sync_time": datetime.utcnow()
                    }
                )
                
            except Exception as e:
                # DIFY同步失败不影响本地存储
                document = crud.document.update(
                    db,
                    db_obj=document,
                    obj_in={
                        "sync_status": "failed",
                        "sync_error": str(e),
                        "last_sync_time": datetime.utcnow()
                    }
                )
                logger.error(f"Failed to sync document to DIFY: {str(e)}")
                # 不抛出异常，继续返回成功创建的文档
        
        return document
                
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def save_upload_file(file: UploadFile) -> Path:
    """保存上传的文件到临时目录"""
    # 验证文件大小
    file_size = 0
    content = await file.read()
    file_size = len(content)
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="File too large")
    
    # 创建临时目录
    temp_dir = Path(settings.UPLOAD_DIR) / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成临时文件路径
    file_path = temp_dir / f"{uuid.uuid4()}_{file.filename}"
    
    # 保存文件
    with open(file_path, "wb") as buffer:
        buffer.write(content)
    
    return file_path 