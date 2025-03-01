from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum, DECIMAL, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
import uuid

class CreativeProject(Base):
    __tablename__ = "creative_projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000))
    status = Column(String(50), default="active")
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # 关联关系
    owner = relationship("User", back_populates="projects")
    document_analyses = relationship("DocumentAnalysis", back_populates="project", cascade="all, delete-orphan")
    market_analyses = relationship("MarketAnalysis", back_populates="project", cascade="all, delete-orphan")
    idea_generations = relationship("IdeaGeneration", back_populates="project", cascade="all, delete-orphan")
    generated_images = relationship("GeneratedImage", back_populates="project", cascade="all, delete-orphan")
    solution_designs = relationship("SolutionDesign", back_populates="project", cascade="all, delete-orphan")

class DocumentAnalysis(Base):
    __tablename__ = "document_analysis"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("creative_projects.id", ondelete="CASCADE"), nullable=False)
    analysis_type = Column(String(50))
    content = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())

    project = relationship("CreativeProject", back_populates="document_analyses")

class MarketAnalysis(Base):
    __tablename__ = "market_analysis"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("creative_projects.id", ondelete="CASCADE"), nullable=False)
    analysis_data = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())

    project = relationship("CreativeProject", back_populates="market_analyses")

class IdeaGeneration(Base):
    __tablename__ = "idea_generations"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("creative_projects.id", ondelete="CASCADE"), nullable=False)
    idea_content = Column(JSON)
    evaluation_score = Column(String(10))
    created_at = Column(DateTime, server_default=func.now())

    project = relationship("CreativeProject", back_populates="idea_generations")
    generated_images = relationship("GeneratedImage", back_populates="idea", cascade="all, delete-orphan")

class GeneratedImage(Base):
    __tablename__ = "generated_images"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("creative_projects.id", ondelete="CASCADE"), nullable=False)
    idea_id = Column(Integer, ForeignKey("idea_generations.id", ondelete="CASCADE"), nullable=False)
    image_url = Column(String(255))
    prompt_used = Column(String(1000))
    style_config = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())

    project = relationship("CreativeProject", back_populates="generated_images")
    idea = relationship("IdeaGeneration", back_populates="generated_images")

class SolutionDesign(Base):
    __tablename__ = "solution_designs"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("creative_projects.id", ondelete="CASCADE"), nullable=False)
    technical_solution = Column(JSON)
    feasibility_study = Column(JSON)
    implementation_path = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())

    project = relationship("CreativeProject", back_populates="solution_designs") 