from typing import List
from fastapi import APIRouter, HTTPException

from ..schemas.recommendation import (
    RoleRecommendation,
    CandidateRecommendationResponse,
    CollaborativeFilterExperimentResult,
)
from ..recommendations.role_recommender import recommend_roles_for_candidate
from ..recommendations.content_recommender import recommend_jobs_for_candidate, recommend_candidates_for_job
from ..recommendations.collaborative_filter import ExperimentalCollaborativeFilter
from ..services.storage import store

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])


@router.get("/roles/{resume_id}", response_model=List[RoleRecommendation])
def get_role_recommendations(resume_id: str):
    """Recommends career trajectories and identifies skill gaps for a candidate."""
    if resume_id not in store.resumes:
        raise HTTPException(status_code=404, detail="Resume not found")
    resume = store.resumes[resume_id]
    return recommend_roles_for_candidate(resume)


@router.get("/jobs/{resume_id}")
def get_job_recommendations_for_candidate(resume_id: str):
    """Recommends open job positions that best match the candidate's skills and projects."""
    if resume_id not in store.resumes:
        raise HTTPException(status_code=404, detail="Resume not found")
    resume = store.resumes[resume_id]
    open_jobs = list(store.jobs.values())
    return recommend_jobs_for_candidate(resume, open_jobs)


@router.get("/candidates/{job_id}")
def get_candidate_recommendations_for_job(job_id: str):
    """Recommends best matching candidates from the talent pool for a job opening."""
    if job_id not in store.jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    job = store.jobs[job_id]
    resumes = list(store.resumes.values())
    return recommend_candidates_for_job(job, resumes)


@router.get("/collaborative-filtering", response_model=CollaborativeFilterExperimentResult)
def get_collaborative_filter_experiment():
    """
    Evaluates collaborative filtering on synthetic recruiter interaction logs.
    Includes explicit academic disclosure of synthetic data provenance.
    """
    # Synthetic recruiter interaction logs
    synthetic_interactions = [
        {"recruiter_id": "rec_01", "candidate_id": "cand_chen", "weight": 5.0},
        {"recruiter_id": "rec_01", "candidate_id": "cand_martinez", "weight": 2.0},
        {"recruiter_id": "rec_02", "candidate_id": "cand_martinez", "weight": 5.0},
        {"recruiter_id": "rec_02", "candidate_id": "cand_kim", "weight": 3.0},
        {"recruiter_id": "rec_03", "candidate_id": "cand_danvers", "weight": 4.0},
        {"recruiter_id": "rec_03", "candidate_id": "cand_chen", "weight": 4.0},
        {"recruiter_id": "rec_04", "candidate_id": "cand_kim", "weight": 5.0},
        {"recruiter_id": "rec_04", "candidate_id": "cand_martinez", "weight": 3.0},
        {"recruiter_id": "rec_05", "candidate_id": "cand_chen", "weight": 5.0},
        {"recruiter_id": "rec_05", "candidate_id": "cand_danvers", "weight": 3.0},
    ]

    cf_engine = ExperimentalCollaborativeFilter(n_factors=2)
    metrics = cf_engine.fit(synthetic_interactions)
    return cf_engine.get_result(metrics)
