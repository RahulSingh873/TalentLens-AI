from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class RoleRecommendation(BaseModel):
    role_title: str = Field(..., description="Target role e.g. Data Scientist, MLOps Engineer, Backend Engineer")
    match_percentage: float = Field(..., ge=0.0, le=100.0)
    overlapping_skills: List[str] = Field(default_factory=list)
    recommended_growth_skills: List[str] = Field(default_factory=list, description="Skills to acquire for 100% role readiness")
    justification: str = Field(..., description="Evidence-based reasoning for recommendation")


class CandidateRecommendationResponse(BaseModel):
    candidate_id: str
    candidate_name: str
    current_primary_skills: List[str]
    recommended_roles: List[RoleRecommendation]
    matched_open_jobs: List[Dict[str, str]] = Field(default_factory=list)


class CollaborativeFilterExperimentResult(BaseModel):
    algorithm: str = Field("Matrix Factorization (SVD / ALS Heuristic on Interaction Matrix)")
    dataset_description: str = Field("Synthetic anonymized recruiter interaction logs (saves, shortlists, clicks)")
    is_synthetic: bool = True
    num_users: int
    num_items: int
    num_interactions: int
    precision_at_5: float
    recall_at_5: float
    mrr: float
    disclaimer: str = Field(
        "Notice: This is an offline experimental evaluation on documented synthetic interaction records. "
        "It does not represent live production hiring outcomes or real human recruiter consensus."
    )
