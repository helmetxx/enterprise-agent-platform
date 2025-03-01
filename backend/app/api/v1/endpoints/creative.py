from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.utils.pdf_generator import PDFGenerator
from fastapi.responses import FileResponse
import os

router = APIRouter()
pdf_generator = PDFGenerator()

@router.post("/projects/", response_model=schemas.CreativeProject)
def create_project(
    project_in: schemas.CreativeProjectCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """创建新项目"""
    project = crud.creative_project.create(db=db, obj_in=project_in)
    return project

@router.get("/projects/", response_model=List[schemas.CreativeProject])
def get_projects(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user)
):
    """获取项目列表"""
    projects = crud.creative_project.get_by_user(db=db, user_id=current_user.id)
    return projects

@router.post("/projects/{project_id}/document-analysis/", response_model=schemas.DocumentAnalysis)
def create_document_analysis(
    project_id: str,
    analysis_in: schemas.DocumentAnalysisCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """创建文档分析"""
    project = crud.creative_project.get(db=db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    analysis = crud.document_analysis.create(db=db, obj_in=analysis_in)
    return analysis

@router.post("/projects/{project_id}/market-analysis/", response_model=schemas.MarketAnalysis)
def create_market_analysis(
    *,
    db: Session = Depends(deps.get_db),
    project_id: str,
    analysis_in: schemas.MarketAnalysisCreate,
    current_user: models.User = Depends(deps.get_current_user)
):
    """创建市场分析"""
    project = crud.creative_project.get(db=db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    analysis = crud.market_analysis.create(db=db, obj_in=analysis_in)
    return analysis

@router.post("/projects/{project_id}/idea-generation/", response_model=schemas.IdeaGeneration)
def create_idea_generation(
    *,
    db: Session = Depends(deps.get_db),
    project_id: str,
    idea_in: schemas.IdeaGenerationCreate,
    current_user: models.User = Depends(deps.get_current_user)
):
    """创建创意生成"""
    project = crud.creative_project.get(db=db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    idea = crud.idea_generation.create(db=db, obj_in=idea_in)
    return idea

@router.post("/ideas/{idea_id}/images/", response_model=schemas.GeneratedImage)
def create_generated_image(
    *,
    db: Session = Depends(deps.get_db),
    idea_id: str,
    image_in: schemas.GeneratedImageCreate,
    current_user: models.User = Depends(deps.get_current_user)
):
    """创建生成图片"""
    idea = crud.idea_generation.get(db=db, id=idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    image = crud.generated_image.create(db=db, obj_in=image_in)
    return image

@router.post("/projects/{project_id}/solution/", response_model=schemas.SolutionDesign)
def create_solution_design(
    *,
    db: Session = Depends(deps.get_db),
    project_id: str,
    solution_in: schemas.SolutionDesignCreate,
    current_user: models.User = Depends(deps.get_current_user)
):
    """创建方案设计"""
    project = crud.creative_project.get(db=db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    solution = crud.solution_design.create(db=db, obj_in=solution_in)
    return solution

@router.get("/projects/{project_id}", response_model=schemas.CreativeProject)
def get_project(
    *,
    db: Session = Depends(deps.get_db),
    project_id: str,
    current_user: models.User = Depends(deps.get_current_user)
):
    """获取项目详情"""
    project = crud.creative_project.get(db=db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.get("/projects/{project_id}/document-analysis", response_model=List[schemas.DocumentAnalysis])
def get_document_analyses(
    *,
    db: Session = Depends(deps.get_db),
    project_id: str,
    current_user: models.User = Depends(deps.get_current_user)
):
    """获取文档分析列表"""
    analyses = crud.document_analysis.get_by_project(db=db, project_id=project_id)
    return analyses

@router.get("/projects/{project_id}/market-analysis", response_model=List[schemas.MarketAnalysis])
def get_market_analyses(
    *,
    db: Session = Depends(deps.get_db),
    project_id: str,
    current_user: models.User = Depends(deps.get_current_user)
):
    """获取市场分析列表"""
    analyses = crud.market_analysis.get_by_project(db=db, project_id=project_id)
    return analyses

@router.get("/projects/{project_id}/ideas", response_model=List[schemas.IdeaGeneration])
def get_ideas(
    *,
    db: Session = Depends(deps.get_db),
    project_id: str,
    current_user: models.User = Depends(deps.get_current_user)
):
    """获取创意列表"""
    ideas = crud.idea_generation.get_by_project(db=db, project_id=project_id)
    return ideas

@router.get("/ideas/{idea_id}/images", response_model=List[schemas.GeneratedImage])
def get_generated_images(
    *,
    db: Session = Depends(deps.get_db),
    idea_id: str,
    current_user: models.User = Depends(deps.get_current_user)
):
    """获取生成图片列表"""
    images = crud.generated_image.get_by_idea(db=db, idea_id=idea_id)
    return images

@router.get("/projects/{project_id}/solution", response_model=schemas.SolutionDesign)
def get_solution_design(
    *,
    db: Session = Depends(deps.get_db),
    project_id: str,
    current_user: models.User = Depends(deps.get_current_user)
):
    """获取方案设计"""
    solution = crud.solution_design.get_by_project(db=db, project_id=project_id)
    if not solution:
        raise HTTPException(status_code=404, detail="Solution not found")
    return solution

@router.patch("/projects/{project_id}/status", response_model=schemas.CreativeProject)
def update_project_status(
    *,
    db: Session = Depends(deps.get_db),
    project_id: str,
    status: str,
    current_user: models.User = Depends(deps.get_current_user)
):
    """更新项目状态"""
    project = crud.creative_project.get(db=db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if status not in ['draft', 'in_progress', 'completed']:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    project_data = {"status": status}
    updated_project = crud.creative_project.update(
        db=db,
        db_obj=project,
        obj_in=project_data
    )
    return updated_project

@router.delete("/projects/{project_id}", status_code=204)
def delete_project(
    *,
    db: Session = Depends(deps.get_db),
    project_id: str,
    current_user: models.User = Depends(deps.get_current_user)
):
    """删除项目"""
    project = crud.creative_project.get(db=db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    crud.creative_project.remove(db=db, id=project_id)

@router.post("/generate-product-pdf")
async def generate_product_pdf(
    filename: str,
    product_requirements: str,
    product_features: str,
    product_image_url: str,
    marketing_copy: str
):
    try:
        # 生成PDF
        pdf_path = pdf_generator.generate_product_pdf(
            filename=filename,
            product_requirements=product_requirements,
            product_features=product_features,
            product_image_url=product_image_url,
            marketing_copy=marketing_copy
        )
        
        # 返回生成的PDF文件
        return FileResponse(
            pdf_path,
            media_type='application/pdf',
            filename=os.path.basename(pdf_path)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 定期清理旧文件的任务
@router.on_event("startup")
async def startup_event():
    pdf_generator.cleanup_old_files()

# 添加其他必要的路由... 