from typing import Optional, List
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class WeightConfig(BaseModel):
    required_skills: float = Field(0.40, ge=0.0, le=1.0)
    preferred_skills: float = Field(0.15, ge=0.0, le=1.0)
    semantic_similarity: float = Field(0.25, ge=0.0, le=1.0)
    experience: float = Field(0.15, ge=0.0, le=1.0)
    projects: float = Field(0.05, ge=0.0, le=1.0)


class JobDescriptionCreate(BaseModel):
    title: str = Field(..., description="Job role title e.g. Senior Machine Learning Engineer")
    company: Optional[str] = Field("HCLTech / Enterprise", description="Company or division name")
    department: Optional[str] = Field("Data & AI", description="Department")
    raw_text: str = Field(..., description="Complete job description text")
    required_skills: Optional[List[str]] = Field(None, description="Explicit or parsed mandatory skills")
    preferred_skills: Optional[List[str]] = Field(None, description="Explicit or parsed nice-to-have skills")
    min_experience_years: Optional[float] = Field(None, description="Required minimum years of relevant experience")
    weights: Optional[WeightConfig] = Field(None, description="Custom criteria weighting")


class JobDescriptionParsed(BaseModel):
    job_id: str = Field(..., description="Unique job posting ID")
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    department: str = Field("Data & AI", description="Department")
    raw_text: str = Field(..., description="Original job text")
    required_skills: List[str] = Field(default_factory=list, description="Mandatory core technical skills")
    preferred_skills: List[str] = Field(default_factory=list, description="Preferred / bonus skills")
    min_experience_years: float = Field(0.0, description="Minimum relevant years required")
    responsibilities: List[str] = Field(default_factory=list, description="Key duties and responsibilities")
    qualifications: List[str] = Field(default_factory=list, description="Degree or qualification requirements")
    weights: WeightConfig = Field(default_factory=WeightConfig, description="Importance weights")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
