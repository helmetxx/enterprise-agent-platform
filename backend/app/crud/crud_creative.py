from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.creative import (
    CreativeProject, DocumentAnalysis, MarketAnalysis,
    IdeaGeneration, GeneratedImage, SolutionDesign
)
from app.schemas.creative import (
    CreativeProjectCreate, DocumentAnalysisCreate, MarketAnalysisCreate,
    IdeaGenerationCreate, GeneratedImageCreate, SolutionDesignCreate,
    CreativeProjectUpdate
)

class CRUDCreativeProject(CRUDBase[CreativeProject, CreativeProjectCreate, CreativeProjectCreate]):
    def get_by_user(self, db: Session, *, user_id: str) -> List[CreativeProject]:
        return db.query(self.model).filter(self.model.user_id == user_id).all()

    def get_by_enterprise(self, db: Session, *, enterprise_id: str) -> List[CreativeProject]:
        return db.query(self.model).filter(self.model.enterprise_id == enterprise_id).all()

class CRUDDocumentAnalysis(CRUDBase[DocumentAnalysis, DocumentAnalysisCreate, DocumentAnalysisCreate]):
    def get_by_project(self, db: Session, *, project_id: str) -> List[DocumentAnalysis]:
        return db.query(self.model).filter(self.model.project_id == project_id).all()

class CRUDMarketAnalysis(CRUDBase[MarketAnalysis, MarketAnalysisCreate, MarketAnalysisCreate]):
    def get_by_project(self, db: Session, *, project_id: str) -> List[MarketAnalysis]:
        return db.query(self.model).filter(self.model.project_id == project_id).all()

class CRUDIdeaGeneration(CRUDBase[IdeaGeneration, IdeaGenerationCreate, IdeaGenerationCreate]):
    def get_by_project(self, db: Session, *, project_id: str) -> List[IdeaGeneration]:
        return db.query(self.model).filter(self.model.project_id == project_id).all()

class CRUDGeneratedImage(CRUDBase[GeneratedImage, GeneratedImageCreate, GeneratedImageCreate]):
    def get_by_idea(self, db: Session, *, idea_id: str) -> List[GeneratedImage]:
        return db.query(self.model).filter(self.model.idea_id == idea_id).all()

class CRUDSolutionDesign(CRUDBase[SolutionDesign, SolutionDesignCreate, SolutionDesignCreate]):
    def get_by_project(self, db: Session, *, project_id: str) -> Optional[SolutionDesign]:
        return db.query(self.model).filter(self.model.project_id == project_id).first()

class CRUDCreative(CRUDBase[CreativeProject, CreativeProjectCreate, CreativeProjectUpdate]):
    def get_by_owner(self, db: Session, *, owner_id: int) -> List[CreativeProject]:
        return db.query(self.model).filter(CreativeProject.owner_id == owner_id).all()

creative_project = CRUDCreativeProject(CreativeProject)
document_analysis = CRUDDocumentAnalysis(DocumentAnalysis)
market_analysis = CRUDMarketAnalysis(MarketAnalysis)
idea_generation = CRUDIdeaGeneration(IdeaGeneration)
generated_image = CRUDGeneratedImage(GeneratedImage)
solution_design = CRUDSolutionDesign(SolutionDesign)
creative = CRUDCreative(CreativeProject) 