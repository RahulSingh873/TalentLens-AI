from typing import Optional, List, Literal
from pydantic import BaseModel, Field
from .job import WeightConfig


class SkillMatchEvidence(BaseModel):
    skill: str = Field(..., description="Canonical skill name")
    status: Literal["matched", "missing", "uncertain"] = Field(..., description="Match verification status")
    is_required: bool = Field(True, description="True if mandatory requirement, False if preferred")
    confidence: float = Field(1.0, ge=0.0, le=1.0)
    source_snippet: Optional[str] = Field(None, description="Exact sentence or bullet point supporting presence")
    match_type: Literal["exact", "alias", "semantic", "none"] = Field("exact")


class ComponentScore(BaseModel):
    name: str = Field(..., description="Score dimension: Required Skills, Preferred Skills, Semantic, Experience, Projects")
    raw_score: float = Field(..., ge=0.0, le=1.0, description="Normalized raw score [0, 1]")
    weight: float = Field(..., ge=0.0, le=1.0, description="Configured weight [0, 1]")
    weighted_score: float = Field(..., ge=0.0, le=1.0, description="raw_score * weight")
    explanation: str = Field(..., description="Human-interpretable explanation of score derivation")
    evidence: List[str] = Field(default_factory=list, description="Concrete evidence snippets from candidate resume")


class CandidateMatchResult(BaseModel):
    candidate_id: str = Field(...)
    candidate_name: str = Field(...)
    resume_id: str = Field(...)
    job_id: str = Field(...)
    overall_score: float = Field(..., ge=0.0, le=100.0, description="Composite match score out of 100")
    calibrated_percentile: Optional[float] = Field(None, description="Cohort relative percentile ranking")
    score_breakdown: List[ComponentScore] = Field(default_factory=list)
    matched_required_skills: List[str] = Field(default_factory=list)
    missing_required_skills: List[str] = Field(default_factory=list)
    matched_preferred_skills: List[str] = Field(default_factory=list)
    missing_preferred_skills: List[str] = Field(default_factory=list)
    skill_evidences: List[SkillMatchEvidence] = Field(default_factory=list)
    experience_years_found: float = Field(0.0)
    experience_years_required: float = Field(0.0)
    experience_evidence: List[str] = Field(default_factory=list)
    project_evidence: List[str] = Field(default_factory=list)
    explanation_summary: str = Field(...)
    limitations_and_uncertainties: List[str] = Field(default_factory=list)
    recommendation_tier: Literal["Strong Match", "Potential Match", "Borderline / Needs Review", "Low Alignment"] = Field(...)
    ranked_position: Optional[int] = Field(None)


class MatchRequest(BaseModel):
    job_id: str
    resume_ids: Optional[List[str]] = Field(None, description="Subset of resume IDs to match, or None for all")
    weights: Optional[WeightConfig] = Field(None, description="Overrides for scoring criteria")


class ScreeningResponse(BaseModel):
    job_id: str
    job_title: str
    total_evaluated: int
    weights: WeightConfig
    candidates: List[CandidateMatchResult]
