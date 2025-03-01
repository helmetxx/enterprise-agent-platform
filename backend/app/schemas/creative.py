from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

# Base schemas
class CreativeProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "active"

class DocumentAnalysisBase(BaseModel):
    analysis_type: str
    content: dict

class MarketAnalysisBase(BaseModel):
    analysis_data: dict

class IdeaGenerationBase(BaseModel):
    idea_content: dict
    evaluation_score: Optional[str] = None

class GeneratedImageBase(BaseModel):
    image_url: str
    prompt_used: str
    style_config: dict

class SolutionDesignBase(BaseModel):
    technical_solution: dict
    feasibility_study: dict
    implementation_path: dict

# Create schemas
class CreativeProjectCreate(CreativeProjectBase):
    user_id: str
    enterprise_id: str
    owner_id: int

class DocumentAnalysisCreate(DocumentAnalysisBase):
    project_id: int

class MarketAnalysisCreate(MarketAnalysisBase):
    project_id: int

class IdeaGenerationCreate(IdeaGenerationBase):
    project_id: int

class GeneratedImageCreate(GeneratedImageBase):
    project_id: int
    idea_id: int

class SolutionDesignCreate(SolutionDesignBase):
    project_id: int

class CreativeProjectUpdate(CreativeProjectBase):
    pass

# Response schemas
class CreativeProject(CreativeProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class DocumentAnalysis(DocumentAnalysisBase):
    id: int
    project_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class MarketAnalysis(MarketAnalysisBase):
    id: int
    project_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class IdeaGeneration(IdeaGenerationBase):
    id: int
    project_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class GeneratedImage(GeneratedImageBase):
    id: int
    project_id: int
    idea_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class SolutionDesign(SolutionDesignBase):
    id: int
    project_id: int
    created_at: datetime

    class Config:
        orm_mode = True 